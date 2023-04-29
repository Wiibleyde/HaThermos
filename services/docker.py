import docker

class DockerService:
    """
    Service to manage docker containers
    """
    def __init__(self):
        """
        Constructor of the class
        """
        self.client = docker.from_env()

    def startDocker(self,version, id, port):
        """
        This method is used to start a docker container

        Args:
            version (str): The version of the server
            id (str): The id of the server
            port (int): The port of the server

        Returns:
            bool: True if the container is started, False if not
        """
        try:
            if version == '1.8.8' or version =='1.9.4' or version == '1.10.2' or version == '1.11.2' or version == '1.12.2' or version == '1.13.2' or version == '1.14.4' or version == '1.15.2' or version == '1.16.5' or version == '1.17.1':
                self.client.containers.run(image=f"itzg/minecraft-server:java8-graalvm-ce", detach=True, ports={25565: port}, environment=["EULA=TRUE", f"VERSION={version}","MEMORY=2G","TYPE=PAPER","MOTD=HaThermos Server","SPIGET_RESSOURCES=#327","ENABLE_COMMAND_BLOCK=true","ENABLE_QUERY=true","MAX_PLAYERS=15","ENABLE_WHITELIST=true","ICON=https://hathermos.bonnell.fr/static/assets/HaThermos.png","OVERRIDE_ICON=true"], name=f"{id}hathermos", network="hathermos_net", volumes={f"/var/hathermos/minecraft-data/{id}": {"bind": "/data", "mode": "rw"}})
            else:
                self.client.containers.run(image=f"itzg/minecraft-server:java17-graalvm-ce", detach=True, ports={25565: port}, environment=["EULA=TRUE", f"VERSION={version}","MEMORY=2G","TYPE=PAPER","MOTD=HaThermos Server","SPIGET_RESSOURCES=#327","ENABLE_COMMAND_BLOCK=true","ENABLE_QUERY=true","MAX_PLAYERS=15","ENABLE_WHITELIST=true","ICON=https://hathermos.bonnell.fr/static/assets/HaThermos.png","OVERRIDE_ICON=true"], name=f"{id}hathermos", network="hathermos_net", volumes={f"/var/hathermos/minecraft-data/{id}": {"bind": "/data", "mode": "rw"}})
            return True
        except Exception:
            return False
        
    def opPlayer(self,id,playerName):
        """
        This method is used to op a player

        Args:
            id (str): The id of the server
            playerName (str): The name of the player

        Returns:
            bool: True if the player is op, False if not
        """
        try:
            container = self.client.containers.get(f"{id}hathermos")
            container.exec_run(f"mc-send-to-console \"op {playerName}\"")
            return True
        except Exception:
            return False
        
    def deopPlayer(self,id,playerName):
        """
        This method is used to deop a player

        Args:
            id (str): The id of the server
            playerName (str): The name of the player

        Returns:
            bool: True if the player is deop, False if not
        """
        try:
            container = self.client.containers.get(f"{id}hathermos")
            container.exec_run(f"mc-send-to-console \"deop {playerName}\"")
            return True
        except Exception:
            return False
        
    def addPlayerToWhitelist(self,id,playerName):
        """
        This method is used to add a player to the whitelist

        Args:
            id (str): The id of the server
            playerName (str): The name of the player

        Returns:
            bool: True if the player is added to the whitelist, False if not
        """
        try:
            container = self.client.containers.get(f"{id}hathermos")
            container.exec_run(f"mc-send-to-console \"whitelist add {playerName}\"")
            return True
        except Exception:
            return False

    def removePlayerFromWhitelist(self,id,playerName):
        """
        This method is used to remove a player from the whitelist

        Args:
            id (str): The id of the server
            playerName (str): The name of the player

        Returns:
            bool: True if the player is removed from the whitelist, False if not
        """
        try:
            container = self.client.containers.get(f"{id}hathermos")
            container.exec_run(f"mc-send-to-console \"whitelist remove {playerName}\"")
            return True
        except Exception:
            return False
        
    def enableWhitelist(self,id):
        """
        This method is used to enable the whitelist

        Args:
            id (str): The id of the server

        Returns:
            bool: True if the whitelist is enabled, False if not
        """
        try:
            container = self.client.containers.get(f"{id}hathermos")
            container.exec_run(f"mc-send-to-console \"whitelist on\"")
            return True
        except Exception:
            return False

    def stopDocker(self,id):
        """
        This method is used to stop a docker container

        Args:
            id (str): The id of the server

        Returns:
            bool: True if the container is stopped, False if not
        """
        try:
            container = self.client.containers.get(f"{id}hathermos")
            container.stop()
            container.remove()
            return True
        except Exception:
            return False