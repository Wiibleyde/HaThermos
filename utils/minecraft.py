from mcstatus import JavaServer

class MinecraftService:
    def __init__(self, host, port):
        self.server = JavaServer(host, port)
        try:
            self.status = self.server.status()
        except:
            self.status = False
        
    def getPlayers(self):
        if self.status is not None:
            try:
                return [player.name for player in self.status.players.sample]
            except:
                return None
        else:
            return None
        
    def getPlayerCount(self):
        if self.status:
            return self.status.players.online
        
    def getMaxPlayers(self):
        if self.status:
            return self.status.players.max
