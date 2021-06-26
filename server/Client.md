# Client Class Documentation

## Client Class

### Property

`socket` is the socket that's passed through the constructor, uneditable. 

`id` is the client id, passed through the constructor, uneditable. 

`username` is the client username, the default is the string representation of the id.

`commandHandler` is the handler that will handle command that comes through the socket

### Methods

`Client(socket, id)` creates a client object

`setCommandHandler(commandHandler) ` accepts a `commmandHandler` with the method `handle(client , command)` that accepts the client object as a way to send response, and a string command.

`setUsername(username)` sets client username

`send(message)` will send a message to the client socket. It will not encode, so encode the message before you pass it through this method.

`sendEncode(message)` will encode a message and send it to the client socket.

`start()` starts a client thread

`run()` is the method that will run in client thread, it's sole responsibility is accepting data from socket, decoding, and passing it to `commandHandler`

`stop()` stops a client thread

`__str__()` and `__repr__()` is used to represent the client object

## ClientFactory Class

### Property

`generator` is the id generator to generate an ID if it's 0

### Methods

`ClientFactory(IDGenerator)` accepts `IDGenerator` that have `newID()` method.

`createClient(socket, id)` is used to generate a new Client, id is optional, if it's `None`, then `ClientFactory` will use it's `generator` to generate a new ID.

## ClientNumberIDGenerator

Generate id based on number and increments
### Property

`currentID` is the current available ID

### Methods

`ClientNumberIDGenerator(init)` accepts initial value for `currentID`

`newID()` will return `currentID` and increments it