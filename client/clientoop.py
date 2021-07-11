import socket
import sys
import pygame
import os
import array as arr
from threading import Thread
from menu import *
from game_constant import *
from match import *
from network import *
from enum import Enum
class GameState(Enum):
    MENU = 1
    INGAME = 2
    HTP = 3
    HS=4

# is_running=True
class Game():
    def __init__(self, *args):
        pygame.init()
        self.title="Dathon"
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
        self.clock = pygame.time.Clock()

        self.server = Server()
        self.menu= Menu(self.server)
        self.state=GameState.MENU
        self.board= Board()
        self.htp= HowToPlay()
        self.hs= HighestScore()
        
    def run(self):
        self.screen.fill(CLR_Parchment)
        is_running=True
        while is_running:
            screen.fill(CLR_Parchment)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running=False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu.buttons["cgame"].hovered:
                        self.state=GameState.INGAME
                    if self.menu.buttons["htp"].hovered:
                        self.state=GameState.HTP
                    if self.menu.trophy_rect.collidepoint(event.pos) and event.type == pygame.MOUSEBUTTONDOWN:
                        self.state=GameState.HS
                if(self.state==GameState.MENU):
                    self.menu.event_handler(event)
                if(self.state==GameState.INGAME):
                    self.board.event_handler(event)
                if(self.state==GameState.HTP):
                    self.htp.event_handler(event)
                if(self.state==GameState.HS):
                    self.hs.event_handler(event)
            if(self.state==GameState.MENU):
                self.menu.update()
                self.menu.draw(self.screen)
            if(self.state==GameState.INGAME):
                self.board.update()
                self.board.draw(self.screen)
            if(self.state==GameState.HTP):
                self.htp.update()
                self.htp.draw(self.screen)
            if(self.state==GameState.HS):
                self.hs.update()
                self.hs.draw(self.screen)
            pygame.display.flip()
            clock.tick()
        pygame.quit()

class Menu():
    def __init__(self, server, *args):
        self.server = server
        self.trophy= pygame.image.load('assets/Throphy.png').convert_alpha()
        self.trophy_rect= self.trophy.get_rect(x=1310,y=78)
        self.font={
            'title': pygame.font.Font(os.path.join("assets","fonts",'Poppins-Bold.ttf'),88),
            'text' : pygame.font.Font(os.path.join("assets","fonts",'Poppins-Bold.ttf'),36)
        }
        self.buttons={
            'cgame' : Button(self.font['text'],"Create Game",CLR_Tan,CLR_ProvincialPink,CLR_Tan,CLR_Tan,MENU_BTN_W,MENU_BTN_H,SCREEN_W/2 - MENU_BTN_W/2,444,MENU_BTN_BORDER,MENU_BTN_EDGE),
            'jgame' : Button(self.font['text'],"Join Game",CLR_Tan,CLR_ProvincialPink,CLR_Tan,CLR_Tan,MENU_BTN_W,MENU_BTN_H,SCREEN_W/2 - MENU_BTN_W/2,585,MENU_BTN_BORDER,MENU_BTN_EDGE),
            'matchmake' : Button(self.font['text'],"Matchmaking",CLR_Tan,CLR_ProvincialPink,CLR_Tan,CLR_Tan,MENU_BTN_W,MENU_BTN_H,SCREEN_W/2 - MENU_BTN_W/2,726,MENU_BTN_BORDER,MENU_BTN_EDGE),
            'htp' : TextButton(self.font['text'],"How to Play",CLR_Tan,600,867,CLR_Paarl)
        }
        self.inputBox=InputBox(self.server, self.font['text'],470,288,500, 100, CLR_Black,CLR_White,"")
        self.title=TextStatic(self.font['title'],"Dathon",CLR_Paarl,553,87)
        self.menuState="Menu"
    def draw(self,screen):
        screen.blit(self.trophy, self.trophy_rect)
        for b in self.buttons:
            self.buttons[b].draw(screen)
        self.inputBox.draw(screen)
        self.title.draw(screen)

    def update(self):
        for b in self.buttons:
            self.buttons[b].update()
        self.inputBox.update()

    def event_handler(self,event):
        for b in self.buttons:
            self.buttons[b].hover(event)
        self.inputBox.event_handler(event)

        
        # if self.menuState=="Menu":    
        #     for b in self.buttons:
        #         self.buttons[b].hover(event)

class Board(object):
    def __init__(self, *args):
        self.board= pygame.image.load('assets/DakonBoard.png').convert_alpha()
        self.myBoard=[
            SeedHole(40,806,475),
            SeedHole(40,708,475),
            SeedHole(40,610,475),
            SeedHole(40,512,475),
            SeedHole(40,414,475),
            SeedHole(40,316,475),
            SeedHole(40,218,475),
            # Score
            SeedHole(50,95,410,0)
        ]
        self.enemyBoard=[
            SeedHole(40,218,343),
            SeedHole(40,316,343),
            SeedHole(40,414,343),
            SeedHole(40,512,343),
            SeedHole(40,610,343),
            SeedHole(40,708,343),
            SeedHole(40,806,343),
            # Score
            SeedHole(50,95,410,0),
        ]
        self.myBox=[
            ValueBox(806,620),
            ValueBox(708,620),
            ValueBox(610,620),
            ValueBox(512,620),
            ValueBox(414,620),
            ValueBox(316,620),
            ValueBox(218,620),
            ScoreBox(0,1215,64,10),
        ]
        self.enemyBox=[
            ValueBox(218,198),
            ValueBox(610,198),
            ValueBox(316,198),
            ValueBox(414,198),
            ValueBox(512,198),
            ValueBox(708,198),
            ValueBox(806,198),
            ScoreBox(0,42,927,10),
        ]
    def draw(self,screen):
        screen.blit(self.board, (42,290))
        for i in range(8):
            self.myBoard[i].draw(screen)
            self.enemyBoard[i].draw(screen)
            self.myBox[i].draw(screen)
            self.enemyBox[i].draw(screen)

    def update(self):
        for i in range(8):
            self.myBoard[i].update()
            self.enemyBoard[i].update()
            self.myBox[i].update()
            self.enemyBox[i].update()    
    def event_handler(self,event):
        for i in range(7):
            self.myBoard[i].event_handler(event)
            
class HowToPlay(object):
    def __init__(self, *args):
        self.font={
            'text' : pygame.font.Font(os.path.join("assets","fonts",'Poppins-Bold.ttf'),36)
        }
        self.htp= pygame.image.load('assets/HowToPlay.png').convert_alpha()
        self.button= Button(self.font['text'],"Back to Main Menu",CLR_Tan,CLR_ProvincialPink,CLR_Tan,CLR_Tan,MENU_BTN_W,MENU_BTN_H,SCREEN_W/2 - MENU_BTN_W/2,826,MENU_BTN_BORDER,MENU_BTN_EDGE)
    def draw(self,screen):
        screen.blit(self.htp, (0,0))
        self.button.draw(screen)
    def update(self):
        self.button.update()
    def event_handler(self,event):
        self.button.hover(event)
        
                
class HighestScore(object):
    def __init__(self, *args):
        self.playerList=[
            {
                "username": "rafid",
                "score": 98
            },
            {
                "username": "rafid lagi",
                "score": 97
            },
            {
                "username": "rafid lagi2",
                "score": 97
            },
            {
                "username": "rafid lagi3",
                "score": 96
            },
            {
                "username": "rafid lagi4",
                "score": 96
            }
        ]
        self.font={
            'text' : pygame.font.Font(os.path.join("assets","fonts",'Poppins-Bold.ttf'),36),
            'score' : pygame.font.Font(os.path.join("assets","fonts",'Poppins-Regular.ttf'),40)
        }
        self.text=[]
        for i in range (5):
            # print(i)
            self.text.append({
                "rank":TextStatic(self.font['score'],str(i+1),CLR_Black,150,323+(60*i)),
                "name":TextStatic(self.font['score'],self.playerList[i]['username'],CLR_Black,387,323+(60*i)),
                "score":TextStatic(self.font['score'],str(self.playerList[i]['score']),CLR_Black,996,323+(60*i)),
            })
        # print(self.text[1]["rank"].draw(screen))      
                
        
        self.htp= pygame.image.load('assets/HighestScore.png').convert_alpha()
        self.button= Button(self.font['text'],"Back to Main Menu",CLR_Tan,CLR_ProvincialPink,CLR_Tan,CLR_Tan,MENU_BTN_W,MENU_BTN_H,SCREEN_W/2 - MENU_BTN_W/2,826,MENU_BTN_BORDER,MENU_BTN_EDGE)
    def draw(self,screen):
        screen.blit(self.htp, (0,0))
        self.button.draw(screen)
        for i in range (5):
            # self.text[0]["rank"].draw(screen)
            self.text[i]["rank"].draw(screen)
            self.text[i]["name"].draw(screen)
            self.text[i]["score"].draw(screen)
            # print(self.text[i])
            
    def update(self):
        self.button.update()
    def event_handler(self,event):
        self.button.hover(event)
        
                    



game = Game()
game.run()