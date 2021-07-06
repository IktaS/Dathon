import socket
import select
import sys
from threading import Thread

BUFFER_SIZE = 2048


class Server:
    def __init__(self, ip_address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip_address, port))
        self.id = sock.recv(BUFFER_SIZE).decode()

        self.connect()

    def connect(self):
        Thread(target=self.send_thread, args=()).start()
        Thread(target=self.recv_thread, args=()).start()

    def send_thread(self):
        input_command = Input_Command()
        while True:
            data = input_command.get()
            self.sock.send(data.encode())

    def recv_thread(self):
        while True:
            data = self.sock.recv(BUFFER_SIZE).decode()
            print(data)
            

try:
    ip_address = '127.0.0.1'
    port = 8081
    
    server = Server(ip_address, port)
except KeyboardInterrupt:
    sys.exit(0)