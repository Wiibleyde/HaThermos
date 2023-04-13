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
from services.database import Database
from services.flaskform import LoginForm, RegisterForm, CreateServerForm, DeleteServerForm
from services.config import Config
from services.logger import Logger

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
    
def createDocker(version, name):
    logger.addDebug(f"Creating docker {name}...")
    try:
        image, logs = client.images.build(path=f"./data/server/{version}", tag=f"minecraft/{name}:latest")
        logger.addDebug(f"Creating docker {name}... Done")
        return image
    except Exception as e:
        logger.addError(f"Error creating docker {name}: {e}")

def getContainerIdByName(name):
    logger.addDebug(f"Getting container id of {name}...")
    try:
        container = client.containers.list()
        for i in container:
            if i.image == f"minecraft/{name}":
                logger.addDebug(f"Getting container id of {name}... Done")
                return i.id
        logger.addDebug(f"Getting container id of {name}... Done")
        return container[0].id
    except Exception as e:
        logger.addError(f"Error getting container id of {name}: {e}")

def startDocker(image, name, port):
    logger.addDebug(f"Starting docker {name}...")
    try:
        container = client.containers.run(image, detach=True, ports={25565: port}, image=f"minecraft/{name}:latest", name=f"{name}",volume=f"{name}:/data")
        logger.addDebug(f"Starting docker {name}... Done")
        return container
    except Exception as e:
        logger.addError(f"Error starting docker {name}: {e}")

def deleteDocker(name):
    logger.addDebug(f"Deleting docker {name}...")
    try:
        id = getContainerIdByName(name)
        logger.addDebug(f"Deleting docker {id}... Done")
        container = client.containers.get(id)
        container.stop()
        container.remove()
        logger.addDebug(f"Deleting docker {name}... Done")
    except Exception as e:
        logger.addError(f"Error deleting docker {name}: {e}")

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

@app.route('/server/<id>')
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
    if server[2] == loggedUser.username:
        return render_template('server.html', ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Server", PageNameLower="server", server=server, loggedUser=loggedUser, userAuth=userAuth)
    else:
        return redirect(url_for('dashboard'))
    

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
        if databaseObj.addServer(form.serverName.data, current_user.username, form.serverVersion.data, 255565, "/dev/null"):
            createDocker(form.serverVersion.data, form.serverName.data)
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
        deleteDocker(serverName)
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

if __name__ == '__main__':
    debugBool = parseArgs()
    jsonConfig = Config()
    flaskLog = logging.getLogger('werkzeug')
    flaskLog.disabled = True
    flask.cli.show_server_banner = lambda *args: None
    logger = Logger("logs.log",debugMode=debugBool)
    logger.addInfo("Starting program...")
    databaseObj = Database("database.db")
    logger.addInfo("Database loaded, building CSS...")
    createApp()
    buildCss()
    logger.addInfo("CSS built, starting server...")
    app.register_error_handler(404, ErrorHandler)
    app.run(port=8090, debug=False,host='0.0.0.0')
