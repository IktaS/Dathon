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
    
    def setCommandHandler(self, commandHandler):
        self.commandHandler = commandHandler
    
    def setUsername(self, username):
        self.username = username

    def send(self, message):
        # sends message through socket, will not encode the message
    
    def sendEncode(self, message):
        # sends message through socket, will not encode the message
        message = message.encode()
        self.send(message)

    def start(self):
        # run self.run in thread, and
        # self.thread will be used to store the thread
    
    def run(self):
        # socket to receive message
        self.commandHandler.handle(self, command)
    
    def stop(self):
        # stop the thread

    def __repr__(self):
        return f"socket : {self.socket}\nid: {self.id}\nusername: {self.username}\ncurrentHandler: {self.commandHandler}"
    
    def __str__(self):
        return f"username: {self.username}"