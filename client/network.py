import configparser
import socket
import select
import sys
from threading import Thread
from command import *

# config = configparser.ConfigParser()
# config.read(".env")

# APP_HOST = config.get("app", "APP_HOST")
# APP_PORT = int(config.get("app", "APP_PORT"))
BUFFER_SIZE = 2048


class Server:
    def __init__(self, ip_address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip_address, port))
        self.id = self.sock.recv(BUFFER_SIZE).decode()

        self.connect()

    def connect(self):
        Thread(target=self.send_thread, args=()).start()
        Thread(target=self.recv_thread, args=()).start()

    def send_thread(self):
        self.input_command = Input_Command(self.id)
        while True:
            data = self.input_command.get()
            self.sock.send( data.encode() )

    def recv_thread(self):
        self.server_command = Server_Command()
        while True:
            data = self.sock.recv(BUFFER_SIZE)
            self.server_command.set( data.decode() )
            

try:
    # server = Server(APP_HOST, APP_PORT)
    server = Server('localhost', 8081)
except KeyboardInterrupt:
    sys.exit(0)