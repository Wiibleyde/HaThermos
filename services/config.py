import json
import os

class ConfigService:
    """
    This class is used to manage the config file
    """
    def __init__(self):
        """
        Constructor of the class
        """        
        self.fileName = 'serversConfig.json'
        if not os.path.exists(self.fileName):
            self.config = {"ProjectName":"HaThermos"}
            self.createFile()
            print('Config file created')
        else:
            self.loadConfig()
            
    def createFile(self):
        """
        This method is used to create the config file
        """
        with open(self.fileName, 'w') as f:
            json.dump(self.config, f,indent=4)
            
    def loadConfig(self):
        """
        This method is used to load the config file
        """
        with open(self.fileName, 'r') as f:
            self.config = json.load(f)
            
    def saveConfig(self):
        """
        This method is used to save the config file
        """
        with open(self.fileName, 'w') as f:
            json.dump(self.config, f)
            
    def addConfig(self, key, value):
        """
        This method is used to add a new config to the config file

        Args:
            key (str): The key of the config
            value (str): The value of the config
        """
        self.config[key] = value
        self.saveConfig()
        
    def deleteConfig(self, key):
        """
        This method is used to delete a config from the config file

        Args:
            key (str): The key of the config
        """
        del self.config[key]
        self.saveConfig()
        
    def modifyConfig(self, key, value):
        """
        This method is used to modify a config from the config file

        Args:
            key (str): The key of the config
            value (str): The value of the config
        """
        self.config[key] = value
        self.saveConfig()
        
    def getConfig(self, key):
        """
        This method is used to get a config from the config file

        Args:
            key (str): The key of the config

        Returns:
            str: The value of the config
        """
        return self.config[key]