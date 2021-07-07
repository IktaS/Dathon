import configparser
import socket
import sys
import threading
from client import *
from room import *

config = configparser.ConfigParser()
config.read(".env")

APP_HOST = config.get("app", "APP_HOST")
APP_PORT = config.get("app", "APP_PORT")

BUFFER_SIZE = int(config.get("app", "BUFFER_SIZE"))

class Server:
    def __init__(self, host, port, logger, clientFactory, BUFFER_SIZE, listen = 100):
        super().__init__()
        self.host = host
        self.port = port
        self.logger = logger
        self.clientFactory = clientFactory

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(listen)
        self.clients = []
        self.handlers = []

        self.BUFFER_SIZE = BUFFER_SIZE

        self.closed = False
    
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

    class LoggerHandler:
        def __init__(self, logger):
            self.logger = logger
        
        def handle(self, client, message):
            print("client " + str(client) + " said " + str(message), file=self.logger)
    
    class ServerHandler:
        def __init__(self, server, logger):
            self.logger = logger
            self.server = server
        
        def handle(self, client, command):
            print("client " + str(client) + " said " + str(command), file=self.logger)
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
                                print("Could not find client id " + params[2], file=self.logger)
                                client.sendEncode("username|check|")
                            else:
                                client.sendEncode("username|check|" + c.username)
                        else:
                            client.sendEncode("username|check|")
                else:
                    client.sendEncode("username|FAIL")
            elif params[0] == "scoreboard":
                print("scoreboard")
                #TODO: implement scoreboard command
            elif params[0] == "private":
                print("private")
                #TODO: implement private command
                # this is for demo only delete afterwards
                if params[1]:
                    print(params[1])
                    if params[1] == "make":
                        self.room_factory = RoomFactory()
                        self.room = self.room_factory.create_room(client)
                        print("created room with id", self.room.id)
                        client.sendEncode("private|" + self.room.room_code)

                    elif params[1] == "join":
                        if params[2]:
                            if params[2] == self.room.room_code:
                                self.room.add_client(client)
                            else:
                                client.sendEncode("room|failed")

            elif params[0] == "matchmake":
                print("matchmake")
                #TODO: implement matchmake command

            # this is for demo only delete afterwards
            elif params[0] == "room" and self.room.check_client(client):
                if params[1] == "chat":
                    self.room.chat(params[2], client)



factory = ClientFactory(ClientNumberIDGenerator())

s = Server('localhost', 8081, sys.stdout, factory, 2048)

try:
    s.start_server()
except KeyboardInterrupt:
    s.stop_server()
    sys.exit(0)