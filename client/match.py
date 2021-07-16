class Match:
    def __init__(self, game):
        self.game = game
        self.board = game.board
        self.myturn = False

    # Mengaktifkan cheat
    def cheat_activated(self):
        for i in range(6):
            self.board.myBoard[i].value = 0
            self.board.myBox[i].value = 0
            self.board.enemyBoard[i].value = 0
            self.board.enemyBox[i].value = 0

        self.board.myBoard[6].value = 1
        self.board.myBox[6].value = 1
        self.board.enemyBoard[6].value = 1
        self.board.enemyBox[6].value = 1

        self.board.myBoard[7].value = 48
        self.board.myBox[7].value = 48
        self.board.enemyBoard[7].value = 48
        self.board.enemyBox[7].value = 48
        print("somthing")
        self.board.update()


    # Gerakan player 
    def move(self,i):
        if self.myturn == False:
            return
        
        self.game.server.send('match|move|' + str(i))
        biji = self.board.myBoard[i].value
        self.board.myBoard[i].value = 0
        self.board.myBox[i].value = 0

        while biji:
            # Board Player
            while biji:
                i += 1
                if i == 7:
                    break

                self.board.myBoard[i].value += 1
                self.board.myBox[i].value += 1
                biji -= 1

                if biji == 0:
                    # Biji di cekungan sendiri masih ada
                    if self.board.myBoard[i].value > 1:
                        biji = self.board.myBoard[i].value
                        self.board.myBoard[i].value = 0
                        self.board.myBox[i].value = 0

                    # jika di cekungan sendiri kosong ambil seberang musuh
                    else:
                        self.board.myBoard[7].value += self.board.enemyBoard[6-i].value
                        self.board.myBox[7].value = self.board.myBoard[7].value
                        self.board.enemyBoard[6-i].value = 0
                        self.board.enemyBox[6-i].value = 0
            
            # cekungan score player
            if biji > 0:
                self.board.myBoard[7].value += 1
                self.board.myBox[7].value += 1
                biji -= 1

            i = 0
            # Board Musuh
            while biji:
                self.board.enemyBoard[i].value += 1
                self.board.enemyBox[i].value += 1
                biji -= 1

                if biji == 0:
                    # Biji di cekungan musuh masih ada
                    if self.board.enemyBoard[i].value > 1:
                        biji = self.board.enemyBoard[i].value
                        self.board.enemyBoard[i].value = 0
                        self.board.enemyBox[i].value = 0
                i += 1
                if i == 7:
                    break
            i = 0
            
        self.checkenemyturn()


    # Gerakan musuh (mirip seperti gerakan player, tetapi milik musuh)
    def enemymove(self,i):
        biji = self.board.enemyBoard[i].value
        self.board.enemyBoard[i].value = 0
        self.board.enemyBox[i].value = 0
        
        while biji:
            while biji:
                i += 1
                if i == 7:
                    break

                self.board.enemyBoard[i].value += 1
                self.board.enemyBox[i].value += 1
                biji -= 1

                if biji == 0:
                    if self.board.enemyBoard[i].value > 1:
                        biji = self.board.enemyBoard[i].value
                        self.board.enemyBoard[i].value = 0
                        self.board.enemyBox[i].value = 0
                    else:
                        self.board.enemyBoard[7].value += self.board.myBoard[6-i].value
                        self.board.enemyBox[7].value = self.board.enemyBoard[7].value
                        self.board.myBoard[6-i].value = 0
                        self.board.myBox[6-i].value = 0
                        
            if biji > 0:
                self.board.enemyBoard[7].value += 1
                self.board.enemyBox[7].value += 1
                biji -= 1

            i = 0
            while biji:
                self.board.myBoard[i].value += 1
                self.board.myBox[i].value += 1
                biji -= 1
                if biji == 0:
                    if self.board.myBoard[i].value > 1:
                        biji = self.board.myBoard[i].value
                        self.board.myBoard[i].value = 0
                        self.board.myBox[i].value = 0
                i += 1
                if i == 7:
                    break
            i = 0
        self.checkemyturn()


    # Mengecek apakah kita bisa jalan setelah gerakan musuh
    def checkemyturn(self):
        for i in range(7):
            if self.board.myBoard[i].value > 0:
                self.game.board.turn.text="My Turn"
                self.myturn = True
                return

    # Mengecek apakah musuh bisa jalan setelah gerakan pllayer
    def checkenemyturn(self):
        for i in range(7):
            if self.board.enemyBoard[i].value > 0:
                self.game.board.turn.text="Enemy Turn"
                self.myturn = False
                return