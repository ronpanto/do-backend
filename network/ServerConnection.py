import SocketServer
import threading
class ServerConnection(SocketServer.StreamRequestHandler):

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls

        data = self.rfile.readline().strip()
        result = self.parse_message(data)

        self.wfile.write(result)

    def parse_message(self, buffer):
        buffer_parts = buffer.split("|")
        try:
            if len(buffer_parts) != 3:
                raise Exception("Syntax Error")
            verb, package_name, deps = buffer_parts
        except Exception, ex:
            return "ERROR\n"