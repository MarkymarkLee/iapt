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
            return False, "Disconnected"

        try:
            data = data.decode(encoding='utf-8')
            command = json.loads(data)
        except:
            logger.error('Invalid command: %s', data)
            return False, "Invalid command"

        return True, command

    @staticmethod
    def run_command(command: dict):
        if 'command' not in command:
            logger.error('No command')
            return False, "No command"

        if 'data' not in command:
            logger.error('Invalid command: %s', command)
            return False, "Invalid command"

        return True, command['command'], command['data']

    @staticmethod
    def create(username):
        pass

    @staticmethod
    def set(command):
        pass

    @staticmethod
    def create(command):
        pass


def handle_client(conn: socket, addr: str):
    logger.info('%s is connected', addr)
    while True:
        good, command = ClientUtils.recv_command(conn)
        if not good and command == "Disconnected":
            break
        elif not good:
            continue

        logger.info('%s Received: %s', addr, json.dumps(
            command, ensure_ascii=False))

    logger.info('%s Disconnect', addr)
    conn.close()


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            context = SSLContext(PROTOCOL_TLS_SERVER)
            context.load_cert_chain(
                certfile='secret/cert.pem', keyfile='secret/key.pem')
            with context.wrap_socket(s, server_side=True) as secure_conn:
                secure_conn.bind((self.host, self.port))
                secure_conn.listen()
                while True:
                    conn, addr = secure_conn.accept()
                    threading.Thread(target=handle_client,
                                     args=(conn, addr)).start()


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9999
    server = Server(HOST, PORT)
    server.run()
