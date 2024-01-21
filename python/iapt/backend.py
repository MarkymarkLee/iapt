import socket
from ssl import SSLContext, PROTOCOL_TLS_CLIENT
import json


class Backend:
    def __init__(self):
        HOST, PORT = '127.0.0.1', 9999
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Create a new SSL context
        context = SSLContext(PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.load_verify_locations(cafile='iapt/secret/cert.pem')
        # Wrap the socket for SSL
        self._socket = context.wrap_socket(sock)
        # Connect to the server
        self._socket.connect((HOST, PORT))

    def __pad_to_ten(self, num) -> str:
        num = str(num)
        while len(num) < 10:
            num += "\n"
        return num

    def send_command(self, command):
        print(command)
        command = json.dumps(command, ensure_ascii=False).encode()
        command_length = self.__pad_to_ten(len(command)).encode()
        print(len(command_length))
        self._socket.sendall(command_length)
        self._socket.sendall(command)

    def recv_data(self):
        self._socket.recv(10)
        return self._socket.recv(1024).decode()

    def close(self):
        self._socket.close()
