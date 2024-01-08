import socket
from ssl import SSLContext, PROTOCOL_TLS_CLIENT, CERT_NONE
from time import sleep

HOST, PORT = '127.0.0.1', 9999

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create a new SSL context
context = SSLContext(PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.load_verify_locations(cafile='secret/cert.pem')

# Wrap the socket for SSL
wrapped_socket = context.wrap_socket(sock)

try:
    # Connect to the server
    wrapped_socket.connect((HOST, PORT))

    # Send some data
    wrapped_socket.sendall(b'Hello, server!')

    # Receive and print the response
    received = wrapped_socket.recv(1024)
    print('Received:', received.decode())

    # Sleep for 5 seconds
    sleep(5)

    # Send some data
    wrapped_socket.sendall(b'Hello, server 2!')

    # Receive and print the response
    received = wrapped_socket.recv(1024)
    print('Received:', received.decode())


finally:
    wrapped_socket.close()
