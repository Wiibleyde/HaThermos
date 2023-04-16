import json
import os

class ConfigService:
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