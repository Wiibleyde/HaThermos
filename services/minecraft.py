from mcstatus import JavaServer

class MinecraftService:
    def __init__(self, host, port):
        self.server = JavaServer(host, port)

    def getServerStatus(self):
        try:
            status = self.server.status()
            return status
        except:
            return False
        
    def getPlayers(self):
        try:
            players = self.server.query()
            return players.players.online
        except:
            return False
        
    def getPlayerCount(self):
        try:
            players = self.getPlayers()
            if players:
                return len(players)
            else:
                return 0
        except:
            return False
        
    def getMaxPlayers(self):
        try:
            status = self.server.status()
            return status.players.max
        except:
            return False
