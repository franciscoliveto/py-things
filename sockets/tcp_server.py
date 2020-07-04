import socketserver
import socket
import sys
import getopt

version = '0.1.0'


class EchoRequestHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the hande() method to implement communication to the
    client.
    """
    def setup(self):
        print('setup()')

    def handle(self):
        # self.request is the TCP socket connected to the client
        running = True
        while running:
            try:
                self.data = self.request.recv(1024)
            except TimeoutError:
                # keepalive timeout
                print('connection closed by the client.')
                running = False
            else:
                if self.data:
                    print("{}:{} wrote: {}".format(self.client_address[0],
                                                   self.client_address[1],
                                                   self.data))
                    self.request.sendall(self.data)
                else:
                    print('connection closed by the client.')
                    running = False

    def finish(self):
        print('finish()')


class MyTCPServer(socketserver.TCPServer):
    """My TCP Server class."""
    def __init__(self, address=None, handler=None,
                 allow_reuse_address=False):
        self.allow_reuse_address = allow_reuse_address
        super().__init__(address, handler)

    def server_bind(self):
        """
        It activates after 1 second of idleness, then sends a keepalive ping
        once every 3 seconds, and closes the connection after 3 failed ping,
        or 9 seconds.
        """
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
        super().server_bind()


if __name__ == "__main__":
    def usage():
        """Print usage and exit"""
        sys.stderr.write("""usage: tcp_server.py [OPTIONS]

Mandatory arguments to long options are mandatory for short options too.
  -h, --host=TEXT          The interface to bind to.
  -p, --port=INTEGER       The port to bind to.
      --help               Print a usage message and exit.
      --version            Output version information and exit.
""")
        raise SystemExit(0)

    try:
        (options, arguments) = getopt.getopt(
            sys.argv[1:],
            "h:p:",
            ['host=', 'port=', 'help', 'version']
        )
    except getopt.GetoptError as msg:
        sys.stderr.write('tcp_server.py: ' + str(msg) + '\n')
        raise SystemExit(1)

    if not options:
        sys.stderr.write(
            'tcp_server.py: requires host and port.\n'
        )
        raise SystemExit(1)

    host = ''
    port = 0

    for opt, value in options:
        if opt in ('-h', '--host'):
            host = value
        elif opt in ('-p', '--port'):
            try:
                port = int(value)
            except ValueError:
                sys.stderr.write('tcp_server.py: invalid value.\n')
                raise SystemExit(1)
        elif opt == '--help':
            usage()
        elif opt == '--version':
            sys.stderr.write('Version %s\n' % version)
            raise SystemExit(0)

    try:
        with MyTCPServer((host, port), EchoRequestHandler,
                         allow_reuse_address=True) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()
    except KeyboardInterrupt:
        sys.stderr.write('tcp_server.py: aborted.\n')
