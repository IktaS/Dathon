import configparser
import socket
import select
import sys
from threading import Thread
from enum import Enum
import json

# read dari .env
config = configparser.ConfigParser()
config.read(".env")

APP_HOST = 'localhost'
# APP_HOST = config.get("app", "APP_HOST")
APP_PORT = int(config.get("app", "APP_PORT"))
BUFFER_SIZE = int(config.get("app", "BUFFER_SIZE"))

class Server:
    def __init__(self, game):
        self.game = game
        self.BUFFER_SIZE = BUFFER_SIZE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((APP_HOST, APP_PORT))
        self.id = self.sock.recv(BUFFER_SIZE).decode()
        self.run()

    # fungsi menjalankan thread untuk recv
    def run(self):
        self.running = True
        Thread(target=self.recv_thread, args=()).start()

    # fungsi menyetop thread untuk recv dan menutup socket
    def stop(self):
        self.send("terminate")
        self.running = False
        self.sock.close()

    # fungsi mengirim perintah ke server
    def send(self, command: str):
        data = command.encode()
        self.sock.send(data)

    # fungsi (thread) menerima dari server
    def recv_thread(self):
        while self.running:
            data = self.sock.recv(BUFFER_SIZE)
            self.handle( data.decode() )

    # fungsi menerjemahkan perintah dari server
    def handle(self, cmd):
        print(cmd)
        params = cmd.split("|")

        # perintah username
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

        # perintah room (saat ada player 2 join, player ini(room master) memulai game)
        elif params[0] == "room":
            if params[2] == "join":
                self.send("start")

        # perintah join room
        elif params[0] == "private":
            if params[1] == "failed":
                self.game.toMenu()
            else:
                self.game.menu.popUp.text = params[1]

        # perintah chat
        elif params[0] == "chat":
            self.game.board.chat.updateChat(params[1],params[2])
    
        # perintah dalam match
        elif params[0] == "match":
            # perintah memulai match dan setup board
            if params[1] == "start":
                self.game.initMatch()
                if params[2] == "other":
                    self.game.match.myturn = False
                    self.game.board.turn.text="Enemy Turn"
                    self.game.board.textName["enemy"].text = params[3]
                    self.game.board.updateName()
                elif params[2] == "you":
                    self.game.match.myturn = True
                    self.game.board.turn.text="Your Turn"
                    self.game.board.textName["enemy"].text = params[3]
                    self.game.board.updateName()

            # perintah move dari player lain
            elif params[1] == "move":
                self.game.match.enemymove(int(params[2]))

            # perintah akhir permainan
            elif params[1] == "end":
                if params[2] == "win":
                    self.game.board.win.banner="Congratulation !"
                    self.game.board.win.text="You Win!"
                elif params[2] == "lose":
                    self.game.board.win.banner="Too Bad !"
                    self.game.board.win.text="You Lose!"
                elif params[2] == "draw":
                    self.game.board.win.banner="GG  !!!"
                    self.game.board.win.text="It's a Tie!"
                self.game.board.update()
                self.game.gameOver()
                self.send("exit")

            # perintah cheat
            elif params[1] == 'cheat_activated':
                self.game.match.cheat_activated()
        
        # perintah highest Score
        elif params[0] == 'scoreboard':
            score = json.loads(params[1])
            player=[]
            a=0
            
            for i in score:
                dict={
                    "username": i,
                    "score" : score[i]
                }
                player.append(dict)
                if a ==4:
                    break
                a+=1
            self.game.hs.playerList=player
                
                

# try:
#     # server = Server(APP_HOST, APP_PORT)
#     server = Server()
# except KeyboardInterrupt:
#     sys.exit(0)