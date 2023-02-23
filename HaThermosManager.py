from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired
import json
import os
import hashlib
from subprocess import run
import time

# ==============================================================================
# Environment variables 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
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
        print('AccountsStorer : init', end='\r')
        self.fileName = 'accounts.json'
        if not os.path.exists(self.fileName):
            print('AccountsStorer : createFile', end='\r')
            self.accounts = {}
            self.createFile()
        print('AccountsStorer : loadFile', end='\r')
        print('AccountsStorer : init done')

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

class Server:
    def __init__(self, fileName):
        print('Server : init', end='\r')
        self.fileName = fileName
        if not os.path.exists(self.fileName):
            print('Server : createFile', end='\r')
            self.server = {}
            self.createFile()
        else:
            print('Server : loadFile', end='\r')
            self.loadFile()
        print('Server : init done')

    def createFile(self):
        with open(self.fileName, 'w') as f:
            json.dump(self.server, f)

    def loadFile(self):
        with open(self.fileName, 'r') as f:
            self.server = json.load(f)

    def addServer(self, serverName, username):
        with open(self.fileName, 'r+') as f:
            self.server = json.load(f)
            if serverName in self.server:
                return False
            else:
                self.server[serverName] = username
                f.seek(0)
                json.dump(self.server, f)
                return True
            
    def deleteServer(self, serverName):
        with open(self.fileName, 'r+') as f:
            self.server = json.load(f)
            if serverName in self.server:
                del self.server[serverName]
                f.seek(0)
                json.dump(self.server, f)
                return True
            else:
                return False
            
    def modifyServer(self, serverName, username):
        with open(self.fileName, 'r+') as f:
            self.server = json.load(f)
            if serverName in self.server:
                self.server[serverName] = username
                f.seek(0)
                json.dump(self.server, f)
                return True
            else:
                return False
            
    def checkServer(self, serverName):
        with open(self.fileName, 'r') as f:
            self.server = json.load(f)
            if serverName in self.server:
                return True
            else:
                return False
            
    def getServer(self, serverName):
        with open(self.fileName, 'r') as f:
            self.server = json.load(f)
            if serverName in self.server:
                return self.server[serverName]
            else:
                return False
            
    def getServerList(self):
        with open(self.fileName, 'r') as f:
            self.server = json.load(f)
            return list(self.server.keys())
        
    def getServerListByUser(self, username):
        with open(self.fileName, 'r') as f:
            self.server = json.load(f)
            serverList = []
            for server in self.server:
                if self.server[server] == username:
                    serverList.append(server)
            return serverList

class Config:
    def __init__(self):
        self.fileName = 'serverConfig.json'
        if not os.path.exists(self.fileName):
            self.config = {}
            self.createFile()
        else:
            self.loadConfig()
            
    def createFile(self):
        with open(self.fileName, 'w') as f:
            json.dump(self.config, f)
            
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
    print("Building CSS : downloading", end="\r")
    run(["npm", "install", "-D", "tailwindcss"])
    print("Building CSS : downloading... Done")
    print("Building CSS : building", end="\r")
    run(["npx", "tailwindcss", "-i", "./static/css/input.css", "-o", "./static/css/tailwind.css"])
    time.sleep(1)
    if os.path.exists("./static/css/tailwind.css"):
        print("Building CSS : building... Done")
        time.sleep(1)
        return True
    else:
        print("Building CSS : building... Failed")
        time.sleep(1)
        return False

def createApp():
    print("Creating app...", end="\r")
    app = Flask(__name__)
    print("Creating app... Done")
    return app

def ErrorHandler(e):
    errorCode = e.code
    return render_template("error.html", ErrorCode=errorCode, ProjectName=jsonConfig.getConfig('ProjectName'))

@app.route('/')
def index():
    return render_template("index.html", ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Home", PageNameLower="home")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("form validated")
        if jsonAccounts.checkAccount(form.username.data, form.password.data):
            print("account exists")
            user = User(form.username.data)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            print("account does not exist")
            flash('Invalid username or password')
            return redirect(url_for('login'))
    else:
        print(form.errors)
    return render_template('login.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Login", PageNameLower="login")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if jsonAccounts.addAccount(form.username.data, form.password.data):
            flash('Account created', category='success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists', category='error')
            return redirect(url_for('register'))
    return render_template('register.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Register", PageNameLower="register")

@app.route('/deleteAccount', methods=['GET', 'POST'])
@login_required
def deleteAccount():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        if jsonAccounts.deleteAccount(form.username.data):
            return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('deleteAccount'))
    return render_template('deleteAccount.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Delete Account", PageNameLower="deleteaccount")

@app.route('/modifyAccount', methods=['GET', 'POST'])
@login_required
def modifyAccount():
    form = ModifyAccountForm()
    if form.validate_on_submit():
        if jsonAccounts.modifyAccount(form.username.data, form.newPassword.data):
            return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('modifyAccount'))
    return render_template('modifyAccount.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Modify Account", PageNameLower="modifyaccount")

@app.route('/dashboard')
@login_required
def dashboard():
    loggedUser = current_user
    print(loggedUser.username)
    print(jsonServers.getServerListByUser(loggedUser.username))
    return render_template('dashboard.html', ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Dashboard", PageNameLower="dashboard", servers=jsonServers.getServerListByUser(loggedUser.username), loggedUser=loggedUser.username)

@app.route('/createServer', methods=['GET', 'POST'])
@login_required
def createServer():
    form = CreateServerForm()
    if form.validate_on_submit():
        if jsonServers.addServer(form.serverName.data, current_user.username):
            return redirect(url_for('dashboard'))
        else:
            flash('Server already exists')
            return redirect(url_for('createServer'))
    return render_template('createServer.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'), PageName="Create Server", PageNameLower="createserver")

if __name__ == '__main__':
    jsonAccounts = AccountsStorer()
    jsonAccounts.addAccount('admin', 'admin')
    jsonConfig = Config()
    jsonServers = Server("servers.json")
    jsonServers.addServer("test", "nathan")
    # buildCss()
    createApp()
    app.register_error_handler(404, ErrorHandler)
    app.run(port=5000)