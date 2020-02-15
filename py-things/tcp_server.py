import socketserver
import time


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the hande() method to implement communication to the 
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote: {}".format(self.client_address[0], self.data))
        #print(self.data)
        time.sleep(10)
        print('leaving handle()')
        #self.request.sendall(self.data)


if __name__ == "__main__":
    HOST, PORT = "localhost", 50007

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
