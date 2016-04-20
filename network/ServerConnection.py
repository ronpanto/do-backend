import SocketServer

class ServerConnection(SocketServer.StreamRequestHandler):
    """
    The class that reads and writes once a socket was opened
    """
    def handle(self):
        """
            handle is the callback called once a new connection is made.
            We basically listen on that connection for data all the time and disconnect when the socket does that
            on their end
        """
        while True:
            #Reading a new line
            data = self.rfile.readline().strip()
            if not data:
                # EOF, client closed, just return
                return
            #Sending the message to the protocol interpreter
            result = self.server.protocol_handler.handle_message(data)
            #Sending the result back to the client
            self.wfile.write(result)
            self.wfile.flush()

