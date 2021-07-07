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
        self.chat = "chat"

    def get(self):
        #TODO: change to input from ui
        cmd = input()
        params = cmd.split("|")

        if params[0] == "update":
            return self.username_update + params[1]
        elif params[0] == "check":
            return self.username_check + self.id
        elif params[0] == "create_private":
            return self.private_create
        elif params[0] == "join_private":
            return self.private_join + params[1]
        elif params[0] == "join_matchmaking":
            return self.matchmaking_join
        elif params[0] == "exit_matchmaking":
            return self.matchmaking_exit
        elif params[0] == "exit":
            return self.game_exit
        elif params[0] == "scoreboard":
            return self.scoreboard
        elif params[0] == "chat":
            return 'room|' + params[1]
        else:
            return ""

class Server_Command:

    def set(self, cmd):
        #TODO: change to do something
        params = cmd.split("|")

        if params[0] == "username":
            if params[1]:
                if params[1] == "update":
                    if params[2] == "OK":
                        print("username has been changed")
                    else:
                        print("failed to change username")
                elif params[1] == "check":
                    if params[2] and params[2] != "":
                        print("your username is " + params[2])
                    else:
                        print("id not found")
            else:
                print("invalid request")
        elif params[0] == "chat":
            print("server >> " + params[1])
        else:
                print("invalid request")