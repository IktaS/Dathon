import string
import random

from client import *

def code_generator():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

class RoomFactory:
    def __init__(self):
        self.currentID = 0
    
    def create_room(self, client):
        self.currentID += 1
        return Room(self.currentID, code_generator(), client)


class Room:
    def __init__(self, id, room_code, client):
        self.id = id
        self.room_code = room_code
        self.clients = [client]
        self.board = {}
        print(self.id, self.room_code)

    def start_game(self):
        self.broadcast('room|' + self.id + '|start')
        self.first_move()
        
        for c in self.clients:
            # board is reverse this way --> for the player perspective
            self.board[c] = [7,7,7,7,7,7,7, 0]
    
    def first_move(self):
        self.current_player = random.choice(self.clients)
        self.sendOther( 'room|move|other' , self.current_player)
        self.sendMe('room|move|you', self.current_player)

    def move(self, client, index):
        if client != self.current_player:
            return

        biji = self.board[client][index]
        self.board[client][index] = 0

        other_client = self.getOther_client(client)
        self.sendMe('room|move|' + index, other_client)

        while biji:
            i = index + 1
            while biji:
                self.board[client][i] += 1
                biji -= 1
                i += 1
                if i == 8:
                    break
            i = 0
            while biji:
                self.board[other_client][i] += 1
                biji -= 1
                i += 1
                if i == 7:
                    break

        self.current_player = other_client

    def chat(self, message, client):
        print('room|chat|' + client.username + '|' + message, client)
        self.sendOther('room|chat|' + client.username + '|' + message, client)

    def getOther_client(self, client):
        for c in self.clients:
            if c != client:
                return c

    def check_endgame(self):
        biji = 0
        for c in self.clients:
            biji += self.board[c][7]

        if biji == 98:
            self.endgame()

    def endgame(self):
        if self.board[ self.clients[0] ][7] > self.board[ self.clients[1] ][7]:
            self.sendOther('room|end|lose', self.clients[0])
            self.sendMe('room|end|win', self.clients[0])
        elif self.board[ self.clients[0] ][7] < self.board[ self.clients[1] ][7]:
            self.sendOther('room|end|lose', self.clients[1])
            self.sendMe('room|end|win', self.clients[1])
        else:
            self.broadcast('room|end|draw')


    def broadcast(self, message):
        for c in self.clients:
            c.sendEncode(message)


    def sendOther(self, message, client):
        for c in self.clients:
            if c != client:
                c.sendEncode(message)

    def sendMe(self, message, client):
        client.sendEncode(message)
        
    def add_client(self, client):
        self.broadcast("room|" + client.username + " has join")
        self.clients.append(client)
        # if len(self.clients) > 1:
        #     self.start_game()

    def remove_client(self, client):
        if client in self.clients:
            self.clients.remove(client)

    def check_client(self, client):
        for c in self.clients:
            if c == client:
                return True
        return False