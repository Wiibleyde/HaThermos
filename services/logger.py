import os
import time

class Logger:
    """
    This class is used to manage the log file
    """
    def __init__(self,fileName:str,debugMode:bool):
        """
        The constructor of the class

        Args:
            fileName (str): Name of the log file
            debugMode (bool): If the debug mode is enabled
        """
        self.fileName = "data/"+fileName
        self.debugMode = debugMode
        self.createFile()

    def createFile(self):
        """
        This method is used to create the log file
        """
        if not os.path.exists(self.fileName):
            with open(self.fileName, 'w') as f:
                f.write(f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [INFO] Log file created")

    def addLog(self,message):
        """
        This method is used to add a new log to the log file

        Args:
            message (str): The message of the log
        """
        with open(self.fileName, 'a') as f:
            f.write(f"{message}\n")
    
    def addDebug(self,message):
        """
        This method is used to add a new debug log to the log file

        Args:
            message (str): The message of the log
        """
        strMessage = f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [DEBUG] {message}"
        if self.debugMode:
            print(strMessage)
        self.addLog(strMessage)

    def addInfo(self,message):
        """
        This method is used to add a new info log to the log file

        Args:
            message (str): The message of the log
        """
        strMessage = f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [INFO] {message}"
        print(strMessage)
        self.addLog(strMessage)

    def addWarning(self,message):
        """
        This method is used to add a new warning log to the log file

        Args:
            message (str): The message of the log
        """
        strMessage = f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [WARNING] {message}"
        print(strMessage)
        self.addLog(strMessage)

    def addError(self,message):
        """
        This method is used to add a new error log to the log file

        Args:
            message (str): The message of the log
        """
        strMessage = f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [ERROR] {message}"
        print(strMessage)
        self.addLog(strMessage)