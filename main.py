from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import flask.cli
import subprocess
import logging
import logging
import argparse
import docker
import requests

# file import  
from services.database import DatabaseService
from utils.flaskform import LoginForm, RegisterForm, CreateServerForm, OpPlayerForm, DeopPlayerForm, WhitelistPlayerForm, UnwhitelistPlayerForm
from services.config import ConfigService
from utils.logger import Logger
from services.ports import PortsService

# ==============================================================================
# Environment variables 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ceciestunsecret'
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
    logger.addDebug("Building CSS : downloading")
    subprocess.run(["npm","i"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logger.addDebug("Building CSS : downloading... Done")
    logger.addDebug("Building CSS : building")
    subprocess.run(["npx","tailwindcss", "-i", "./static/css/input.css", "-o", "./static/css/tailwind.css"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
        # container = client.containers.run(image=f"itzg/minecraft-server", detach=True, ports={25565: port}, environment=["EULA=TRUE", f"VERSION={version}","MEMORY=2G","TYPE=PAPER","MOTD=HaThermos Server"], name=f"{id}hathermos", volumes={f"/srv/minecraft-data/{id}": {"bind": "/data", "mode": "rw"}})
        if version == '1.8.8' or version =='1.9.4' or version == '1.10.2' or version == '1.11.2' or version == '1.12.2' or version == '1.13.2' or version == '1.14.4' or version == '1.15.2' or version == '1.16.5' or version == '1.17.1':
            container = client.containers.run(image=f"itzg/minecraft-server:java8-graalvm-ce", detach=True, ports={25565: port}, environment=["EULA=TRUE", f"VERSION={version}","MEMORY=2G","TYPE=PAPER","MOTD=HaThermos Server","SPIGET_RESSOURCES=#327"], name=f"{id}hathermos", volumes={f"/srv/minecraft-data/{id}": {"bind": "/data", "mode": "rw"}})
        else:
            container = client.containers.run(image=f"itzg/minecraft-server:java17-graalvm-ce", detach=True, ports={25565: port}, environment=["EULA=TRUE", f"VERSION={version}","MEMORY=2G","TYPE=PAPER","MOTD=HaThermos Server","SPIGET_RESSOURCES=327"], name=f"{id}hathermos", volumes={f"/srv/minecraft-data/{id}": {"bind": "/data", "mode": "rw"}})
        logger.addDebug(f"Starting docker {id}... Done")
        return container
    except Exception as e:
        logger.addError(f"Error starting docker {id}: {e}")
        return False
    
def opPlayer(id,playerName):
    logger.addDebug(f"Op player {playerName} in docker {id}...")
    try:
        # cmd : docker exec 3hathermos mc-send-to-console "op player"
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
        # cmd : docker exec 3hathermos mc-send-to-console "deop player"
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
        # cmd : docker exec 3hathermos mc-send-to-console "whitelist add player"
        container = client.containers.get(f"{id}hathermos")
        container.exec_run(f"mc-send-to-console \"whitelist add {playerName}\"")
        logger.addDebug(f"Add player {playerName} to whitelist in docker {id}... Done")
        return True
    except Exception as e:
        logger.addError(f"Error add player {playerName} to whitelist in docker {id}: {e}")
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
        databaseObj.deleteUser(loggedUser.username)
        logout_user()
        flash('Account deleted', category='success')
        return redirect(url_for('index'))

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
    port = server[4]
    if port == None:
        port = "Server is not running"
    op = OpPlayerForm()
    whitelist = WhitelistPlayerForm()
    if op.validate_on_submit():
        if opPlayer(server[0], op.player.data):
            flash('Player added as op', category='success')
            return redirect(url_for('server', id=id))
        else:
            flash('Player already op', category='error')
            return redirect(url_for('server', id=id))
    if whitelist.validate_on_submit():
        if addPlayerToWhitelist(server[0], whitelist.player.data):
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
            return redirect(url_for('dashboard'))
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
    if databaseObj.deleteServer(id):
        flash('Server deleted', category='success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid server', category='error')
        return redirect(url_for('dashboard'))
    
@app.route('/startServer/<id>', methods=['GET', 'POST'])
@login_required
def startServer(id):
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
        logger.addInfo(f'User {current_user.username} is logged in and going to the start server page')
    else:
        logger.addInfo('User is not logged in and going to the start server page')
    serverId = databaseObj.getServer(id)[0]
    portToOpen = ports.getFreePort()
    if portToOpen == None:
        flash('No ports available, try again later', category='error')
        return redirect(url_for('dashboard'))
    if startDocker(id=serverId,port=portToOpen,version=databaseObj.getServer(id)[3]):
        ports.addPort(portToOpen)
        databaseObj.updateServerPort(serverId, portToOpen)
        flash('Server started', category='success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid server', category='error')
        return redirect(url_for('dashboard'))
    
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
    if stopDocker(id=serverId):
        ports.removePort(databaseObj.getServer(id)[4])
        databaseObj.updateServerPort(serverId, None)
        flash('Server stopped', category='success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid server', category='error')
        return redirect(url_for('dashboard'))
    
if __name__ == '__main__':
    debugBool = parseArgs()
    jsonConfig = ConfigService()
    flaskLog = logging.getLogger('werkzeug')
    flaskLog.disabled = True
    flask.cli.show_server_banner = lambda *args: None
    logger = Logger("logs.log",debugMode=debugBool)
    logger.addInfo("Starting program...")
    logger.addInfo("Loading config...")
    ports = PortsService("ports.json")
    logger.addInfo("Ports loaded, loading database...")
    databaseObj = DatabaseService("database.db")
    # databaseObj.addAdmin("Wiibleyde","nathan@bonnell.fr","WiiBleyde33!")
    logger.addInfo("Database loaded, building CSS...")
    createApp()
    buildCss()
    logger.addInfo("CSS built, starting server...")
    app.register_error_handler(404, ErrorHandler)
    app.run(port=8090, debug=False,host='0.0.0.0')
