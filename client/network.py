import configparser
import socket
import select
import sys
from threading import Thread

config = configparser.ConfigParser()
config.read(".env")

# APP_HOST = config.get("app", "APP_HOST")
APP_HOST = 'localhost'
APP_PORT = int(config.get("app", "APP_PORT"))

BUFFER_SIZE = int(config.get("app", "BUFFER_SIZE"))

class Server:
    # def __init__(self):
    def __init__(self, game):
        self.game = game
        self.BUFFER_SIZE = BUFFER_SIZE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((APP_HOST, APP_PORT))
        self.id = self.sock.recv(BUFFER_SIZE).decode()

        self.run()

    def run(self):
        Thread(target=self.send, args=()).start()
        Thread(target=self.recv_thread, args=()).start()

    def send(self, command: str):
    # def send(self):
        # while True:
            # data = input().encode()
            data = command.encode()
            self.sock.send(data)

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
    
        elif params[0] == "private":
            self.game.menu.popUp.text = params[1]

        else:
            print(cmd)


# try:
#     # server = Server(APP_HOST, APP_PORT)
#     server = Server()
# except KeyboardInterrupt:
#     sys.exit(0)