from network.Listener import Listener
from network.ServerConnection import ServerConnection
import threading
import socket


if __name__ == '__main__':
    address = ('localhost', 8080)
    server = Listener(address, ServerConnection, bind_and_activate=False)
    server.allow_reuse_address = True
    server.request_queue_size = 100
    server.server_bind()
    server.server_activate()
    server.serve_forever()
    t = threading.Thread(target=server.serve_forever)
    t.daemon = True
    t.start()

    print 'Server loop running in thread:', t.getName()

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8080))

    # Send the data
    message = 'Hello, world\n'
    print 'Sending : "%s"' % message
    len_sent = s.send(message)

    # Receive a response
    response = s.recv(1024)
    print 'Received: "%s"' % response

    # Clean up
    s.close()
    server.socket.close()