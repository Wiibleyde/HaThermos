import json

class PortsService:
    """
    This class is used to manage the ports
    """
    def __init__(self, filename):
        """
        Constructor of the class

        Args:
            filename (str): The name of the file
        """
        self.filename = "data/"+filename
        self.possiblePorts = [25566,25567,25568,25569]
        self.usedPorts = []
        self.loadPorts()

    def loadPorts(self):
        """
        This method is used to load the ports
        """
        try:
            with open(self.filename, 'r') as f:
                self.usedPorts = json.load(f)
        except:
            self.usedPorts = []

    def savePorts(self):
        """
        This method is used to save the ports
        """
        with open(self.filename, 'w') as f:
            json.dump(self.usedPorts, f)

    def getPort(self):
        """
        This method is used to get a port

        Returns:
            int: The port
        """
        for port in self.possiblePorts:
            if port not in self.usedPorts:
                self.usedPorts.append(port)
                self.savePorts()
                return port
        return False
    
    def removePort(self, port):
        """
        This method is used to remove a port

        Args:
            port (int): The port

        Returns:
            bool: True if the port has been removed, False otherwise
        """
        if port in self.usedPorts:
            self.usedPorts.remove(port)
            self.savePorts()
            return True
        return False
    
    def getPorts(self):
        """
        This method is used to get the ports
        """
        return self.usedPorts
    
    def getFreePorts(self):
        """
        This method is used to get the free ports

        Returns:
            list: The free ports
        """
        freePorts = []
        for port in self.possiblePorts:
            if port not in self.usedPorts:
                freePorts.append(port)
        return freePorts
    
    def getFreePort(self):
        """
        This method is used to get a free port

        Returns:
            int: The free port
        """
        for port in self.possiblePorts:
            if port not in self.usedPorts:
                return port
        return False
    
    def addPort(self, port):
        """
        This method is used to add a port

        Args:
            port (int): The port

        Returns:
            bool: True if the port has been added, False otherwise
        """
        if port not in self.usedPorts:
            self.usedPorts.append(port)
            self.savePorts()
            return True
        return False
    
    def getUsedPorts(self):
        """
        This method is used to get the used ports

        Returns:
            list: The used ports
        """
        usedPorts = []
        for port in self.possiblePorts:
            if port in self.usedPorts:
                usedPorts.append(port)
        return usedPorts
    
    def testIfPortIsUsed(self, port):
        """
        This method is used to test if a port is used

        Args:
            port (int): The port

        Returns:
            bool: True if the port is used, False otherwise
        """
        if port in self.usedPorts:
            return True
        else:
            return False
        
    def testIfPortIsFree(self, port):
        """
        This method is used to test if a port is free

        Args:
            port (int): The port

        Returns:
            bool: True if the port is free, False otherwise
        """
        if port not in self.usedPorts:
            return True
        else:
            return False
        