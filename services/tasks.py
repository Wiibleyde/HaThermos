import time
import threading
from utils.minecraft import MinecraftService

class serverCheck:
    def __init__(self,host,port):
        self.server = MinecraftService(host,port)
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        beforeShutDown = 15
        while True:
            time.sleep(5)
            if self.server.getPlayerCount() is not None:
                print(self.server.getPlayerCount())

    