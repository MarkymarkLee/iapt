import socket
from ssl import SSLContext, PROTOCOL_TLS_CLIENT, CERT_NONE
from time import sleep
import json

HOST, PORT = '127.0.0.1', 9999

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create a new SSL context
context = SSLContext(PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.load_verify_locations(cafile='secret/cert.pem')

# Wrap the socket for SSL
wrapped_socket = context.wrap_socket(sock)
# Connect to the server
wrapped_socket.connect((HOST, PORT))


def pad_to_ten(num):
    num = str(num)
    while len(num) < 10:
        num += "\n"
    return num


def send_command(command):
    print(command)
    command = json.dumps(command, ensure_ascii=False).encode()
    command_length = pad_to_ten(len(command)).encode()
    print(len(command_length))
    wrapped_socket.sendall(command_length)
    wrapped_socket.sendall(command)


try:
    send_command(
        {"command": "login", "username": "admi愛", "password": "admin"})

finally:
    wrapped_socket.close()
