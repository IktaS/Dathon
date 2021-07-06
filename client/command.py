class Input_Command:
        
    def __init__(self, id):
        self.id = id
        self.username_update = "username|update|"     # + {username}
        self.username_check = "username|check|"       # + {client_id}
        self.private_create = "private|make"
        self.private_join = "private|join|"           # + {room-code}
        self.matchmaking_join = "matchmake|join"
        self.matchmaking_exit = "matchmake|exit"
        self.game_exit = "exit"
        self.scoreboard = "scoreboard"

    def get(self):
        #TODO: change to input from ui
        cmd = input()
        command = cmd.split(" ")

        if command[0] == "update":
            return self.username_update + command[1]
        elif command[0] == "check":
            return self.username_check + self.id
        elif command[0] == "create_private":
            return self.private_create
        elif command[0] == "join_private":
            return self.private_join + command[1]
        elif command[0] == "join_matchmaking":
            return self.matchmaking_join
        elif command[0] == "exit_matchmaking":
            return self.matchmaking_exit
        elif command[0] == "exit":
            return self.game_exit
        elif command[0] == "scoreboard":
            return self.scoreboard
        else:
            return ""

class Server_Command:

    def set(self, cmd):
        #TODO: change to do something
        command = cmd.split("|")

        if command[0] == "username":
            if command[1]:
                if command[1] == "update":
                    if command[2] == "OK":
                        print("username has been changed")
                    else:
                        print("failed to change username")
                elif command[1] == "check":
                    if command[2] and command[2] != "":
                        print("your username is " + command[2])
                    else:
                        print("id not found")
            else:
                print("invalid request")
        else:
                print("invalid request")