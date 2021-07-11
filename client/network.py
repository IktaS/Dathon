import configparser
import socket
import select
import sys
from threading import Thread
from command import *

config = configparser.ConfigParser()
config.read(".env")

# APP_HOST = config.get("app", "APP_HOST")
APP_HOST = 'localhost'
APP_PORT = int(config.get("app", "APP_PORT"))

BUFFER_SIZE = int(config.get("app", "BUFFER_SIZE"))

class Server:
    def __init__(self):
        self.BUFFER_SIZE = BUFFER_SIZE

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((APP_HOST, APP_PORT))
        self.id = self.sock.recv(BUFFER_SIZE).decode()

        self.run()

    def run(self):
        # Thread(target=self.send_thread, args=()).start()
        Thread(target=self.recv_thread, args=()).start()

    def send(self, command: str):
        data = command.encode()
        self.sock.send(data)
        # self.input_command = Input_Command(self.id)
        # while True:
        #     data = self.input_command.get()
        #     self.sock.send( data.encode() )

    def recv_thread(self):
        while True:
            data = self.sock.recv(BUFFER_SIZE)
            self.handle( data.decode() )

    def handle(self, cmd):
        params = cmd.split("|")

        if params[0] == "username":
            if params[1]:
                if params[1] == "update":
                    if params[2] == "OK":
                        print("username has been changed")
                    else:
                        print("failed to change username")
                elif params[1] == "check":
                    if params[2] and params[2] != "":
                        print("your username is " + params[2])
                    else:
                        print("id not found")
            else:
                print("invalid request")
        else:
            print(cmd)

# try:
#     # server = Server(APP_HOST, APP_PORT)
#     server = Server('localhost', 8081, 2048)
# except KeyboardInterrupt:
#     sys.exit(0)