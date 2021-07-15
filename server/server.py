import configparser
from server.scoreboard import Scoreboard
from match import Match
from clients import Client, ClientFactory, ClientNumberIDGenerator
from room import UIDGenerator, Room, RoomFactory
import socket
import sys
import threading
import queue

config = configparser.ConfigParser()
config.read(".env")

APP_HOST = config.get("app", "APP_HOST")
APP_PORT = config.get("app", "APP_PORT")

BUFFER_SIZE = int(config.get("app", "BUFFER_SIZE"))

SCORE_FILE = config.get("app", "SCORE_FILE")


class Server:
    def __init__(self, host, port, logger, clientFactory, BUFFER_SIZE, listen=100, roomFactory: RoomFactory = None):
        super().__init__()
        self.host = host
        self.port = port
        self.logger = logger
        self.clientFactory = clientFactory

        self.roomFactory = roomFactory
        self.rooms: dict[str, Room] = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(listen)
        self.clients = []
        self.handlers = []

        self.queue = queue.Queue()

        self.BUFFER_SIZE = BUFFER_SIZE

        self.closed = False

        self.scorefile = open(SCORE_FILE, 'rw')
        self.scoreboard = Scoreboard(self.scorefile)

    def register_client(self, client):
        self.clients.append(client)

    def remove_client(self, client):
        if client in self.clients:
            client.stop()
            self.clients.remove(client)

    def make_client(self, sock, addr):
        return self.clientFactory.createClient(self.BUFFER_SIZE, sock, addr)

    def log_message(self, message):
        print(message, file=self.logger)

    def start_server(self):
        # start server thread running run()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop_server(self):
        # stop server thread
        self.closed = True
        for client in self.clients:
            client.stop()
        self.socket.close()
        self.scoreboard.save()
        self.scorefile.close()

    def find_client(self, id):
        for client in self.clients:
            if client.id == int(id):
                return client
        return None

    def run(self):
        serverHandler = Server.ServerHandler(self, self.logger)
        while True and not self.closed:
            sock, addr = self.socket.accept()
            client = self.make_client(sock, addr)
            self.log_message("client " + str(client) + " connected")
            client.setCommandHandler(serverHandler)
            client.start()
            client.sendEncode(str(client.id))
            self.register_client(client)

    def saveScore(self, score, username):
        self.scoreboard.addScore(username, score)

    class LoggerHandler:
        def __init__(self, logger):
            self.logger = logger

        def handle(self, client, message):
            print("client " + str(client) + " said " +
                  str(message), file=self.logger)

    class ServerHandler:
        def __init__(self, server, logger):
            self.logger = logger
            self.server: Server = server

        def handle(self, client: Client, command: str):
            print("client " + str(client) + " said " +
                  str(command), file=self.logger)
            command = command.rstrip()
            params = command.split("|")
            if params[0] == "username":
                if params[1]:
                    if params[1] == "update":
                        if params[2] and params[2] != "":
                            client.setUsername(params[2])
                            client.sendEncode("username|update|OK")
                        else:
                            client.sendEncode("username|update|FAIL")
                    elif params[1] == "check":
                        if params[2] and params[2] != "":
                            c = self.server.find_client(params[2])
                            if c == None:
                                print("Could not find client id " +
                                      params[2], file=self.logger)
                                client.sendEncode("username|check|")
                            else:
                                client.sendEncode(
                                    "username|check|" + c.username)
                        else:
                            client.sendEncode("username|check|")
                else:
                    client.sendEncode("username|FAIL")
            elif params[0] == "scoreboard":
                print("scoreboard")
                client.sendEncode(self.server.scoreboard.toJSON())
            elif params[0] == "private":
                if params[1]:
                    if params[1] == "make":
                        room = self.server.roomFactory.newRoom(
                            self.server, client
                        )
                        self.server.rooms[room.id] = room
                        client.sendEncode("private|" + room.id)
                    elif params[1] == "join":
                        if params[2]:
                            if params[2] in self.server.rooms and not self.server.rooms[params[2]].locked:
                                self.server.rooms[params[2]].addClient(client)
                            else:
                                client.sendEncode("private|failed")

            elif params[0] == "matchmake":
                print("matchmake")
                self.server.queue.put(client)
                if self.server.queue.qsize() == 2:
                    c1 = self.server.queue.get()
                    c2 = self.server.queue.get()
                    match = Match(self.server, c1, c2)


clientFactory = ClientFactory(ClientNumberIDGenerator())
roomFactory = RoomFactory(UIDGenerator(6))

s = Server('localhost', 8081, sys.stdout,
           clientFactory, 2048, roomFactory=roomFactory)

try:
    s.start_server()
    input()
except KeyboardInterrupt:
    s.stop_server()
    sys.exit(0)
except Exception as e:
    print(e)
    s.stop_server()
    sys.exit(0)
