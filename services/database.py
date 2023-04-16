import sqlite3
import hashlib

class DatabaseService:
    # server is database
    def __init__(self, fileName):
        self.fileName = fileName
        self.createDatabase()

    def createDatabase(self):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS servers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, owner TEXT, serverVersion TEXT, serverPort INTEGER)')
        c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT, admin BOOLEAN)')
        conn.commit()
        conn.close()

    def addServer(self, name, owner, serverVersion):
        if self.testIfExist(name,owner):
            return False
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('INSERT INTO servers (name, owner, serverVersion) VALUES (?, ?, ?)', (name, owner, serverVersion))
        conn.commit()
        conn.close()
        return True

    def deleteServer(self, id):
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
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers')
        servers = c.fetchall()
        conn.close()
        return servers
    
    def getServer(self, id):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE id = ?', (id,))
        server = c.fetchone()
        conn.close()
        return server
    
    def getServerByName(self, name):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE name = ?', (name,))
        server = c.fetchone()
        conn.close()
        return server
    
    def getServerByOwner(self, owner):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE owner = ?', (owner,))
        server = c.fetchall()
        conn.close()
        return server
    
    def getServerByVersion(self, version):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE serverVersion = ?', (version,))
        server = c.fetchone()
        conn.close()
        return server
    
    def testIfExist(self, name, owner):
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
        if self.testIfUserExist(username):
            return False
        hashPassword = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, email, password, admin) VALUES (?, ?, ?, ?)', (username, email, hashPassword, True))
        conn.commit()
        conn.close()
        return True
    
    def addUser(self, username, email, password):
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
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users')
        users = c.fetchall()
        conn.close()
        return users
    
    def getUser(self, id):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE id = ?', (id,))
        user = c.fetchone()
        conn.close()
        return user
    
    def getUserByName(self, username):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        return user
    
    def getUserByEmail(self, email):
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        return user
    
    def testIfUserExist(self, username):
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
        conn = sqlite3.connect(self.fileName)
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE owner = ?', (username,))
        servers = c.fetchall()
        conn.close()
        return servers
    
    def isUserServerHasPort(self, username):
        servers = self.getUserServers(username)
        for server in servers:
            if server[3] != 0:
                return True
        return False