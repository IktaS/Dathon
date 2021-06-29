import configparser
import socket
import sys

config = configparser.ConfigParser()
config.read(".env")

APP_HOST = config.get("app", "APP_HOST")
APP_PORT = config.get("app", "APP_PORT")

BUFFER_SIZE = config.get("app", "BUFFER_SIZE")

class Server:
    def __init__(self, host, port, logger, clientFactory, listen = 100):
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
    
    def stop_server(self):
        # stop server thread
    
    def run(self):
        loggerHandler = LoggerHandler(self.logger)
        while True:
            sock, addr = self.socket.accept()
            client = self.make_client(sock, addr)
            self.log_message("client " + str(client) + " connected")
            client.setCommandHandler(loggerHandler)
            client.start()
            self.register_client(client)

    class LoggerHandler:
        def __init__(self, logger):
            self.logger = logger
        
        def handle(self, client, message):
            print("client " + str(client) + " said " + str(message), file=self.logger)
