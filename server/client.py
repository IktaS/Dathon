import threading

class ClientFactory:
    def __init__(self, IDGenerator):
        self.generator = IDGenerator
    
    def createClient(self, BUFFER_SIZE, socket, addr, id = None):
        clientID = str(id)
        if(id == None):
            clientID = self.generator.newID()
        return Client(BUFFER_SIZE, socket, addr, clientID)

class ClientNumberIDGenerator:
    def __init__(self, init = 0):
        self.currentID = init
    
    def newID(self):
        retID = self.currentID
        self.currentID = self.currentID + 1
        return retID

class Client:
    def __init__(self, BUFFER_SIZE, socket, addr, id):
        self.socket = socket
        self.id = id
        self.username = str(self.id)
        self.BUFFER_SIZE = BUFFER_SIZE
        self.addr = addr

        self.closed = False
    
    def setCommandHandler(self, commandHandler):
        self.commandHandler = commandHandler
    
    def setUsername(self, username):
        self.username = username

    def send(self, message):
        if(self.closed):
            raise Exception("client is closed")
        try:
            self.socket.send(message)
        except:
            self.socket.close()
            raise Exception("cannot send message")
    
    def sendEncode(self, message):
        # sends message through socket, will not encode the message
        message = message.encode()
        self.send(message)

    def start(self):
        # run self.run in thread, and
        # self.thread will be used to store the thread
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
    
    def run(self):
        while True and not self.closed:
            try:
                # socket to receive message
                command = self.socket.recv(self.BUFFER_SIZE).decode()
                if command:
                    self.commandHandler.handle(self, command)
                else:
                    self.stop()
                    return
            except Exception as e:
                continue
    
    def stop(self):
        # stop the thread
        self.socket.close()
        self.closed = True


    def __repr__(self):
        return f"socket : {self.socket}\nid: {self.id}\nusername: {self.username}\ncurrentHandler: {self.commandHandler}"
    
    def __str__(self):
        return f"username: {self.username}"