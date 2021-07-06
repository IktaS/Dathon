class Input_Command:
    username_update = "username|update|"     # + {username}
    username_check = "username|check|"       # + {client_id}
    private_create = "private|make"
    private_join = "private|join|"           # + {room-code}
    matchmaking_join = "matchmake|join"
    matchmaking_exit = "matchmake|exit"
    game_exit = "exit"
    scoreboard = "scoreboard"
    
    def __init__(self, id):
        self.id = id

    def get(self):
        #TODO: change to input from ui
        cmd = input()
        command = cmd.split(" ")

        if command[0] == "update":
            return username_update + command[1]
        elif command[0] == "check":
            return username_check + self.id
        elif command[0] == "create_private":
            return private_create
        elif command[0] == "join_private":
            return private_join + command[1]
        elif command[0] == "join_matchmaking":
            return matchmaking_join
        elif command[0] == "exit_matchmaking":
            return matchmaking_exit
        elif command[0] == "exit":
            return game_exit
        elif command[0] == "scoreboard":
            return scoreboard


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