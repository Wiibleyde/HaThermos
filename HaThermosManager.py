from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired
import json
import os
import hashlib
import time
import logging
import sqlite3
import logging

# ==============================================================================
# Environment variables 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ceciestunsecret'
login_manager=LoginManager()
login_manager.init_app(app)
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

class AccountsStorer:
    def __init__(self):
        logger.addDebug('AccountsStorer : init')
        self.fileName = 'accounts.json'
        if not os.path.exists(self.fileName):
            logger.addDebug('AccountsStorer : createFile')
            self.accounts = {}
            self.createFile()
        logger.addDebug('AccountsStorer : loadFile')
        logger.addDebug('AccountsStorer : init done')

    def createFile(self):
        with open('accounts.json', 'w') as f:
            json.dump(self.accounts, f)

    def addAccount(self, username, password):
        with open(self.fileName, 'r+') as f:
            self.accounts = json.load(f)
            if username in self.accounts:
                return False
            else:
                encodedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
                self.accounts[username] = encodedPassword
                f.seek(0)
                json.dump(self.accounts, f)
                return True
            
    def checkAccount(self, username, password):
        with open(self.fileName, 'r') as f:
            self.accounts = json.load(f)
            if username in self.accounts:
                encodedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
                if self.accounts[username] == encodedPassword:
                    return True
                else:
                    return False
            else:
                return False
            
    def deleteAccount(self, username):
        with open(self.fileName, 'r+') as f:
            self.accounts = json.load(f)
            if username in self.accounts:
                del self.accounts[username]
                f.seek(0)
                json.dump(self.accounts, f)
                return True
            else:
                return False
            
    def modifyAccount(self, username, password):
        with open(self.fileName, 'r+') as f:
            self.accounts = json.load(f)
            if username in self.accounts:
                encodedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
                self.accounts[username] = encodedPassword
                f.seek(0)
                json.dump(self.accounts, f)
                return True
            else:
                return False
            
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

class Servers:
    # server is database
    def __init__(self, fileName):
        self.fileName = fileName
        self.createDatabase()

    def createDatabase(self):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS servers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, owner TEXT, serverVersion TEXT, serverPort INTEGER, serverPath TEXT)')
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

class Config:
    def __init__(self):
        self.fileName = 'serversConfig.json'
        if not os.path.exists(self.fileName):
            self.config = {"ProjectName":"HaThermos","DebugMode":True}
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
    username = StringField('username', validators=[DataRequired()], render_kw={"placeholder": "Username", "class": "text-black"})
    password = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Password", "type": "password", "class": "text-black"})
    submit = SubmitField('submit', render_kw={"value": "Login", "class": "text-white"})

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()], render_kw={"placeholder": "Username", "class": "text-black"})
    password = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Password", "type": "password", "class": "text-black"})
    confirmPassword = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Confirm password", "type": "password", "class": "text-black"})
    submit = SubmitField('submit', render_kw={"value": "Register", "class": "text-white"})

class DeleteAccountForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('submit', render_kw={"value": "Delete"})

class ModifyAccountForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    newPassword = StringField('newPassword', validators=[DataRequired()])
    submit = SubmitField('submit', render_kw={"value": "Modify"})

class CreateServerForm(FlaskForm):
    serverName = StringField('serverName', validators=[DataRequired()])
    serverVersion = SelectField('serverVersion', choices=[('1.8.8', '1.8.8'), ('1.9.4', '1.9.4'), ('1.10.2', '1.10.2'), ('1.11.2', '1.11.2'), ('1.12.2', '1.12.2'), ('1.13.2', '1.13.2'), ('1.14.4', '1.14.4'), ('1.15.2', '1.15.2'), ('1.16.5', '1.16.5'), ('1.17.1', '1.17.1'), ('1.18.2', '1.18.2'), ('1.19.3','1.19.3')], validators=[DataRequired()])
    submit = SubmitField('submit', render_kw={"value": "Create"})

class ModifyServerForm(FlaskForm):
    serverName = StringField('serverName', validators=[DataRequired()])
    serverVersion = SelectField('serverVersion', choices=[('1.8.8', '1.8.8'), ('1.9.4', '1.9.4'), ('1.10.2', '1.10.2'), ('1.11.2', '1.11.2'), ('1.12.2', '1.12.2'), ('1.13.2', '1.13.2'), ('1.14.4', '1.14.4'), ('1.15.2', '1.15.2'), ('1.16.5', '1.16.5'), ('1.17.1', '1.17.1'), ('1.18.2', '1.18.2'), ('1.19.3','1.19.3')], validators=[DataRequired()])
    serverGamemode = SelectField('serverGamemode', choices=[('survival', 'survival'), ('creative', 'creative'), ('adventure', 'adventure'), ('spectator', 'spectator')], validators=[DataRequired()])
    serverDifficulty = SelectField('serverDifficulty', choices=[('peaceful', 'peaceful'), ('easy', 'easy'), ('normal', 'normal'), ('hard', 'hard')], validators=[DataRequired()])
    serverPVP = SelectField('serverPVP', choices=[('true', 'true'), ('false', 'false')], validators=[DataRequired()])
    serverWhitelist = SelectField('serverWhitelist', choices=[('true', 'true'), ('false', 'false')], validators=[DataRequired()])
    serverMaxPlayers = IntegerField('serverMaxPlayers', validators=[DataRequired()])
    submit = SubmitField('submit', render_kw={"value": "Modify"})

class DeleteServerForm(FlaskForm):
    serverName = StringField('serverName', validators=[DataRequired()])
    submit = SubmitField('submit', render_kw={"value": "Delete"})

def buildCss():
    logger.addDebug("Building CSS : downloading")
    os.system("npm i --silent")
    logger.addDebug("Building CSS : downloading... Done")
    logger.addDebug("Building CSS : building")
    os.system("npx tailwindcss -i ./static/css/input.css -o ./static/css/tailwind.css --silent")
    logger.addDebug("Building CSS : building... Done")

def createApp():
    logger.addDebug("Creating app...")
    app = Flask(__name__)
    logger.addDebug("Creating app... Done")
    return app

def ErrorHandler(e):
    errorCode = e.code
    if errorCode == 404:
        flash('Page not found', category='error')
        return render_template("error.html", ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Error", PageNameLower="error", userAuth=False), 404
    else:
        flash('An error occured', category='error')
        return render_template("error.html", ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Error", PageNameLower="error", userAuth=False), 500

@app.route('/')
def index():
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
    return render_template("index.html", ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Home", PageNameLower="home", userAuth=userAuth)

@app.route('/about')
def about():
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
    return render_template("about.html", ProjectName=jsonConfig.getConfig('ProjectName'), PageName="About", PageNameLower="about", userAuth=userAuth)

@app.route('/contact')
def contact():
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
    return render_template("contact.html", ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Contact", PageNameLower="contact", userAuth=userAuth)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
    if form.validate_on_submit():
        if jsonAccounts.checkAccount(form.username.data, form.password.data):
            user = User(form.username.data)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', category='error')
            return redirect(url_for('login'))
    else:
        logger.addError(form.errors)
    return render_template('login.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Login", PageNameLower="login", userAuth=userAuth)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', category='success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
    if form.validate_on_submit():
        if form.confirmPassword.data == form.password.data:
            if jsonAccounts.addAccount(form.username.data, form.password.data):
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
    form = DeleteAccountForm()
    if form.validate_on_submit():
        if jsonAccounts.deleteAccount(form.username.data):
            return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('deleteAccount'))
    return render_template('deleteAccount.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Delete Account", PageNameLower="deleteaccount", userAuth=userAuth)

@app.route('/modifyAccount', methods=['GET', 'POST'])
@login_required
def modifyAccount():
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
    form = ModifyAccountForm()
    if form.validate_on_submit():
        if jsonAccounts.modifyAccount(form.username.data, form.newPassword.data):
            return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('modifyAccount'))
    return render_template('modifyAccount.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Modify Account", PageNameLower="modifyaccount", userAuth=userAuth)

@app.route('/dashboard')
@login_required
def dashboard():
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
    loggedUser = current_user
    userServers = servers.getServerByOwner(loggedUser.username)
    return render_template('dashboard.html', ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Dashboard", PageNameLower="dashboard", servers=userServers, loggedUser=loggedUser, userAuth=userAuth)

@app.route('/server/<id>')
@login_required
def server(id):
    userAuth = False
    if current_user.is_authenticated:
        userAuth = True
    loggedUser = current_user
    server = servers.getServer(id)
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
    form = CreateServerForm()
    if form.validate_on_submit():
        if servers.addServer(form.serverName.data, current_user.username, form.serverVersion.data, 255565, "/dev/null"):
            flash('Server created', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Server already exists', category='error')
            return redirect(url_for('createServer'))
    return render_template('createServer.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Create Server", PageNameLower="createserver", userAuth=userAuth)

@app.route('/deleteServer/<id>', methods=['GET', 'POST'])
@login_required
def deleteServer(id):
    if servers.deleteServer(id):
        flash('Server deleted', category='success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid server', category='error')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    jsonConfig = Config()
    flaskLog = logging.getLogger('werkzeug')
    flaskLog.disabled = True
    # osLog = logging.getLogger('os')
    # osLog.disabled = True
    logger = Logger("logs.log",jsonConfig.getConfig("DebugMode"))
    jsonAccounts = AccountsStorer()
    jsonAccounts.addAccount('admin', 'admin')
    jsonConfig = Config()
    servers = Servers("server.db")
    createApp()
    buildCss()
    app.register_error_handler(404, ErrorHandler)
    app.run(port=5000, debug=True)
    