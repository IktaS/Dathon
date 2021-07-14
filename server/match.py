import string
import random

from clients import *

class Match:
    def __init__(self, server, player1, player2):
        self.server = server
        self.player1 = player1
        self.player2 = player2
        
        self.board = {
            self.player1: [7, 7, 7, 7, 7, 7, 7, 0],
            self.player2: [7, 7, 7, 7, 7, 7, 7, 0]
            # self.player1: [0, 0, 0, 0, 0, 0, 1, 96],
            # self.player2: [0, 0, 0, 0, 0, 0, 1, 0]

        }

        handler = MatchHandler(self)
        self.previusPlayer1Handler = player1.commandHandler
        self.previusPlayer2Handler = player2.commandHandler
        self.player1.setCommandHandler(handler)
        self.player2.setCommandHandler(handler)
        
        self.startgame()

    def startgame(self):
        print('match|start')

        if bool(random.getrandbits(1)):
            self.current_player = self.player1
            self.player2.sendEncode('match|start|other|' + self.player1.username)
            self.player1.sendEncode('match|start|you|' + self.player2.username)
        else:
            self.current_player = self.player2
            self.player1.sendEncode('match|start|other|' + self.player2.username)
            self.player2.sendEncode('match|start|you|' + self.player1.username)


    def move(self, client, i: int):
        # print(self.board)
        if client != self.current_player:
            return

        other_client = self.getOther_client(client)
        other_client.sendEncode('match|move|' + str(i))

        biji = self.board[client][i]
        self.board[client][i] = 0

        while biji:
            while biji:
                i += 1
                if i == 7:
                    break

                self.board[client][i] += 1
                biji -= 1

                if biji == 0:
                    if self.board[client][i] > 1:
                        biji = self.board[client][i]
                        self.board[client][i] = 0
                    else:
                        self.board[client][7] += self.board[other_client][6-i]
                        self.board[other_client][6-i] = 0

            if biji > 0:
                self.board[client][7] += 1
                biji -= 1

            i = 0
            while biji:
                self.board[other_client][i] += 1
                biji -= 1

                if biji == 0:
                    if self.board[other_client][i] > 1:
                        biji = self.board[other_client][i]
                        self.board[other_client][i] = 0

                i += 1
                if i == 7:
                    break
            i = 0

        if (self.check_endgame()):
            self.endgame()
        else:
            self.checkturn(other_client)

    def endgame(self):
        self.checkResult()

        # self.server.saveScore( self.board[player1][7], self.player1.username)
        # self.server.saveScore( self.board[player2][7], self.player2.username)

        self.player1.setCommandHandler( self.previusPlayer1Handler)
        self.player2.setCommandHandler( self.previusPlayer2Handler)

    def check_endgame(self):
        if (self.board[self.player1][7] + self.board[self.player2][7]) == 98:
            return True
        else:
            return False

    def checkturn(self, client):
        for i in range(7):
            if self.board[client][i] > 0:
                self.current_player = client
                return

    def getOther_client(self, client):
        if client == self.player1:
            return self.player2
        else:
            return self.player1

    def checkResult(self):
        if self.board[self.player1][7] > self.board[self.player2][7]:
            print('player1 Win')
            self.player1.sendEncode('match|end|win')
            self.player2.sendEncode('match|end|lose')
        elif self.board[self.player1][7] < self.board[self.player2][7]:
            print('player2 Win')
            self.player1.sendEncode('match|end|win')
            self.player2.sendEncode('match|end|lose')
        else:
            self.broadcast('match|end|draw')

    def broadcast(self, message):
        self.player1.sendEncode(message)
        self.player2.sendEncode(message)

    def chat(self, client, message):
        
        if client == self.player1:
            print("p1")
            self.player2.sendEncode('chat|' + client.username + '|' + message)
        else:
            self.player1.sendEncode('chat|' + client.username + '|' + message)


class MatchHandler:
    def __init__(self, match):
        self.match = match

    def handle(self, client: Client, command: str):
        print(command)
        command = command.rstrip()
        params = command.split("|")

        if params[0] == 'match':
            if params[1] == 'move':
                self.match.move(client, int(params[2]))

        elif params[0] == 'chat':
            self.match.chat(client, params[1])
