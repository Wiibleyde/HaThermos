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
            return [{'name': player.name, 'uuid': player.id} for player in self.server.players().sample]
        except:
            return False
        
    def getPlayerCount(self):
        try:
            players = self.server.players()
            return players.online
        except:
            return False
        
    def getMaxPlayers(self):
        try:
            players = self.server.players()
            return players.max
        except:
            return False