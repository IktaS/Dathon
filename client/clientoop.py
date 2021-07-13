import socket
import sys
import pygame
import os
import array as arr
from threading import Thread
from menu import *
from game_constant import *
from match import *
from network import Server
from enum import Enum

class GameState(Enum):
    MENU = 1
    INGAME = 2
    HTP = 3
    HS=4
    CreateGame = 5
    JoinGame = 6
    Matchmake = 7

# is_running=True
class Game():
    # state=GameState.MENU
    def __init__(self, *args):
        pygame.init()
        self.state=GameState.MENU
        self.prevsstate=GameState.MENU
        self.title="Dathon"
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
        self.clock = pygame.time.Clock()
        self.server = Server(self)
        self.menu= Menu(self)
        self.htp= HowToPlay(self)
        self.hs= HighestScore(self)

    def initMatch(self):
        self.board = Board(self)
        self.match = Match(self)
        self.state = GameState.INGAME
        
    def run(self):
        self.screen.fill(CLR_Parchment)
        is_running=True
        while is_running:
            screen.fill(CLR_Parchment)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running=False
                if self.state==GameState.MENU or self.state==GameState.CreateGame or self.state==GameState.JoinGame:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # print("ko"+str(self.state))
                        if self.menu.buttons["cgame"].bg_rect.collidepoint(event.pos) and self.state==self.prevsstate:
                            self.server.send('private|make')
                            self.prevsstate=self.state
                            self.state=GameState.CreateGame
                            # self.board.updateName()
                        elif self.menu.buttons["jgame"].bg_rect.collidepoint(event.pos):
                            self.state=GameState.JoinGame
                        elif self.menu.buttons["htp"].rect.collidepoint(event.pos) and self.state==self.prevsstate:
                            self.prevsstate=self.state
                            self.state=GameState.HTP
                            # event=pygame.NOEVENT
                        elif self.menu.trophy_rect.collidepoint(event.pos) and self.state==self.prevsstate:
                            self.prevsstate=self.state
                            self.state=GameState.HS
                        elif self.menu.buttons["matchmake"].bg_rect.collidepoint(event.pos):
                            self.state=GameState.Matchmake
                            self.server.send('matchmake|join')
                        
                    self.menu.event_handler(event)
                elif(self.state==GameState.INGAME):
                    self.board.event_handler(event)
                elif(self.state==GameState.HTP):
                    self.htp.event_handler(event)
                elif(self.state==GameState.HS):
                    self.hs.event_handler(event)
            
            if(self.state==GameState.MENU or self.state==GameState.CreateGame or self.state==GameState.JoinGame):
                self.menu.update()
                self.menu.draw(self.screen)
            elif(self.state==GameState.INGAME):
                self.board.update()
                self.board.draw(self.screen)
            elif(self.state==GameState.HTP):
                self.htp.update()
                self.htp.draw(self.screen)
            elif(self.state==GameState.HS):
                self.hs.update()
                self.hs.draw(self.screen)
            pygame.display.flip()
            clock.tick(30)
        pygame.quit()

class Menu():
    def __init__(self, game, *args):
        self.game=game
        self.server = self.game.server
        self.trophy= pygame.image.load('./client/assets/Throphy.png').convert_alpha()
        self.trophy_rect= self.trophy.get_rect(x=1310,y=78)
        self.font={
            'title': pygame.font.Font(os.path.join("./client/assets","fonts",'Poppins-Bold.ttf'),88),
            'text' : pygame.font.Font(os.path.join("./client/assets","fonts",'Poppins-Bold.ttf'),36)
        }
        self.buttons={
            'cgame' : Button(self.font['text'],"Create Game",CLR_Tan,CLR_ProvincialPink,CLR_Tan,CLR_Tan,MENU_BTN_W,MENU_BTN_H,SCREEN_W/2 - MENU_BTN_W/2,444,MENU_BTN_BORDER,MENU_BTN_EDGE),
            'jgame' : Button(self.font['text'],"Join Game",CLR_Tan,CLR_ProvincialPink,CLR_Tan,CLR_Tan,MENU_BTN_W,MENU_BTN_H,SCREEN_W/2 - MENU_BTN_W/2,585,MENU_BTN_BORDER,MENU_BTN_EDGE),
            'matchmake' : Button(self.font['text'],"Matchmaking",CLR_Tan,CLR_ProvincialPink,CLR_Tan,CLR_Tan,MENU_BTN_W,MENU_BTN_H,SCREEN_W/2 - MENU_BTN_W/2,726,MENU_BTN_BORDER,MENU_BTN_EDGE),
            'htp' : TextButton(self.font['text'],"How to Play",CLR_Tan,600,867,CLR_Paarl)
        }
        self.inputBox=InputBox(self.font['text'],470,288,500, 100, CLR_Black,CLR_White,"")
        self.title=TextStatic(self.font['title'],"Dathon",CLR_Paarl,553,87)
        self.popUp= PopUpMenu(self.game)
        self.popUpJoin= PopUpInput(self.game)
        # self.inputCode=InputBox(self.font['text'],470,288,500, 100, CLR_Black,CLR_White,"")
    def draw(self,screen):
        if self.game.state==GameState.MENU:
            # print("somthing")
            pass
        screen.blit(self.trophy, self.trophy_rect)
        for b in self.buttons:
            self.buttons[b].draw(screen)
        self.inputBox.draw(screen)
        self.title.draw(screen)
        if self.game.state==GameState.CreateGame:
            self.popUp.draw(screen)
            # print("csomthing")
        if self.game.state==GameState.JoinGame:
            self.popUpJoin.draw(screen)
            # print("jsomthing")

    def update(self):
        for b in self.buttons:
            self.buttons[b].update()
        self.inputBox.update()
        if self.game.state==GameState.CreateGame:
            self.popUp.update()
        if self.game.state==GameState.JoinGame:
            self.popUpJoin.update()

    def event_handler(self,event):
        if self.game.state== GameState.MENU:
            for b in self.buttons:
                self.buttons[b].hover(event)
            self.inputBox.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if self.inputBox.active:
                    if event.key == pygame.K_RETURN:
                        self.server.send('username|update|' + self.inputBox.text)
        elif self.game.state== GameState.CreateGame:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.state=GameState.MENU
                    # print(self.game.state)
        elif self.game.state== GameState.JoinGame:
            self.popUpJoin.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # check if code valid here
                    self.game.server.send('private|join|' + self.popUpJoin.text)
                    # self.game.state=GameState.INGAME
                    # print(self.popUpJoin.text)
        
class Chat(object):
    def __init__(self,game):
        self.game=game
        self.font={
            'nama': pygame.font.Font(os.path.join("./client/assets","fonts",'Poppins-Bold.ttf'),25),
            'input' : pygame.font.Font(os.path.join("./client/assets","fonts",'Poppins-Regular.ttf'),28),
            'chat' : pygame.font.Font(os.path.join("./client/assets","fonts",'Poppins-Regular.ttf'),28)
        }
        self.card= pygame.image.load('./client/assets/Chat.png').convert_alpha()
        self.chatInputBox=InputBox(self.font['input'],1067,908,352, 73, CLR_Black,CLR_White,"")
        self.staticText=[]
        self.staticDraw=self.staticText[:4]
    def draw(self,screen):
        screen.blit(self.card, (1040,610))
        self.chatInputBox.draw(screen)
        # print(self.staticDraw)
        for i in self.staticDraw:
            # print(i)
            i["name"].draw(screen)
            i["text"].draw(screen)
            
    def update(self):
        self.chatInputBox.update()
        self.staticDraw=self.staticText[-5:]
            
    def event_handler(self,event):
        self.chatInputBox.event_handler(event)
        if event.type == pygame.KEYDOWN:
            if self.chatInputBox.active:
                if event.key == pygame.K_RETURN:
                    for i in self.staticText:
                        i["name"].y-=50
                        i["text"].y-=50
                    dict={
                        "name":TextStatic(self.font['nama'],self.game.menu.inputBox.text,CLR_Black,1067,854),
                        "text":TextStatic(self.font['chat'],self.chatInputBox.text,CLR_White,1200,854),
                    }
                    self.staticText.append(dict)
                    self.chatInputBox.text=""
                    self.chatInputBox.display=""
                    self.chatInputBox.update()
                    # self.server.send('username|update|' + self.inputBox.text)
                    
        
        
class Board(object):
    def __init__(self,game, *args):
        self.game=game
        self.chat=Chat(self.game)
        self.board= pygame.image.load('./client/assets/DakonBoard.png').convert_alpha()
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
            SeedHole(50,925,410,0),
        ]
        self.myBox=[
            ValueBox(806,620),
            ValueBox(708,620),
            ValueBox(610,620),
            ValueBox(512,620),
            ValueBox(414,620),
            ValueBox(316,620),
            ValueBox(218,620),
            ScoreBox(0,42,927,10),
        ]
        self.enemyBox=[
            ValueBox(218,198),
            ValueBox(316,198),
            ValueBox(414,198),
            ValueBox(512,198),
            ValueBox(610,198),
            ValueBox(708,198),
            ValueBox(806,198),
            ScoreBox(0,1215,64,10),
        ]
        self.font=pygame.font.Font(os.path.join("./client/assets","fonts",'Poppins-Bold.ttf'),40)
        self.textName={
            "player" : TextStatic(self.font,game.menu.inputBox.text,CLR_Black,72,875),
            "enemy" : TextStatic(self.font,"Musuh",CLR_Black,1244,157)
        }
        self.turn=TextStatic(self.font,"Turn :",CLR_Black,0,0)

    def draw(self,screen):
        screen.blit(self.board, (42,290))
        for i in range(8):
            self.myBoard[i].draw(screen)
            self.enemyBoard[i].draw(screen)
            self.myBox[i].draw(screen)
            self.enemyBox[i].draw(screen)
        for i in self.textName:
            self.textName[i].draw(screen)
        self.chat.draw(screen)
        self.turn.draw(screen)
    def update(self):
        for i in range(8):
            self.myBoard[i].update()
            self.enemyBoard[i].update()
            self.myBox[i].update()
            self.enemyBox[i].update()
        self.chat.update()
        self.turn.update()

    def updateName(self):
        for i in self.textName:
            self.textName[i].update()
                      
    def event_handler(self,event):
        for i in range(7):
            self.myBoard[i].event_handler(event)
            if event.type == pygame.MOUSEBUTTONDOWN and self.myBoard[i].hovered:
                    self.game.match.move(i)
                    # print("Jalan Gan")
        self.chat.event_handler(event)
            
class HowToPlay(object):
    def __init__(self,game, *args):
        self.game=game
        self.font={
            'text' : pygame.font.Font(os.path.join("./client/assets","fonts",'Poppins-Bold.ttf'),36)
        }
        self.htp= pygame.image.load('./client/assets/HowToPlay.png').convert_alpha()
        self.button= Button(self.font['text'],"Back to Main Menu",CLR_Tan,CLR_ProvincialPink,CLR_Tan,CLR_Tan,MENU_BTN_W,MENU_BTN_H,SCREEN_W/2 - MENU_BTN_W/2,826,MENU_BTN_BORDER,MENU_BTN_EDGE)
    def draw(self,screen):
        screen.blit(self.htp, (0,0))
        self.button.draw(screen)
    def update(self):
        self.button.update()
    def event_handler(self,event):
        self.button.hover(event)
        if event.type == pygame.MOUSEBUTTONDOWN and self.button.bg_rect.collidepoint(event.pos):
            # print("hehehe")
            # print(self.game.state)
            self.game.state=GameState.MENU
            # print(self.game.state)
        
                
class HighestScore(object):
    def __init__(self,game, *args):
        self.game=game
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
            'text' : pygame.font.Font(os.path.join("./client/assets","fonts",'Poppins-Bold.ttf'),36),
            'score' : pygame.font.Font(os.path.join("./client/assets","fonts",'Poppins-Regular.ttf'),40)
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
                
        
        self.htp= pygame.image.load('./client/assets/HighestScore.png').convert_alpha()
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
        if event.type == pygame.MOUSEBUTTONDOWN and self.button.bg_rect.collidepoint(event.pos):
            self.game.state=GameState.MENU
            # print("hehe")
        
        
                    



game = Game()
game.run()