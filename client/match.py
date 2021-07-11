import string
import random
import time

from client import *

class Match:
    def __init__(self, playerHole, playerBox, enemyHole, enemyBox, playerScoreHole, enemyScoreHole, scoreBox):
        self.playerHole = playerHole
        self.playerBox = playerBox
        self.enemyHole = enemyHole
        self.enemyBox = enemyBox
        self.playerScoreHole = playerScoreHole
        self.enemyScoreHole = enemyScoreHole
        self.scoreBox = scoreBox
        self.clock = pygame.time.Clock()

    def timer(self):
        timer = 1
        dt = 0

        while True:
            timer -= dt
            if timer <= 0:
                break
            dt = self.clock.tick(60)/1000

        return
    
    def drawPlayer(self, i):
        self.playerBox[i].update()
        self.playerHole[i].update()
        self.playerHole[i].hovered=True
        # self.timer()
        self.playerBox[i].draw()
        self.playerHole[i].draw()
        self.playerHole[i].hovered=False

    def drawEnemy(self, i):
        self.enemyBox[i].update()
        self.enemyHole[i].update()
        self.enemy[i].hovered=True
        # self.timer()
        self.enemyBox[i].draw()
        self.enemyHole[i].draw()
        self.enemyHole[i].hovered=False

    def drawScoreboard(self):
        self.playerScoreHole.update()
        self.enemyScoreHole.update()
        self.scoreBox[0].update()
        self.scoreBox[1].update()

        self.playerScoreHole.draw()
        self.enemyScoreHole.draw()
        self.scoreBox[0].draw()
        self.scoreBox[1].draw()
    
    def move(self,i):
        
        biji = self.playerHole[i].value
        self.playerHole[i].value = 0
        self.playerBox[i].value = 0
        self.drawPlayer(i)

        while biji:
            while biji:
                i += 1
                if i == 7:
                    break
                print("p"+str(i)+"--"+str(self.playerHole[i].value)+"--"+str(biji))

                self.playerHole[i].value += 1
                self.playerBox[i].value += 1
                self.drawPlayer(i)
                # self.timer()
                # time.sleep(5)
                # pygame.time.wait(10)
                biji -= 1
                if biji == 0:
                    if self.playerHole[i].value > 1:
                        biji = self.playerHole[i].value
                        self.playerHole[i].value = 0
                        self.playerBox[i].value = 0
                        self.drawPlayer(i)
                        # self.timer()
                        
                        # time.sleep(5)
                        # pygame.time.wait(10)

                    # jika di cekungan sendiri kosong ambil seberang musuh
                    else:
                        self.scoreBox[0].value += self.enemyHole[6-i].value
                        self.playerScoreHole.value = self.scoreBox[0].value
                        self.enemyHole[6-i].value = 0
                        self.enemyBox[6-i].value = 0
                        self.drawScoreboard()   
                        # self.timer()             
                # self.clock.tick(1)
            
            # if biji == 1:
            #     print("hehe")
            if biji > 0:
                self.scoreBox[0].value += 1
                self.playerScoreHole.value += 1
                biji -= 1

            i = 0
            while biji:
                i += 1
                if i == 7:
                    break

                print("e"+str(i)+"--"+str(self.enemyHole[i].value)+"--"+str(biji))
                self.enemyHole[i].value += 1
                self.enemyBox[i].value += 1
                biji -= 1

                self.drawEnemy(i)
                
                if biji == 0:
                    if self.enemyHole[i].value > 1:
                        biji = self.enemyHole[i].value
                        self.enemyHole[i].value = 0
                        self.enemyBox[i].value = 0
                        
                        self.drawEnemy(i)
                # self.clock.tick(1)
            i = 0
            # self.clock.tick(1)


        # if ( self.check_endgame()):
        #     return
        #     # Do something
        # else:
        #     self.checkturn(other_client)

    # def checkturn(self, other_client):
    #     biji = 0
    #     for i in range(7) :
    #         biji += self.board[other_client][i]
    #     if biji > 0:
    #         self.current_player(other_client)


    # def chat(self, message, client):
    #     print('room|chat|' + client.username + '|' + message, client)
    #     self.sendOther('room|chat|' + client.username + '|' + message, client)

    # def check_endgame(self):
    #     biji = 0
    #     for c in self.clients:
    #         biji += self.board[c][7]

    #     if biji == 98:
    #         self.endgame()
    #         return True
    #     else:
    #         return False
