import sqlite3
import hashlib

class DatabaseService:
    """
    This class is used to manage the database
    """
    def __init__(self, fileName):
        """
        Constructor of the class

        Args:
            fileName (str): Name of the database file
        """
        self.fileName = "data/"+fileName
        self.createDatabase()

    def createDatabase(self):
        """
        This method is used to create the database
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS servers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, owner TEXT, serverVersion TEXT, serverPort INTEGER)')
        c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT, admin BOOLEAN)')
        conn.commit()
        conn.close()

    def addServer(self, name, owner, serverVersion):
        """
        This method is used to add a new server to the database

        Args:
            name (str): The name of the server
            owner (str): The owner of the server
            serverVersion (str): The version of the server

        Returns:
            bool: True if the server has been added, False if not
        """
        if self.testIfExist(name,owner):
            return False
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('INSERT INTO servers (name, owner, serverVersion) VALUES (?, ?, ?)', (name, owner, serverVersion))
        conn.commit()
        conn.close()
        return True

    def deleteServer(self, id):
        """
        This method is used to delete a server from the database

        Args:
            id (int): The id of the server

        Returns:
            bool: True if the server has been deleted, False if not
        """
        try:
            conn = sqlite3.connect(self.fileName)
            c = conn.cursor()
            c.execute('DELETE FROM servers WHERE id = ?', (id,))
            conn.commit()
            conn.close()
            return True
        except:
            return False

    def modifyServer(self, id, name, owner, serverVersion, serverPort, serverPath):
        """
        This method is used to modify a server from the database

        Args:
            id (int): The id of the server
            name (str): The name of the server
            owner (str): The owner of the server
            serverVersion (str): The version of the server
            serverPort (int): The port of the server
            serverPath (str): The path of the server

        Returns:
            bool: True if the server has been modified, False if not
        """
        try:
            conn = sqlite3.connect(self.fileName)
            c = conn.cursor()
            c.execute('UPDATE servers SET name = ?, owner = ?, serverVersion = ?, serverPort = ?, serverPath = ? WHERE id = ?', (name, owner, serverVersion, serverPort, serverPath, id))
            conn.commit()
            conn.close()
            return True
        except:
            return False

    def getServers(self):
        """
        This method is used to get all the servers from the database

        Args:
            id (int): The id of the server

        Returns:
            list: A list of servers
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers')
        servers = c.fetchall()
        conn.close()
        return servers
    
    def getServer(self, id):
        """
        This method is used to get a server from the database

        Args:
            id (int): The id of the server

        Returns:
            list: A list of servers
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE id = ?', (id,))
        server = c.fetchone()
        conn.close()
        return server
    
    def getServerByName(self, name):
        """
        This method is used to get a server from the database

        Args:
            name (str): The name of the server

        Returns:
            list: A list of servers
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE name = ?', (name,))
        server = c.fetchone()
        conn.close()
        return server
    
    def getServerByOwner(self, owner):
        """
        This method is used to get a server from the database

        Args:
            owner (str): The owner of the server

        Returns:
            list: A list of servers
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE owner = ?', (owner,))
        server = c.fetchall()
        conn.close()
        return server
    
    def getServerByVersion(self, version):
        """
        This method is used to get a server from the database

        Args:
            version (str): The version of the server

        Returns:
            list: A list of servers
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE serverVersion = ?', (version,))
        server = c.fetchone()
        conn.close()
        return server
    
    def testIfExist(self, name, owner):
        """
        This method is used to test if a server exist in the database

        Args:
            name (str): The name of the server
            owner (str): The owner of the server

        Returns:
            bool: True if the server exist, False if not
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE name = ? AND owner = ?', (name, owner))
        server = c.fetchone()
        conn.close()
        if server:
            return True
        else:
            return False
        
    def addAdmin(self, username, email, password):
        """
        This method is used to add a new admin to the database

        Args:
            username (str): The username of the admin
            email (str): The email of the admin
            password (str): The password of the admin

        Returns:
            bool: True if the admin has been added, False if not
        """
        if self.testIfUserExist(username):
            return False
        hashPassword = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, email, password, admin) VALUES (?, ?, ?, ?)', (username, email, hashPassword, True))
        conn.commit()
        conn.close()
        return True
    
    def isAdmin(self, username):
        """
        This method is used to test if a user is admin

        Args:
            username (str): The username of the user

        Returns:
            bool: True if the user is admin, False if not
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND admin = ?', (username, True))
        user = c.fetchone()
        conn.close()
        if user:
            return True
        else:
            return False
        
    def setAdmin(self, id):
        """
        This method is used to set a user as admin
        
        Args:
            id (int): The id of the user
            
        Returns:
            bool: True if the user has been set as admin, False if not
        """
        try:
            conn = sqlite3.connect(self.fileName)
            c = conn.cursor()
            c.execute('UPDATE users SET admin = ? WHERE id = ?', (True, id))
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def unsetAdmin(self, id):
        try:
            conn = sqlite3.connect(self.fileName)
            c = conn.cursor()
            c.execute('UPDATE users SET admin = ? WHERE id = ?', (False, id))
            conn.commit()
            conn.close()
            return True
        except:
            return False

    def addUser(self, username, email, password):
        """
        This method is used to add a new user to the database

        Args:
            username (str): The username of the user
            email (str): The email of the user
            password (str): The password of the user

        Returns:
            bool: True if the user has been added, False if not
        """
        if self.testIfUserExist(username):
            return False
        hashPassword = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, email, password, admin) VALUES (?, ?, ?, ?)', (username, email, hashPassword, False))
        conn.commit()
        conn.close()
        return True
    
    def deleteUser(self, id):
        """
        This method is used to delete a user from the database

        Args:
            id (int): The id of the user

        Returns:
            bool: True if the user has been deleted, False if not
        """
        try:
            conn = sqlite3.connect(self.fileName)
            c = conn.cursor()
            c.execute('DELETE FROM users WHERE id = ?', (id,))
            conn.commit()
            conn.close()
            return True
        except:
            return False
        
    def modifyUser(self, id, username, email, password, admin):
        """
        This method is used to modify a user from the database

        Args:
            id (int): The id of the user
            username (str): The username of the user
            email (str): The email of the user
            password (str): The password of the user
            admin (bool): True if the user is admin, False if not

        Returns:
            bool: True if the user has been modified, False if not
        """
        try:
            conn = sqlite3.connect(self.fileName)
            c = conn.cursor()
            c.execute('UPDATE users SET username = ?, email = ?, password = ?, admin = ? WHERE id = ?', (username, email, password, admin, id))
            conn.commit()
            conn.close()
            return True
        except:
            return False
        
    def getUsers(self):
        """
        This method is used to get all users from the database

        Returns:
            list: A list of all users
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users')
        users = c.fetchall()
        conn.close()
        return users
    
    def getUser(self, id):
        """
        This method is used to get a user from the database

        Args:
            id (int): The id of the user

        Returns:
            tuple: A tuple containing the user
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE id = ?', (id,))
        user = c.fetchone()
        conn.close()
        return user
    
    def getUserByName(self, username):
        """
        This method is used to get a user from the database

        Args:
            username (str): The username of the user

        Returns:
            tuple: A tuple containing the user
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        return user
    
    def getUserByEmail(self, email):
        """
        This method is used to get a user from the database

        Args:
            email (str): The email of the user

        Returns:
            tuple: A tuple containing the user
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        return user
    
    def testIfUserExist(self, username):
        """
        This method is used to test if a user exist in the database

        Args:
            username (str): The username of the user

        Returns:
            bool: True if the user exist, False if not
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        if user:
            return True
        else:
            return False
        
    def testIfUserExistByEmail(self, email):
        """
        This method is used to test if a user exist in the database

        Args:
            email (str): The email of the user

        Returns:
            bool: True if the user exist, False if not
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        if user:
            return True
        else:
            return False
        
    def checkUser(self, data, password):
        """
        This method is used to check if a user exist in the database and if the password is correct

        Args:
            data (str): The username or email of the user
            password (str): The password of the user

        Returns:
            bool: True if the user exist and the password is correct, False if not
        """
        if self.testIfUserExist(data):
            user = self.getUserByName(data)
        elif self.testIfUserExistByEmail(data):
            user = self.getUserByEmail(data)
        else:
            return False
        if user[3] == hashlib.sha256(password.encode()).hexdigest():
            return user
        else:
            return False

    def updateServerPort(self, id, port):
        """
        This method is used to update the port of a server

        Args:
            id (int): The id of the server
            port (int): The port of the server

        Returns:
            bool: True if the port has been updated, False if not
        """
        try:
            conn = sqlite3.connect(self.fileName)
            c = conn.cursor()
            c.execute('UPDATE servers SET serverPort = ? WHERE id = ?', (port, id))
            conn.commit()
            conn.close()
            return True
        except:
            return False
        
    def getUserServers(self, username):
        """
        This method is used to get all servers of a user

        Args:
            username (str): The username of the user

        Returns:
            list: A list of all servers of the user
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE owner = ?', (username,))
        servers = c.fetchall()
        conn.close()
        return servers
    
    def isUserServerHasPort(self, username):
        """
        This method is used to test if a user has a server with a port

        Args:
            username (str): The username of the user

        Returns:
            bool: True if the user has a server with a port, False if not
        """
        servers = self.getUserServers(username)
        for server in servers:
            if server[4] != None:
                return True
        return False
    
    def getServerWithPorts(self):
        """
        This method is used to get all servers with a port

        Returns:
            list: A list of all servers with a port
        """
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE serverPort IS NOT NULL')
        servers = c.fetchall()
        conn.close()
        return servers
    