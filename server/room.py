import json
import random
from clients import Client
from typing import List
import string


class UIDGenerator:
    def __init__(self, length) -> None:
        self.length = length

    def newID(self) -> str:
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(self.length))


class RoomFactory:
    def __init__(self, IDGenerator: UIDGenerator) -> None:
        self.id_generator = IDGenerator

    def newRoom(self, master: Client = None):
        return Room(self.id_generator.newID(), master)


class Room:
    def __init__(self, id, master: Client = None) -> None:
        self.id = id
        self.master: Client = master
        self.clients: List[Client] = []
        self.previousHandlers = {}
        self.handler = RoomCommandHandler(self)

        if self.master is not None:
            self.clients.append(master)
            self.previousHandlers[master] = master.commandHandler
            master.setCommandHandler(self.handler)

    def clientLeave(self, client: Client) -> bool:
        if client not in self.clients:
            return False

        self.clients.remove(client)
        client.setCommandHandler(self.previousHandlers[client])
        self.previousHandlers.pop(client, None)

        self.broadcastMessageEncode(
            "room|" + str(self.id) + "|exit|" + str(client.id),
            client
        )

        if client == self.master:
            if not len(self.clients):
                self.master = None
                return True
            self.master = random.choice(self.clients)
            if self.master is not None:
                self.broadcastMessageEncode(
                    "room|" + str(self.id) + "|master|" + str(self.master.id)
                )

        return True

    def addClient(self, client: Client) -> None:
        self.previousHandlers[client] = client.commandHandler
        client.setCommandHandler(self.handler)
        self.clients.append(client)

        try:
            client.sendEncode(self.toJSON())
        except Exception as e:
            print(e)

        self.broadcastMessageEncode(
            "room|" + str(self.id) + "|join|" + str(client.id),
            client
        )

    def startMatch(self, caller: Client) -> bool:
        if caller is not self.master:
            return False
        # TODO: implement match

    def broadcastMessageEncode(self, message: str, exception: Client = None):
        if not len(self.clients):
            return
        for client in self.clients:
            if exception != None and client == exception:
                continue
            print("sending to: " + str(client.username))
            client.sendEncode(message)

    def toJSON(self):
        jsonObject = RoomData()
        jsonObject.master = self.master.id
        jsonObject.clients = []
        for client in self.clients:
            jsonObject.clients.append(client.id)
        return json.dumps(jsonObject, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class RoomData:
    def __init__(self) -> None:
        self.master = None
        self.clients = []


class RoomCommandHandler:
    def __init__(self, room: Room) -> None:
        self.room = room

    def handle(self, client: Client, command: str):
        command = command.rstrip()
        params = command.split("|")
        if params[0] == "exit":
            try:
                succ = self.room.clientLeave(client)
            except Exception as e:
                print(e)
            if succ:
                client.sendEncode("room|exit|success")
            else:
                client.sendEncode("room|exit|fail")
        elif params[0] == "start":
            self.room.startMatch(client)
