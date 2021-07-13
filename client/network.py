import configparser
import socket
import select
import sys
from threading import Thread
from enum import Enum

config = configparser.ConfigParser()
config.read(".env")

APP_HOST = 'localhost'
# APP_HOST = config.get("app", "APP_HOST")
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
        # Thread(target=self.send, args=()).start()
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
        print(cmd)
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

        # scoreboard in json
        # scoreboard in json

        # elif params[0] == "room":
        #     print(cmd)
        elif params[0] == "private":
            if params[1] == "failed":
                pass
            else:
                self.game.menu.popUp.text = params[1]
    
        elif params[0] == "match":
            if params[1] == "start":
                self.game.initMatch()
            elif params[1] == "move":
                self.game.match.enemymove(int(params[2]))

            elif params[1] == "other":
                self.game.match.myturn = False
                self.game.board.turn.text="Enemy Turn"
                self.game.board.textName["enemy"].text = params[2]
                self.game.board.updateName()
            elif params[1] == "you":
                self.game.match.myturn = True
                self.game.board.turn.text="Your Turn"
                self.game.board.textName["enemy"].text = params[2]
                self.game.board.updateName()

            elif params[1] == "end":
                if params[2] == "win":
                    pass
                elif params[2] == "lose":
                    pass
                elif params[2] == "draw":
                    pass
                

# try:
#     # server = Server(APP_HOST, APP_PORT)
#     server = Server()
# except KeyboardInterrupt:
#     sys.exit(0)