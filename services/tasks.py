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
        beforeShutDown = 5
        while True:
            time.sleep(60)
            if beforeShutDown == 0:
                # Stop the server
                break
            if self.server.getPlayerCount() is not None:
                if self.server.getPlayerCount() == 0:
                    if beforeShutDown == 0:
                        self.server.stop()
                        break
                    else:
                        beforeShutDown -= 1
                else:
                    beforeShutDown = 15
    