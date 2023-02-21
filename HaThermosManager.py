from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from flask_wtf import FlaskForm
# from wtforms import StringField
# from wtforms.validators import DataRequired
import json
import os
import hashlib

# ==============================================================================
# Environment variables 
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'neledispas'
# login_manager=LoginManager()
# login_manager.init_app(app)
# ==============================================================================

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
            
def createApp():
    app = Flask(__name__)
    return app

def ErrorHandler(e):
    errorCode = e.code
    return render_template("error.html", ErrorCode=errorCode, ProjectName=jsonConfig.getConfig('ProjectName'))

if __name__ == '__main__':
    jsonAccounts = AccountsStorer()
    jsonConfig = Config()
    createApp()
    app.register_error_handler(404, ErrorHandler)
    app.run(host='0.0.0.0', port=80, debug=True)