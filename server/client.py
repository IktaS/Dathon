class ClientFactory:
    def __init__(self, IDGenerator):
        self.generator = IDGenerator
    
    def createClient(self, socket, id = None):
        clientID = str(id)
        if(id == None):
            clientID = self.generator.newID()
        return Client(socket, clientID)

class ClientNumberIDGenerator:
    def __init__(self, init = 0):
        self.currentID = init
    
    def newID(self):
        retID = self.currentID
        self.currentID = self.currentID + 1
        return retID

class Client:
    def __init__(self, socket, id):
        self.socket = socket
        self.id = id
        self.username = str(self.id)
    
    def setCommandHandler(self, commandHandler):
        self.commandHandler = commandHandler
    
    def setUsername(self, username):
        self.username = username
    
    def run(self):
        # socket to receive message
        self.commandHandler.handle(command)

    def __repr__(self):
        return f"socket : {self.socket}\nid: {self.id}\nusername: {self.username}\ncurrentHandler: {self.commandHandler}"
    
    def __str__(self):
        return f"username: {self.username}"