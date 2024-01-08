from ssl import SSLContext, PROTOCOL_TLS_SERVER
import socketserver
from socketserver import BaseServer


class MyTCPHandler(socketserver.BaseRequestHandler):

    def setup(self):
        print("Connection established:", self.client_address)
        super().setup()

    def handle(self):
        # self.request is the SSL-wrapped socket
        self.data = self.request.recv(1024).strip()
        # print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

    def finish(self):
        print("Connection closed:", self.client_address)
        super().finish()


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9999

    # Create the server
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Create a new SSL context
    context = SSLContext(PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='secret/cert.pem',
                            keyfile='secret/key.pem')

    # Wrap the server socket with SSL
    server.socket = context.wrap_socket(server.socket, server_side=True)

    # Activate the server
    server.serve_forever()
