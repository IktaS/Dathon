import socket
import select
import sys
from threading import Thread

BUFFER_SIZE = 2048


class Network:
    def __init__(self, sock):
        self.sock = sock
        self.id = sock.recv(BUFFER_SIZE).decode()

        print("my id = " + self.id)
        self.start()

    def start(self):
        Thread(target=self.send_thread, args=()).start()
        Thread(target=self.recv_thread, args=()).start()

    def send_thread(self):
        while True:
            data = input()
            self.sock.send(data.encode())

    def recv_thread(self):
        while True:
            data = self.sock.recv(BUFFER_SIZE).decode()
            print(data)
            

try:
    ip_address = '127.0.0.1'
    port = 8081

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((ip_address, port))

    network = Network(server_socket)

except KeyboardInterrupt:
    sys.exit(0)