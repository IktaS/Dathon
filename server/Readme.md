# Dathon Server Code API

## Connecting to Server

Client connect to `host:port` with socket.

Server will return `id` as player ID.

Now Client will be able to send available [commands](#commands)

## Commands
---
### Assigning username
---
A client can assign a username to their ID, by default their username is their `id`
```bash
username|{username}
```

Server will send back
```bash
username|OK
```
on accepted request

```bash
username|FAIL
```

on failed request

### Getting Scoreboard
---
To get scoreboard data from server, a client can send
```bash
scoreboard|{username}
```

Server will send back a json object
```json
    "server-id": {server-id},
    "scores": [
        {
            "username": {username},
            "score": {score}
        }...
    ]
```
---
### Making a private room
---
Client sends a socket message to server with the format

```bash
private|make
```

Server will make a private room for the client, assign client as room master, and send back a room code with the format

```bash
private|{code}
```

Client can send this code to their friend that's connected to the same server.

While in the room, clients can use several [commands](#-room-commands)

Also while in a room, everytime someone joins a room, the server will broadcast to every client in room a message with the format
```
room|{room-code}|join|{client-id}
```

Indicating in `room` with `room-code` for the room code, happen a `join` action by `client-id` for the joining client `id`.

---
### Room commands
---
```bash
exit
```
will exit the client from the room, if there's no one else in the room, server will close the room and the code will no longer be usable to join. Then the server will broadcast to all client in the room with the format

```bash
room|{room-code}|exit|{client-id}
```
Indicating in `room` with `room-code` for the room code, happen a `exit` action by `client-id` for the exiting client `id`.

In a case where the room master exit the room, another player will be randomly selected as the room master. Then the server will broadcast to all clients in the room a message with the format.
```
room|{room-code}|master|{client-id}
```
Indicating in `room` with `room-code` for the room code, happen a `master` action, indicating that a new room master was chosen which is `client-id` for the new master client `id`.

---
```bash
start
```
will start a match in a given room. for protocols and command while in a match, refer to [this documentation]()

Then the server will broadcast to all clients in the room a message with the format.
```
room|{room-code}|start
```
Indicating in `room` with `room-code` for the room code, happen a `start` action, indicating that the room will now start a match.

---
### Joining a private room
---
To join a private room, client can send 
```bash
private|join|{code}
```

This will join a client to a private room, which will return a JSON object in the form of
```json
{
    "master": {room-master-client-id},
    "clients": [
        ...{client-id}
    ]
}
```
with `master` contains the room master `client-id`, while clients holds all `client-id` in the room, including the room master.

While a client is in this room, clients can use all the available [room commands](#-room-commands)

---
### Matchmaking
---

To join a matchmaking queue, client can send
```bash
matchmake|join
```

Server will enter that client in a matchmaking queue, and returns
```bash
matchmake|{queue-id}|count|{player-count}
```
With `queue-id` is the id of the queue which the player is in, and `player-count` the number of player in that queue.

When a match has been found and ready to be made, 
```bash
matchmake|{queue-id}|start
```
will be broadcasted to all involved client. Indicating that their match is about to start