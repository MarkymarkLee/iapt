import socket
from ssl import SSLContext, PROTOCOL_TLS_SERVER
import threading
import logging
import json

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the handler
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)


class ClientUtils:

    @staticmethod
    def recv_command(conn: socket.socket):
        data = conn.recv(10)
        if not data:
            return False, "Disconnected"

        try:
            data = data.decode()
            data = data.strip()
            data = int(data)
        except:
            logger.error('Invalid length: %s', data)
            return False, "Invalid length"

        command_length = data
        if command_length <= 0:
            logger.error('Invalid length: %s', command_length)
            return False, "Invalid length"

        data = conn.recv(command_length)
        if not data:
            logger.error('Disconnected')
            return False, "Disconnected"
        try:
            data = data.decode()
            command = json.loads(data)
        except:
            logger.error('Invalid command: %s', data)
            return False, "Invalid command"

        return True, command


def handle_client(conn, addr):
    logger.info('Connected by %s', addr)
    while True:
        good, command = ClientUtils.recv_command(conn)
        if not good and command == "Disconnected":
            break
        elif not good:
            continue

        logger.info('%s Received: %s', addr, json.dumps(command))
    conn.close()


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            context = SSLContext(PROTOCOL_TLS_SERVER)
            context.load_cert_chain(
                certfile='secret/cert.pem', keyfile='secret/key.pem')
            while True:
                conn, addr = s.accept()
                with context.wrap_socket(conn, server_side=True) as secure_conn:
                    threading.Thread(target=handle_client,
                                     args=(secure_conn, addr)).start()


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9999
    server = Server(HOST, PORT)
    server.run()
