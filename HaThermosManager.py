from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired
import json
import os
import hashlib

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

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

class AccountsStorer:
    def __init__(self):
        self.fileName = 'accounts.json'
        if not os.path.exists(self.fileName):
            self.accounts = {}
            self.createFile()

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
    def __init__(self, serverName, serverVersion):
        self.serverName = serverName
        self.serverVersion = serverVersion
        self.fileName = 'serverUsers.json'
        if not os.path.exists(self.fileName):
            self.serverUsers = {}
            self.createFile()

    def createFile(self):
        with open(self.fileName, 'w') as f:
            json.dump(self.serverUsers, f)

    def addServerUser(self, username, password):
        with open(self.fileName, 'r+') as f:
            self.serverUsers = json.load(f)
            if username in self.serverUsers:
                return False
            else:
                encodedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
                self.serverUsers[username] = encodedPassword
                f.seek(0)
                json.dump(self.serverUsers, f)
                return True
            
    def checkServerUser(self, username, password):
        with open(self.fileName, 'r') as f:
            self.serverUsers = json.load(f)
            if username in self.serverUsers:
                encodedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
                if self.serverUsers[username] == encodedPassword:
                    return True
                else:
                    return False
            else:
                return False
            
    def deleteServerUser(self, username):
        with open(self.fileName, 'r+') as f:
            self.serverUsers = json.load(f)
            if username in self.serverUsers:
                del self.serverUsers[username]
                f.seek(0)
                json.dump(self.serverUsers, f)
                return True
            else:
                return False
            
    def modifyServerUser(self, username, password):
        with open(self.fileName, 'r+') as f:
            self.serverUsers = json.load(f)
            if username in self.serverUsers:
                encodedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
                self.serverUsers[username] = encodedPassword
                f.seek(0)
                json.dump(self.serverUsers, f)
                return True
            else:
                return False

class ServerConfig:
    def __init__(self, serverName, serverVersion):
        self.serverName = serverName
        self.serverVersion = serverVersion
        self.fileName = 'serverConfig.json'
        if not os.path.exists(self.fileName):
            self.config = {}
            self.createFile()

    def createFile(self):
        with open(self.fileName, 'w') as f:
            json.dump(self.config, f)

    def addConfig(self, key, value):
        with open(self.fileName, 'r+') as f:
            self.config = json.load(f)
            if key in self.config:
                return False
            else:
                self.config[key] = value
                f.seek(0)
                json.dump(self.config, f)
                return True
            
    def deleteConfig(self, key):
        with open(self.fileName, 'r+') as f:
            self.config = json.load(f)
            if key in self.config:
                del self.config[key]
                f.seek(0)
                json.dump(self.config, f)
                return True
            else:
                return False
            
    def modifyConfig(self, key, value):
        with open(self.fileName, 'r+') as f:
            self.config = json.load(f)
            if key in self.config:
                self.config[key] = value
                f.seek(0)
                json.dump(self.config, f)
                return True
            else:
                return False

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
    username = StringField('username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Password", "type": "password"})
    submit = SubmitField('submit', render_kw={"value": "Login"})

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

class DeleteAccountForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

class ModifyAccountForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    newPassword = StringField('newPassword', validators=[DataRequired()])

class CreateServer(FlaskForm):
    serverName = StringField('serverName', validators=[DataRequired()])
    serverVersion = SelectField('serverVersion', choices=[('1.8.8', '1.8.8'), ('1.9.4', '1.9.4'), ('1.10.2', '1.10.2'), ('1.11.2', '1.11.2'), ('1.12.2', '1.12.2'), ('1.13.2', '1.13.2'), ('1.14.4', '1.14.4'), ('1.15.2', '1.15.2'), ('1.16.5', '1.16.5'), ('1.17.1', '1.17.1'), ('1.18.2', '1.18.2'), ('1.19.3','1.19.3')], validators=[DataRequired()])

class ModifyServer(FlaskForm):
    serverName = StringField('serverName', validators=[DataRequired()])
    serverVersion = SelectField('serverVersion', choices=[('1.8.8', '1.8.8'), ('1.9.4', '1.9.4'), ('1.10.2', '1.10.2'), ('1.11.2', '1.11.2'), ('1.12.2', '1.12.2'), ('1.13.2', '1.13.2'), ('1.14.4', '1.14.4'), ('1.15.2', '1.15.2'), ('1.16.5', '1.16.5'), ('1.17.1', '1.17.1'), ('1.18.2', '1.18.2'), ('1.19.3','1.19.3')], validators=[DataRequired()])
    serverGamemode = SelectField('serverGamemode', choices=[('survival', 'survival'), ('creative', 'creative'), ('adventure', 'adventure'), ('spectator', 'spectator')], validators=[DataRequired()])
    serverDifficulty = SelectField('serverDifficulty', choices=[('peaceful', 'peaceful'), ('easy', 'easy'), ('normal', 'normal'), ('hard', 'hard')], validators=[DataRequired()])

class DeleteServer(FlaskForm):
    serverName = StringField('serverName', validators=[DataRequired()])

def createApp():
    app = Flask(__name__)
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
        if jsonAccounts.checkAccount(form.username.data, form.password.data):
            user = User(form.username.data)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    else:
        print(form.errors)
    return render_template('login.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'))

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
            return redirect(url_for('login'))
        else:
            flash('Username already exists')
            return redirect(url_for('register'))
    return render_template('register.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'))

@app.route('/deleteAccount', methods=['GET', 'POST'])
def deleteAccount():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        if jsonAccounts.deleteAccount(form.username.data):
            return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('deleteAccount'))
    return render_template('deleteAccount.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'))

@app.route('/modifyAccount', methods=['GET', 'POST'])
def modifyAccount():
    form = ModifyAccountForm()
    if form.validate_on_submit():
        if jsonAccounts.modifyAccount(form.username.data, form.newPassword.data):
            return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('modifyAccount'))
    return render_template('modifyAccount.html', form=form, ProjectName=jsonConfig.getConfig('ProjectName'))

if __name__ == '__main__':
    jsonAccounts = AccountsStorer()
    jsonAccounts.addAccount('admin', 'admin')
    jsonConfig = Config()
    createApp()
    app.register_error_handler(404, ErrorHandler)
    app.run(port=5000)