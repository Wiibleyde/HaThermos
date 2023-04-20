import json

class PortsService:
    def __init__(self, filename):
        self.filename = filename
        self.possiblePorts = [25566,25567,25568,25569]
        self.usedPorts = []
        self.loadPorts()

    def loadPorts(self):
        try:
            with open(self.filename, 'r') as f:
                self.usedPorts = json.load(f)
        except:
            self.usedPorts = []

    def savePorts(self):
        with open(self.filename, 'w') as f:
            json.dump(self.usedPorts, f)

    def getPort(self):
        for port in self.possiblePorts:
            if port not in self.usedPorts:
                self.usedPorts.append(port)
                self.savePorts()
                return port
        return False
    
    def removePort(self, port):
        if port in self.usedPorts:
            self.usedPorts.remove(port)
            self.savePorts()
            return True
        return False
    
    def getPorts(self):
        return self.usedPorts
    
    def getFreePorts(self):
        freePorts = []
        for port in self.possiblePorts:
            if port not in self.usedPorts:
                freePorts.append(port)
        return freePorts
    
    def getFreePort(self):
        for port in self.possiblePorts:
            if port not in self.usedPorts:
                return port
        return False
    
    def addPort(self, port):
        if port not in self.usedPorts:
            self.usedPorts.append(port)
            self.savePorts()
            return True
        return False
    
    def getUsedPorts(self):
        usedPorts = []
        for port in self.possiblePorts:
            if port in self.usedPorts:
                usedPorts.append(port)
        return usedPorts
    
    def testIfPortIsUsed(self, port):
        if port in self.usedPorts:
            return True
        else:
            return False
        
    def testIfPortIsFree(self, port):
        if port not in self.usedPorts:
            return True
        else:
            return False
        