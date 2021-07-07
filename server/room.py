import string
import random

from client import *


class RoomFactory:
    def __init__(self):
        self.currentID = 0
    
    def create_room(self):
        self.currentID += 1
        return Room(self.currentID, code_generator())

def code_generator():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


class Room:
    def __init__(self, room_id, room_code):
        self.room_id = room_id
        self.room_code = room_code
        self.clients = []
        self.board = {}

    def start_game():
        self.broadcast('room|' + self.room_id + '|start')
        self.first_move()
        
        for c in self.clients:
            self.board[c] = [7,7,7,7,7,7,7, 0]
    
    def first_move(self):
        self.current_player = random.choice(self.clients)
        self.sendOther( 'room| move | other' , self.current_player)
        self.current_player.sendEncode('room| move | you')

    def broadcast(message):
        for c in self.clients:
            c.sendEncode(message)

    def sendOther(message, client):
        for c in self.clients:
            if c != client:
                c.sendEncode(message)
        
    def set_client(self, client):
        self.clients.append(client)
        if len(self.clients) > 1:
            self.start_game()

    def remove_client(self, client):
        if client in self.clients:
            self.clients.remove(client)