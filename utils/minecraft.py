from mcstatus import JavaServer

class MinecraftService:
    """
    MinecraftService class
    """
    def __init__(self, host, port):
        """
        Constructor of the class

        Args:
            host (str): The host of the server
            port (int): The port of the server
        """
        self.server = JavaServer(host, port)
        try:
            self.status = self.server.status()
        except:
            self.status = False
        
    def getPlayers(self):
        """
        This method is used to get the players of the server

        Returns:
            list: The list of the players
        """
        if self.status is not None:
            try:
                return [player.name for player in self.status.players.sample]
            except:
                return None
        else:
            return None
        
    def getPlayerCount(self):
        """
        This method is used to get the player count of the server

        Returns:
            int: The player count
        """
        if self.status:
            return self.status.players.online
        
    def getMaxPlayers(self):
        """
        This method is used to get the max players of the server

        Returns:
            int: The max players
        """
        if self.status:
            return self.status.players.max
