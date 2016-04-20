import SocketServer
class Listener(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    def start_sync(self, protocol_handler):
        """
            Setting some socket specific parameters :
                allow_reuse_address - allow the os to recycle the port as soon as the app shuts down
                request_queue_size - basically the number of concurrent sockets available
                bind->activate->serve_forever : binds the socket and starts listening
        """
        self.allow_reuse_address = True
        self.request_queue_size = 128
        self.protocol_handler = protocol_handler
        self.server_bind()
        self.server_activate()
        self.serve_forever()