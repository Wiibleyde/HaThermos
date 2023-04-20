import os
import time

class Logger:
    def __init__(self,fileName:str,debugMode:bool):
        self.fileName = fileName
        self.debugMode = debugMode
        self.createFile()

    def createFile(self):
        if not os.path.exists(self.fileName):
            with open(self.fileName, 'w') as f:
                f.write(f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [INFO] Log file created")

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