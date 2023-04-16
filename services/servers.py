import os
import json

class Servers:
    def __init__(self, filename):
        self.filename = filename
        self.possiblePorts = [25566, 25567, 25568, 25569]
        
    def createFile(self):
        if not os.path.exists(self.filename):
            # create an empty JSON object and write it to the file
            with open(self.filename, 'w') as f:
                json.dump({}, f, indent=4)

    def loadServers(self):
        self.createFile()
        with open(self.filename, 'r') as f:
            return json.load(f)
        
    def addRunningServer(self, serverName, port):
        servers = self.loadServers()
        servers[serverName] = port
        with open(self.filename, 'w') as f:
            json.dump(servers, f, indent=4)

    def removeRunningServer(self, serverName):
        servers = self.loadServers()
        if serverName in servers:
            del servers[serverName]
            with open(self.filename, 'w') as f:
                json.dump(servers, f, indent=4)
            return True
        return False
    
    def getRunningServers(self):
        servers = self.loadServers()
        return servers
    
    def getRunningServer(self, serverName):
        servers = self.loadServers()
        if serverName in servers:
            return (serverName, servers[serverName])
        return False
    
    def getRunningServerPort(self, serverName):
        servers = self.loadServers()
        if serverName in servers:
            return servers[serverName]
        return False
    
    def getRunningServerNames(self):
        servers = self.loadServers()
        return list(servers.keys())
    
    def getRunningServerPorts(self):
        servers = self.loadServers()
        return list(servers.values())
    
    def getRunningServerNamesAndPorts(self):
        servers = self.loadServers()
        return servers
    
    def isPortUsed(self, port):
        servers = self.loadServers()
        return port in servers.values()
    
    def getFreePorts(self):
        usedPorts = self.getUsedPorts()
        return list(set(self.possiblePorts) - set(usedPorts))
    
    def getFreePort(self):
        freePorts = self.getFreePorts()
        if freePorts:
            return freePorts[0]
        return False
    
    def getUsedPorts(self):
        servers = self.loadServers()
        return list(servers.values())
    
    def getUsedPort(self):
        usedPorts = self.getUsedPorts()
        if usedPorts:
            return usedPorts[0]
        return False
    
    def getPort(self, port):
        if port in self.possiblePorts and not self.isPortUsed(port):
            return port
        return False
