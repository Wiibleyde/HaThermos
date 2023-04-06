from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired
import flask.cli
import json
import os
import subprocess
import hashlib
import time
import logging
import sqlite3
import logging
import argparse
import docker

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

class Logger:
    def __init__(self,fileName:str,debugMode:bool):
        self.fileName = fileName
        self.debugMode = debugMode
        self.createFile()

    def createFile(self):
        if not os.path.exists(self.fileName):
            with open(self.fileName, 'w') as f:
                pass

    def addLog(self,message):
        with open(self.fileName, 'a') as f:
            f.write(f"{message}\n")
    
    def addDebug(self,message):
        strMessage = f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [DEBUG] {message}"
        if self.debugMode:
            print(strMessage)
        self.addLog(strMessage)

    def addInfo(self,message):
        strMessage = f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [INFO] {message}"
        print(strMessage)
        self.addLog(strMessage)

    def addWarning(self,message):
        strMessage = f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [WARNING] {message}"
        print(strMessage)
        self.addLog(strMessage)

    def addError(self,message):
        strMessage = f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [ERROR] {message}"
        print(strMessage)
        self.addLog(strMessage)

class Database:
    # server is database
    def __init__(self, fileName):
        self.fileName = fileName
        self.createDatabase()

    def createDatabase(self):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS servers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, owner TEXT, serverVersion TEXT, serverPort INTEGER, serverPath TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT, admin BOOLEAN)')
        conn.commit()
        conn.close()

    def addServer(self, name, owner, serverVersion, serverPort, serverPath):
        if self.testIfExist(name,owner):
            return False
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('INSERT INTO servers (name, owner, serverVersion, serverPort, serverPath) VALUES (?, ?, ?, ?, ?)', (name, owner, serverVersion, serverPort, serverPath))
        conn.commit()
        conn.close()
        return True

    def deleteServer(self, id):
        try:
            conn = sqlite3.connect(self.fileName)
            c = conn.cursor()
            c.execute('DELETE FROM servers WHERE id = ?', (id,))
            conn.commit()
            conn.close()
            return True
        except:
            return False

    def modifyServer(self, id, name, owner, serverVersion, serverPort, serverPath):
        try:
            conn = sqlite3.connect(self.fileName)
            c = conn.cursor()
            c.execute('UPDATE servers SET name = ?, owner = ?, serverVersion = ?, serverPort = ?, serverPath = ? WHERE id = ?', (name, owner, serverVersion, serverPort, serverPath, id))
            conn.commit()
            conn.close()
            return True
        except:
            return False

    def getServers(self):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers')
        servers = c.fetchall()
        conn.close()
        return servers
    
    def getServer(self, id):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE id = ?', (id,))
        server = c.fetchone()
        conn.close()
        return server
    
    def getServerByName(self, name):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE name = ?', (name,))
        server = c.fetchone()
        conn.close()
        return server
    
    def getServerByOwner(self, owner):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE owner = ?', (owner,))
        server = c.fetchall()
        conn.close()
        return server
    
    def getServerByPort(self, port):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE serverPort = ?', (port,))
        server = c.fetchone()
        conn.close()
        return server
    
    def getServerByPath(self, path):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE serverPath = ?', (path,))
        server = c.fetchone()
        conn.close()
        return server
    
    def getServerByVersion(self, version):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE serverVersion = ?', (version,))
        server = c.fetchone()
        conn.close()
        return server
    
    def testIfExist(self, name, owner):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE name = ? AND owner = ?', (name, owner))
        server = c.fetchone()
        conn.close()
        if server:
            return True
        else:
            return False
        
    def addAdmin(self, username, email, password):
        if self.testIfUserExist(username):
            return False
        hashPassword = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, email, password, admin) VALUES (?, ?, ?, ?)', (username, email, hashPassword, True))
        conn.commit()
        conn.close()
        return True
    
    def addUser(self, username, email, password):
        if self.testIfUserExist(username):
            return False
        hashPassword = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, email, password, admin) VALUES (?, ?, ?, ?)', (username, email, hashPassword, False))
        conn.commit()
        conn.close()
        return True
    
    def deleteUser(self, id):
        try:
            conn = sqlite3.connect(self.fileName)
            c = conn.cursor()
            c.execute('DELETE FROM users WHERE id = ?', (id,))
            conn.commit()
            conn.close()
            return True
        except:
            return False
        
    def modifyUser(self, id, username, email, password, admin):
        try:
            conn = sqlite3.connect(self.fileName)
            c = conn.cursor()
            c.execute('UPDATE users SET username = ?, email = ?, password = ?, admin = ? WHERE id = ?', (username, email, password, admin, id))
            conn.commit()
            conn.close()
            return True
        except:
            return False
        
    def getUsers(self):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users')
        users = c.fetchall()
        conn.close()
        return users
    
    def getUser(self, id):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE id = ?', (id,))
        user = c.fetchone()
        conn.close()
        return user
    
    def getUserByName(self, username):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        return user
    
    def getUserByEmail(self, email):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        return user
    
    def testIfUserExist(self, username):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        if user:
            return True
        else:
            return False
        
    def testIfUserExistByEmail(self, email):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        if user:
            return True
        else:
            return False
        
    def checkUser(self, data, password):
        if self.testIfUserExist(data):
            user = self.getUserByName(data)
        elif self.testIfUserExistByEmail(data):
            user = self.getUserByEmail(data)
        else:
            return False
        if user[3] == hashlib.sha256(password.encode()).hexdigest():
            return user
        else:
            return False

class Config:
    def __init__(self):
        self.fileName = 'serversConfig.json'
        if not os.path.exists(self.fileName):
            self.config = {"ProjectName":"HaThermos"}
            self.createFile()
            print('Config file created')
        else:
            self.loadConfig()
            
    def createFile(self):
        with open(self.fileName, 'w') as f:
            json.dump(self.config, f,indent=4)
            
    def loadConfig(self):
        with open(self.fileName, 'r') as f:
            self.config = json.load(f)
            
    def saveConfig(self):
        with open(self.fileName, 'w') as f:
            json.dump(self.config, f)
            
    def addConfig(self, key, value):
        self.config[key] = value
        self.saveConfig()
        
    def deleteConfig(self, key):
        del self.config[key]
        self.saveConfig()
        
    def modifyConfig(self, key, value):
        self.config[key] = value
        self.saveConfig()
        
    def getConfig(self, key):
        return self.config[key]

class LoginForm(FlaskForm):
    usernameOrEmail = StringField('usernameOrEmail', validators=[DataRequired()], render_kw={"placeholder": "Username/Email", "class": "text-black"})
    password = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Password", "type": "password", "class": "text-black"})
    submit = SubmitField('submit', render_kw={"value": "Login", "class": "text-white"})

class RegisterForm(FlaskForm):
    username = StringField('usernameOrEmail', validators=[DataRequired()], render_kw={"placeholder": "Username", "class": "text-black"})
    email = StringField('email', validators=[DataRequired()], render_kw={"placeholder": "Email", "class": "text-black"})
    password = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Password", "type": "password", "class": "text-black"})
    confirmPassword = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Confirm password", "type": "password", "class": "text-black"})
    submit = SubmitField('submit', render_kw={"value": "Register", "class": "text-white"})

class CreateServerForm(FlaskForm):
    serverName = StringField('serverName', validators=[DataRequired()])
    serverVersion = SelectField('serverVersion', choices=[('1.8.8', '1.8.8'), ('1.9.4', '1.9.4'), ('1.10.2', '1.10.2'), ('1.11.2', '1.11.2'), ('1.12.2', '1.12.2'), ('1.13.2', '1.13.2'), ('1.14.4', '1.14.4'), ('1.15.2', '1.15.2'), ('1.16.5', '1.16.5'), ('1.17.1', '1.17.1'), ('1.18.2', '1.18.2'), ('1.19.4','1.19.4')], validators=[DataRequired()])
    submit = SubmitField('submit', render_kw={"value": "Create"})

class DeleteServerForm(FlaskForm):
    serverName = StringField('serverName', validators=[DataRequired()])
    submit = SubmitField('submit', render_kw={"value": "Delete"})

def buildCss():
    logger.addDebug("Building CSS : downloading")
    subprocess.run(["npm","i"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logger.addDebug("Building CSS : downloading... Done")
    logger.addDebug("Building CSS : building")
    subprocess.run(["npx","tailwindcss", "-i", "./static/css/input.css", "-o", "./static/css/tailwind.css"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logger.addDebug("Building CSS : building... Done")

def parseArgs():
    parser = argparse.ArgumentParser(description="HaThermos Web Panel")
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    if args.debug:
        return True
    else:
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
    image, logs = client.images.build(path=f"./data/server/{version}", tag=f"minecraft:{name}")
    if logs:
        for log in logs:
            if log['stream']:
                logger.addDebug(log['stream'])
    logger.addDebug(f"Creating docker {name}... Done")
    return image

def deleteDocker(name):
    logger.addDebug(f"Deleting docker {name}...")
    client.images.remove(f"minecraft:{name}")
    logger.addDebug(f"Deleting docker {name}... Done")
    return True

def startDocker(name, port):
    logger.addDebug(f"Starting docker {name}...")
    container = client.containers.run(f"minecraft:{name}", detach=True, ports={f"{port}/tcp": port}, name=f"minecraft:{name}")
    logger.addDebug(f"Starting docker {name}... Done")
    return container

def stopDocker(name):
    logger.addDebug(f"Stopping docker {name}...")
    container = client.containers.get(f"minecraft:{name}")
    container.stop()
    logger.addDebug(f"Stopping docker {name}... Done")
    return container

def pauseDocker(name):
    logger.addDebug(f"Pausing docker {name}...")
    container = client.containers.get(f"minecraft:{name}")
    container.pause()
    logger.addDebug(f"Pausing docker {name}... Done")
    return container

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
    createDocker("1.8.8","testServer")
    startDocker("testServer")
    app.register_error_handler(404, ErrorHandler)
    app.run(port=5000, debug=False)
