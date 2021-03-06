from network.Listener import Listener
from network.ServerConnection import ServerConnection
from BusinessLogic import BusinessLogic
from storage.MemStorage import MemStorage
from network.LineProtocol import LineProtocol

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
    address = ('', 8080)
    business_logic = BusinessLogic(storage_layer=MemStorage())
    # All we have to do is to start the server
    server = Listener(address, ServerConnection, bind_and_activate=False)
    server.start_sync(protocol_handler=LineProtocol(business_logic))
