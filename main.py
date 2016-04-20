from network.Listener import Listener
from network.ServerConnection import ServerConnection

#Setting up the logging
import logging
import sys
logger = logging.getLogger('server')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
fh = logging.FileHandler("do-backend.log", "w")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

if __name__ == '__main__':
    address = ('localhost', 8080)
    # All we have to do is to start the server
    server = Listener(address, ServerConnection, bind_and_activate=False)
    server.start_sync()
