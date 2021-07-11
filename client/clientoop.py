import socket
import sys
import pygame
import os
import array as arr
from threading import Thread
from menu import *
from game_constant import *
from match import *

# is_running=True
class Game():
    def __init__(self, *args):
        pygame.init()
        self.title="Dathon"
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
        self.clock = pygame.time.Clock()
        self.menu= Menu()
        
    def run(self):
        self.screen.fill(CLR_Parchment)
        is_running=True
        while is_running:
            screen.fill(CLR_Parchment)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running=False
                self.menu.event_handler(event)
            self.menu.update()
            self.menu.draw(self.screen)
            
            pygame.display.flip()
            clock.tick()
        pygame.quit()

class Menu():
    def __init__(self, *args):
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
        self.inputBox=InputBox(self.font['text'],470,288,500, 100, CLR_Black,CLR_White,"")
        self.title=TextStatic(self.font['title'],"Dathon",CLR_Paarl,553,87)
        self.menuState={
            "popUpCGame":False,
            "popUpJGame":False,
            "inputName": False
        }
    def draw(self,screen):
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
        
        
            



game = Game()
game.run()