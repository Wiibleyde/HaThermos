from flask import Flask, render_template, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import flask.cli
import subprocess
import logging
import argparse
import docker
import requests

# file import  
from utils.database import DatabaseService
from utils.flaskform import LoginForm, RegisterForm, CreateServerForm, OpPlayerForm, WhitelistPlayerForm
from services.config import ConfigService
from services.logger import Logger
from utils.ports import PortsService
from utils.minecraft import MinecraftService

# ==============================================================================
# Environment variables 
app = Flask(__name__)
app.config['SECRET_KEY'] = '10fba9806ecc78b383c2bc6345b6145794a35acac9c9298c95fd011c9ec7fd70'
login_manager=LoginManager()
login_manager.init_app(app)
client = docker.from_env()
# ==============================================================================

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

def buildCss():
    logger.addDebug("Building CSS : building")
    subprocess.run(["./tailwindcss", "-i", "./static/css/input.css", "-o", "./static/css/tailwind.css"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logger.addDebug("Building CSS : building... Done")

def parseArgs():
    parser = argparse.ArgumentParser(description="HaThermos Web Panel")
    parser.add_argument('-d','--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    if args.debug:
        return True
    else:
        return False
    
def checkMinecraftUsername(username):
    url = "https://api.minetools.eu/uuid/" + username
    response = requests.get(url)
    logger.addDebug(f'Checking username : {response.status_code}')
    if response.status_code == 200:
        logger.addDebug(f'Checking username : {response.json()}')
        try:
            if response.json()['id'] == "null":
                logger.addDebug(f'Checking username : {username} not found')
                return False
            else:
                logger.addDebug(f'Checking username : {username} found')
                return True
        except:
            logger.addDebug(f'Checking username : {username} not found')
            return False
    else:
        logger.addError(f'Error while checking username : {response.status_code}')
        return False
    
def startDocker(version, id, port):
    logger.addDebug(f"Starting docker {id}...")
    try:
        if version == '1.8.8' or version =='1.9.4' or version == '1.10.2' or version == '1.11.2' or version == '1.12.2' or version == '1.13.2' or version == '1.14.4' or version == '1.15.2' or version == '1.16.5' or version == '1.17.1':
            client.containers.run(image=f"itzg/minecraft-server:java8-graalvm-ce", detach=True, ports={25565: port}, environment=["EULA=TRUE", f"VERSION={version}","MEMORY=2G","TYPE=PAPER","MOTD=HaThermos Server","SPIGET_RESSOURCES=#327","ENABLE_COMMAND_BLOCK=true","ENABLE_QUERY=true","MAX_PLAYERS=15","ENABLE_WHITELIST=true","ICON=https://hathermos.bonnell.fr/static/assets/HaThermos.png","OVERRIDE_ICON=true"], name=f"{id}hathermos", network="hathermos_net", volumes={f"/srv/minecraft-data/{id}": {"bind": "/data", "mode": "rw"}})
        else:
            client.containers.run(image=f"itzg/minecraft-server:java17-graalvm-ce", detach=True, ports={25565: port}, environment=["EULA=TRUE", f"VERSION={version}","MEMORY=2G","TYPE=PAPER","MOTD=HaThermos Server","SPIGET_RESSOURCES=#327","ENABLE_COMMAND_BLOCK=true","ENABLE_QUERY=true","MAX_PLAYERS=15","ENABLE_WHITELIST=true","ICON=https://hathermos.bonnell.fr/static/assets/HaThermos.png","OVERRIDE_ICON=true"], name=f"{id}hathermos", network="hathermos_net", volumes={f"/srv/minecraft-data/{id}": {"bind": "/data", "mode": "rw"}})
        logger.addDebug(f"Starting docker {id}... Done")
        return True
    except Exception as e:
        logger.addError(f"Error starting docker {id}: {e}")
        return False
    
def opPlayer(id,playerName):
    logger.addDebug(f"Op player {playerName} in docker {id}...")
    try:
        container = client.containers.get(f"{id}hathermos")
        container.exec_run(f"mc-send-to-console \"op {playerName}\"")
        logger.addDebug(f"Op player {playerName} in docker {id}... Done")
        return True
    except Exception as e:
        logger.addError(f"Error op player {playerName} in docker {id}: {e}")
        return False
    
def deopPlayer(id,playerName):
    logger.addDebug(f"Deop player {playerName} in docker {id}...")
    try:
        container = client.containers.get(f"{id}hathermos")
        container.exec_run(f"mc-send-to-console \"deop {playerName}\"")
        logger.addDebug(f"Deop player {playerName} in docker {id}... Done")
        return True
    except Exception as e:
        logger.addError(f"Error deop player {playerName} in docker {id}: {e}")
        return False
    
def addPlayerToWhitelist(id,playerName):
    logger.addDebug(f"Add player {playerName} to whitelist in docker {id}...")
    try:
        container = client.containers.get(f"{id}hathermos")
        container.exec_run(f"mc-send-to-console \"whitelist add {playerName}\"")
        logger.addDebug(f"Add player {playerName} to whitelist in docker {id}... Done")
        return True
    except Exception as e:
        logger.addError(f"Error add player {playerName} to whitelist in docker {id}: {e}")
        return False

def removePlayerFromWhitelist(id,playerName):
    logger.addDebug(f"Remove player {playerName} from whitelist in docker {id}...")
    try:
        container = client.containers.get(f"{id}hathermos")
        container.exec_run(f"mc-send-to-console \"whitelist remove {playerName}\"")
        logger.addDebug(f"Remove player {playerName} from whitelist in docker {id}... Done")
        return True
    except Exception as e:
        logger.addError(f"Error remove player {playerName} from whitelist in docker {id}: {e}")
        return False
    
def enableWhitelist(id):
    logger.addDebug(f"Enable whitelist in docker {id}...")
    try:
        container = client.containers.get(f"{id}hathermos")
        container.exec_run(f"mc-send-to-console \"whitelist on\"")
        logger.addDebug(f"Enable whitelist in docker {id}... Done")
        return True
    except Exception as e:
        logger.addError(f"Error enable whitelist in docker {id}: {e}")
        return False

def stopDocker(id):
    logger.addDebug(f"Stopping docker {id}...")
    try:
        container = client.containers.get(f"{id}hathermos")
        # remove stop and remove container
        container.stop()
        container.remove()
        logger.addDebug(f"Stopping docker {id}... Done")
        return True
    except Exception as e:
        logger.addError(f"Error stopping docker {id}: {e}")
        return False

def createApp():
    logger.addDebug("Creating app...")
    app = Flask(__name__)
    logger.addDebug("Creating app... Done")
    return app

def ErrorHandler(e):
    logger.addError(f'Error : {e}')
    errorCode = e.code
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
    errorMessage = e.description
    if errorCode == 404:
        flash('Page not found', category='error')
        return render_template("error.html", ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Error", PageNameLower="error", userAuth=userAuth, ErrorMessage=errorMessage, ErrorCode=errorCode), 404
    else:
        flash('An error occured', category='error')
        return render_template("error.html", ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Error", PageNameLower="error", userAuth=userAuth), 500

@app.route('/')
def index():
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the home page')
    else:
        logger.addInfo('User is not logged in and going to the home page')
    return render_template("index.html", ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Home", PageNameLower="home", userAuth=userAuth)

@app.route('/about')
def about():
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the about page')
    else:
        logger.addInfo('User is not logged in and going to the about page')
    return render_template("about.html", ProjectName=jsonConfig.getConfig('ProjectName'), PageName="About", PageNameLower="about", userAuth=userAuth)

@app.route('/contact')
def contact():
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the contact page')
    else:
        logger.addInfo('User is not logged in and going to the contact page')
    return render_template("contact.html", ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Contact", PageNameLower="contact", userAuth=userAuth)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the login page')
        return redirect(url_for('dashboard'))
    else:
        logger.addInfo('User is not logged in and going to the login page')
    if form.validate_on_submit():
        if databaseObj.checkUser(form.usernameOrEmail.data, form.password.data):
            user = User(form.usernameOrEmail.data)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username/email or password', category='error')
            return redirect(url_for('login'))
    return render_template('login.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Login", PageNameLower="login", userAuth=userAuth)

@app.route('/logout')
@login_required
def logout():
    logger.addInfo(f'User {current_user.username} logged out')
    logout_user()
    flash('Logged out', category='success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the register page')
        return redirect(url_for('dashboard'))
    else:
        logger.addInfo('User is not logged in and going to the register page')
    if form.validate_on_submit():
        if form.confirmPassword.data == form.password.data:
            if not checkMinecraftUsername(form.username.data):
                flash('Invalid username, please enter you Minecraft username', category='error')
                return redirect(url_for('register'))
            if databaseObj.addUser(form.username.data, form.email.data, form.password.data):
                flash('Account created', category='success')
                return redirect(url_for('login'))
            else:
                flash('Username already exists', category='error')
                return redirect(url_for('register'))
        else:
            flash('Passwords do not match', category='error')
            return redirect(url_for('register'))
    return render_template('register.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Register", PageNameLower="register", userAuth=userAuth)

@app.route('/admin/accounts')
@login_required
def adminAccounts():
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the admin accounts page')
        if not databaseObj.isAdmin(current_user.username):
            flash('You are not an admin', category='error')
            return redirect(url_for('index'))
    else:
        logger.addInfo('User is not logged in and going to the admin accounts page')
        return redirect(url_for('index'))
    accounts = databaseObj.getUsers()
    logger.addDebug(accounts)
    return render_template("adminAccount.html", ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Admin Accounts", PageNameLower="admin/accounts", userAuth=userAuth, Accounts=accounts)

@app.route('/admin/servers')
@login_required
def adminServers():
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the admin servers page')
        if not databaseObj.isAdmin(current_user.username):
            flash('You are not an admin', category='error')
            return redirect(url_for('index'))
    else:
        logger.addInfo('User is not logged in and going to the admin servers page')
        return redirect(url_for('index'))
    servers = databaseObj.getServers()
    logger.addDebug(servers)
    return render_template("adminServer.html", ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Admin Servers", PageNameLower="admin/servers", userAuth=userAuth, Servers=servers)

@app.route('/deleteAccount', methods=['GET', 'POST'])
@login_required
def deleteAccount():
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the delete account page')
    else:
        logger.addInfo('User is not logged in and going to the delete account page')
    loggedUser = current_user
    if userAuth:
        if loggedUser == current_user:
            databaseObj.deleteUser(loggedUser.username)
            logout_user()
            flash('Account deleted', category='success')
            return redirect(url_for('index'))
        else:
            flash('You can only delete your own account', category='error')
            return redirect(url_for('index'))
    else:
        flash('You need to be logged in to delete your account', category='error')
        return redirect(url_for('index'))
    
@app.route('/deleteAccount/<id>')
@login_required
def deleteAccountAdmin(id):
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the delete account page')
        if not databaseObj.isAdmin(current_user.username):
            flash('You are not an admin', category='error')
            return redirect(url_for('index'))
    else:
        logger.addInfo('User is not logged in and going to the delete account page')
        return redirect(url_for('index'))
    if userAuth:
        databaseObj.deleteUser(id)
        flash('Account deleted', category='success')
        return redirect(url_for('adminAccounts'))
    else:
        flash('You need to be logged (and admin) in to delete an account', category='error')
        return redirect(url_for('index'))

@app.route('/setAdmin/<id>')
@login_required
def setAdminAdmin(id):
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the set admin page')
        if not databaseObj.isAdmin(current_user.username):
            flash('You are not an admin', category='error')
            return redirect(url_for('index'))
    else:
        logger.addInfo('User is not logged in and going to the set admin page')
        return redirect(url_for('index'))
    if userAuth:
        databaseObj.setAdmin(id)
        flash('Account set as admin', category='success')
        return redirect(url_for('adminAccounts'))
    else:
        flash('You need to be logged (and admin) in to set an account as admin', category='error')
        return redirect(url_for('index'))
    
@app.route('/unsetAdmin/<id>')
@login_required
def unsetAdminAdmin(id):
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the unset admin page')
        if not databaseObj.isAdmin(current_user.username):
            flash('You are not an admin', category='error')
            return redirect(url_for('index'))
    else:
        logger.addInfo('User is not logged in and going to the unset admin page')
        return redirect(url_for('index'))
    if userAuth:
        databaseObj.unsetAdmin(id)
        flash('Account unset as admin', category='success')
        return redirect(url_for('adminAccounts'))
    else:
        flash('You need to be logged (and admin) in to unset an account as admin', category='error')
        return redirect(url_for('index'))
    
@app.route('/deleteServerAdmin/<id>')
@login_required
def deleteServerAdmin(id):
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the delete server page')
        if not databaseObj.isAdmin(current_user.username):
            flash('You are not an admin', category='error')
            return redirect(url_for('index'))
    else:
        logger.addInfo('User is not logged in and going to the delete server page')
        return redirect(url_for('index'))
    if userAuth:
        if databaseObj.getServer(id)[4] != None:
            if databaseObj.deleteServer(id):
                flash('Server deleted', category='success')
                return redirect(url_for('adminServers'))
            else:
                stopDocker(id)
                if databaseObj.deleteServer(id):
                    flash('Server deleted', category='success')
                    return redirect(url_for('adminServers'))
                else:
                    flash('Error deleting server', category='error')
                    return redirect(url_for('adminServers'))
        else:
            flash('Error deleting server', category='error')
            return redirect(url_for('adminServers'))

@app.route('/dashboard')
@login_required
def dashboard():
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the dashboard page')
    else:
        logger.addInfo('User is not logged in and going to the dashboard page')
    loggedUser = current_user
    userServers = databaseObj.getServerByOwner(loggedUser.username)
    return render_template('dashboard.html', ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Dashboard", PageNameLower="dashboard", servers=userServers, loggedUser=loggedUser, userAuth=userAuth)

@app.route('/server/<id>', methods=['GET', 'POST'])
@login_required
def server(id):
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the server page')
    else:
        logger.addInfo('User is not logged in and going to the server page')
    loggedUser = current_user
    server = databaseObj.getServer(id)
    if server[2] != loggedUser.username:
        flash('You are not the owner of this server', category='error')
        return redirect(url_for('dashboard'))
    port = server[4]
    if port == None:
        port = "Server is not running"
    op = OpPlayerForm()
    whitelist = WhitelistPlayerForm()
    if op.validate_on_submit():
        if opPlayer(server[0], op.player1.data):
            flash('Player added as op', category='success')
            return redirect(url_for('server', id=id))
        else:
            flash('Player already op', category='error')
            return redirect(url_for('server', id=id))
    if whitelist.validate_on_submit():
        if addPlayerToWhitelist(server[0], whitelist.player2.data):
            flash('Player added to whitelist', category='success')
            return redirect(url_for('server', id=id))
        else:
            flash('Player already whitelisted', category='error')
            return redirect(url_for('server', id=id))
    return render_template('server.html', ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Server", PageNameLower="server", server=server, op=op, loggedUser=loggedUser, userAuth=userAuth, port=port, whitelist=whitelist)

@app.route('/createServer', methods=['GET', 'POST'])
@login_required
def createServer():
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the create server page')
    else:
        logger.addInfo('User is not logged in and going to the create server page')
    form = CreateServerForm()
    if form.validate_on_submit():
        if databaseObj.addServer(form.serverName.data, current_user.username, form.serverVersion.data):
            flash('Server created', category='success')
            server = databaseObj.getServerByName(form.serverName.data)
            return redirect(url_for('server', id=server[0]))
        else:
            flash('Server already exists', category='error')
            return redirect(url_for('createServer'))
    return render_template('createServer.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Create Server", PageNameLower="createserver", userAuth=userAuth)

@app.route('/deleteServer/<id>', methods=['GET', 'POST'])
@login_required
def deleteServer(id):
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the delete server page')
    else:
        logger.addInfo('User is not logged in and going to the delete server page')
    serverName = databaseObj.getServer(id)[1]
    if databaseObj.getServer(id)[2] != current_user.username:
        flash('You can only delete your own servers', category='error')
        return redirect(url_for('dashboard'))
    if databaseObj.deleteServer(id):
        flash('Server deleted', category='success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid server', category='error')
        return redirect(url_for('server', id=id))
    
@app.route('/startServer/<id>', methods=['GET', 'POST'])
@login_required
def startServer(id):
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the start server page')
    else:
        logger.addInfo('User is not logged in and going to the start server page')
    if databaseObj.getServer(id)[2] != current_user.username:
        flash('You can only start your own servers', category='error')
        return redirect(url_for('dashboard'))
    if databaseObj.isUserServerHasPort(current_user.username):
        flash('You can only have one server running at a time', category='error')
        return redirect(url_for('dashboard'))
    serverId = databaseObj.getServer(id)[0]
    portToOpen = ports.getFreePort()
    if portToOpen == None:
        flash('No ports available, try again later', category='error')
        return redirect(url_for('dashboard'))
    if startDocker(id=serverId,port=portToOpen,version=databaseObj.getServer(id)[3]):
        ports.addPort(portToOpen)
        databaseObj.updateServerPort(serverId, portToOpen)
        flash('Server started', category='success')
        return redirect(url_for('server', id=id))
    else:
        flash('Invalid server', category='error')
        return redirect(url_for('server', id=id))
    
@app.route('/stopServer/<id>', methods=['GET', 'POST'])
@login_required
def stopServer(id):
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the stop server page')
    else:
        logger.addInfo('User is not logged in and going to the stop server page')
    serverId = databaseObj.getServer(id)[0]
    if databaseObj.getServer(id)[2] != current_user.username:
        flash('You can only stop your own servers', category='error')
        return redirect(url_for('dashboard'))
    if stopDocker(id=serverId):
        ports.removePort(databaseObj.getServer(id)[4])
        databaseObj.updateServerPort(serverId, None)
        flash('Server stopped', category='success')
        return redirect(url_for('server', id=id))
    else:
        flash('Invalid server', category='error')
        return redirect(url_for('server', id=id))

@app.route('/api/server/<id>')
def apiServer(id):
    mcServer = MinecraftService(f"{id}hathermos", 25565)
    status = mcServer.status
    if status == False:
        return jsonify({"status": "offline"})
    else:
        return jsonify({"status": "online", "players": mcServer.getPlayers(), "playerCount": mcServer.getPlayerCount(), "maxPlayers": mcServer.getMaxPlayers()})

if __name__ == '__main__':
    debugBool = parseArgs()
    jsonConfig = ConfigService()
    flaskLog = logging.getLogger('werkzeug')
    flaskLog.disabled = True
    flask.cli.show_server_banner = lambda *args: None
    logger = Logger("logs.log",debugMode=debugBool)
    logger.addInfo("Starting program...")
    ports = PortsService("ports.json")
    databaseObj = DatabaseService("database.db")
    logger.addInfo("Utils loaded")
    createApp()
    buildCss()
    logger.addInfo("Web server started on port 8090")
    app.register_error_handler(404, ErrorHandler)
    app.run(port=8090, debug=False,host='0.0.0.0')
