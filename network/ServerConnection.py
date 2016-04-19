import SocketServer
import threading
from BusinessLogic import BusinessLogic
class ServerConnection(SocketServer.StreamRequestHandler):

    def handle(self):
        print "STARTING"
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        while True:

            data = self.rfile.readline().strip()
            if not data:
                # EOF, client closed, just return
                return
            result = BusinessLogic.handle_message(data)
            print "Writing %s" % result
            self.wfile.write(result)
            self.wfile.flush()

