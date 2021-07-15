class Match:
    def __init__(self, game):
        self.game = game
        self.board = game.board
        self.myturn = False

    def move(self,i):
        if self.myturn == False:
            return
        
        self.game.server.send('match|move|' + str(i))
        biji = self.board.myBoard[i].value
        self.board.myBoard[i].value = 0
        self.board.myBox[i].value = 0
        # draw here

        while biji:
            while biji:
                i += 1
                if i == 7:
                    break

                self.board.myBoard[i].value += 1
                self.board.myBox[i].value += 1
                # draw here

                biji -= 1
                if biji == 0:
                    if self.board.myBoard[i].value > 1:
                        biji = self.board.myBoard[i].value
                        self.board.myBoard[i].value = 0
                        self.board.myBox[i].value = 0
                        
                        # draw here
                        
                    # jika di cekungan sendiri kosong ambil seberang musuh
                    else:
                        self.board.myBoard[7].value += self.board.enemyBoard[6-i].value
                        self.board.myBox[7].value = self.board.myBoard[7].value
                        self.board.enemyBoard[6-i].value = 0
                        self.board.enemyBox[6-i].value = 0
                        # draw here
                        
            if biji > 0:
                self.board.myBoard[7].value += 1
                self.board.myBox[7].value += 1
                biji -= 1

            i = 0
            while biji:
                self.board.enemyBoard[i].value += 1
                self.board.enemyBox[i].value += 1
                biji -= 1

                # draw here
                
                if biji == 0:
                    if self.board.enemyBoard[i].value > 1:
                        biji = self.board.enemyBoard[i].value
                        self.board.enemyBoard[i].value = 0
                        self.board.enemyBox[i].value = 0
                        
                        # draw here
                i += 1
                if i == 7:
                    break
            i = 0
            
        # self.board.draw(self.game.screen)
        self.checkenemyturn()

    def enemymove(self,i):
        
        biji = self.board.enemyBoard[i].value
        self.board.enemyBoard[i].value = 0
        self.board.enemyBox[i].value = 0
        # draw here

        while biji:
            while biji:
                i += 1
                if i == 7:
                    break

                self.board.enemyBoard[i].value += 1
                self.board.enemyBox[i].value += 1
                # draw here

                biji -= 1
                if biji == 0:
                    if self.board.enemyBoard[i].value > 1:
                        biji = self.board.enemyBoard[i].value
                        self.board.enemyBoard[i].value = 0
                        self.board.enemyBox[i].value = 0
                        
                        # draw here
                        
                    # jika di cekungan sendiri kosong ambil seberang musuh
                    else:
                        self.board.enemyBoard[7].value += self.board.myBoard[6-i].value
                        self.board.enemyBox[7].value = self.board.enemyBoard[7].value
                        self.board.myBoard[6-i].value = 0
                        self.board.myBox[6-i].value = 0
                        # draw here
                        
            if biji > 0:
                self.board.enemyBoard[7].value += 1
                self.board.enemyBox[7].value += 1
                biji -= 1

            i = 0
            while biji:
                self.board.myBoard[i].value += 1
                self.board.myBox[i].value += 1
                biji -= 1

                # draw here
                
                if biji == 0:
                    if self.board.myBoard[i].value > 1:
                        biji = self.board.myBoard[i].value
                        self.board.myBoard[i].value = 0
                        self.board.myBox[i].value = 0
                        
                        # draw here
                i += 1
                if i == 7:
                    break
            i = 0
            
        # self.board.draw(self.game.screen)
        self.checkemyturn()

    def checkemyturn(self):
        for i in range(7):
            if self.board.myBoard[i].value > 0:
                self.game.board.turn.text="My Turn"
                self.myturn = True
                return

    def checkenemyturn(self):
        for i in range(7):
            if self.board.enemyBoard[i].value > 0:
                self.game.board.turn.text="Enemy Turn"
                self.myturn = False
                return
        # self.myturn=True
    # def check_endgame(self):
    #     biji = 0
    #     for c in self.clients:
    #         biji += self.board[c][7]

    #     if biji == 98:
    #         self.endgame()
    #         return True
    #     else:
    #         return False
