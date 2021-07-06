class Input_Command:
    update = "username|update|"     # + {username}
    check = "username|check|"       # + {client_id}
    scoreboard = "scoreboard"
    create_private = "private|make"
    join_private = "private|join|"  # + {room-code}
    start = "start"
    join_matchmaking = "matchmake|join"
    exit_matchmaking = "matchmake|exit"
    exit_room = "exit"
    
    def __init__(self, id):
        self.id = id

    def get(self):
        #TODO: change to input from ui
        cmd = input()
        command = cmd.split(" ")

        if command[0] == "update":
            return update + command[1]
        elif command[0] == "check":
            return check + self.id
        elif command[0] == "scoreboard":
            return scoreboard
        elif command[0] == "create_private":
            return create_private
        elif command[0] == "join_private":
            return join_private + command[1]
        elif command[0] == "join_matchmaking":
            return join_matchmaking
        elif command[0] == "exit_matchmaking":
            return exit_matchmaking
        elif command[0] == "exit":
            return exit_room
