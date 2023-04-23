from time import sleep
from utils.minecraft import MinecraftService
from utils.database import DatabaseService

def checkServer(serverList):
    """
    This method is used to check the server, if there is no player on the server, it will be stopped after 5 minutes
    """
    beforeShutdown = 5
    for server in serverList:
        serverId = server[0]
        port = server[1]
        serverObj = MinecraftService(f"{id}hathermos", port)
        players = serverObj.getPlayers()
        
        if not players:
            print(f"No players found on server {serverId}, shutting down in {beforeShutdown} minutes...")
            sleep(beforeShutdown * 60)  # Wait for 5 minutes before shutting down server
            players = serverObj.getPlayers()  # Check again if there are players after waiting
            if not players:
                print(f"Stopping server {serverId} as there are still no players...")
                serverObj.stopServer()
        else:
            print(f"Players found on server {serverId}, server will remain running.")


if __name__ == '__main__':
    databaseObj = DatabaseService("database.db")
    # Get a list of all the running servers from the database
    runningServers = databaseObj.getServerWithPorts()
    
    # Divide the servers into groups, with each group containing at most 1 server
    groupSize = 1
    serverGroups = [runningServers[i:i+groupSize] for i in range(0, len(runningServers), groupSize)]
    
    # Process each group of servers sequentially
    for serverGroup in serverGroups:
        checkServer(serverGroup)
