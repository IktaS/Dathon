import socket
import sys
import pygame
import os
import array as arr
from menu import Button
from menu import TextStatic
from menu import TextButton
from menu import PopUpMenu
from menu import InputBox
from game import SeedHole
from game import ValueBox
from game import ScoreBox
from game_constant import *

pygame.init()
title="Dathon"
screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
pygame.display.set_caption(title)
clock = pygame.time.Clock()
# is_running=True

def game():
    screen.fill(CLR_Parchment)
    is_running=True
    board= pygame.image.load('assets/DakonBoard.png').convert_alpha()
    board_pos=(42,290)
    
    playerScoreHole=SeedHole(screen,50,95,410,0)
    enemyScoreHole=SeedHole(screen,50,925,410,0)
    playerHole=[
        SeedHole(screen,40,806,475),
        SeedHole(screen,40,708,475),
        SeedHole(screen,40,610,475),
        SeedHole(screen,40,512,475),
        SeedHole(screen,40,414,475),
        SeedHole(screen,40,316,475),
        SeedHole(screen,40,218,475),
        # playerScoreHole
    ]
    enemyHole=[
        SeedHole(screen,40,218,343),
        SeedHole(screen,40,316,343),
        SeedHole(screen,40,414,343),
        SeedHole(screen,40,512,343),
        SeedHole(screen,40,610,343),
        SeedHole(screen,40,708,343),
        SeedHole(screen,40,806,343),
        # enemyScoreHole
    ]
    scoreBox=[
        ScoreBox(screen,str(0),1215,64,10),
        ScoreBox(screen,str(0),42,927,10),
    ]
    playerBox=[
        ValueBox(screen,806,620),
        ValueBox(screen,708,620),
        ValueBox(screen,610,620),
        ValueBox(screen,512,620),
        ValueBox(screen,414,620),
        ValueBox(screen,316,620),
        ValueBox(screen,218,620),
    ]
    enemyBox=[
        ValueBox(screen,806,198),
        ValueBox(screen,708,198),
        ValueBox(screen,610,198),
        ValueBox(screen,512,198),
        ValueBox(screen,414,198),
        ValueBox(screen,316,198),
        ValueBox(screen,218,198),
    ]
    
    
    
    while is_running:
        screen.fill(CLR_Parchment)
        screen.blit(board, board_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running=False
            for hole in playerHole:
                hole.event_handler(event)
        for i in range(7):
            playerBox[i].value=playerHole[i].value
            enemyBox[i].value=enemyHole[i].value
        playerScoreHole.update()
        enemyScoreHole.update()
        
        for hole in playerHole:
            hole.update()
        for hole in enemyHole:
            hole.update()
        for box in scoreBox:
            box.update()
        for hole in playerBox:
            hole.update()
        for hole in enemyBox:
            hole.update()
        playerScoreHole.draw()
        enemyScoreHole.draw()
        for hole in playerHole:
            hole.draw()
            
        for hole in enemyHole:
            hole.draw()
        for box in scoreBox:
            box.draw()
        for hole in playerBox:
            hole.draw()
        for hole in enemyBox:
            hole.draw()
        pygame.display.flip()
        clock.tick()
    pygame.quit()

def waiting():
    screen.fill(CLR_Parchment)
    is_running=True
    while is_running:
        screen.fill(CLR_Parchment)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running=False
            
        pygame.display.flip()
        clock.tick()
    pygame.quit()

def menu():
    screen.fill(CLR_Parchment)
    # screen.fill(CLR_BG_MENU)
    is_running=True
    # Menu
    title_font=pygame.font.Font(os.path.join("assets","fonts",'Poppins-Bold.ttf'),88)
    menu_font=pygame.font.Font(os.path.join("assets","fonts",'Poppins-Bold.ttf'),36)
    menu=["Create Game","Join Game","How to Play?"]
    text_title = TextStatic(screen,title_font,title,CLR_Paarl,553,128)
    pu_cgame=PopUpMenu(screen)
    pu_jgame=PopUpMenu(screen)
    btn_cgame = Button(screen,menu_font,menu[0],CLR_Tan,CLR_ProvincialPink,CLR_Tan,CLR_Tan,MENU_BTN_W,MENU_BTN_H,SCREEN_W/2 - MENU_BTN_W/2,585,MENU_BTN_BORDER,MENU_BTN_EDGE,pu_cgame)
    btn_jgame = Button(screen,menu_font,menu[1],CLR_Tan,CLR_ProvincialPink,CLR_Tan,CLR_Tan,MENU_BTN_W,MENU_BTN_H,SCREEN_W/2 - MENU_BTN_W/2,726,MENU_BTN_BORDER,MENU_BTN_EDGE,pu_jgame)
    text_htp = TextButton(screen,menu_font,menu[2],CLR_Tan,600,867,CLR_Paarl)
    input_box1 = InputBox(screen,menu_font,470,370,500, 100, CLR_Black,CLR_White,"")

    menuState={
        "inMenu":True,
        "popUpCGame":False,
        "popUpJGame":False,
        "inputName": False
    }
    while is_running:
        screen.fill(CLR_Parchment)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                is_running=False
            if menuState["inMenu"]:
                menuState["popUpCGame"]=btn_cgame.event_handler(event)
                menuState["popUpJGame"]=btn_jgame.event_handler(event)
                text_htp.event_handler(event)
                input_box1.handle_event(event)
                if menuState["popUpCGame"] or menuState["popUpJGame"]:
                    menuState["inMenu"]=False
            if menuState["popUpCGame"]:
                game()
                menuState["popUpCGame"]=pu_cgame.event_handler(event)
                if not menuState["popUpCGame"]:
                    menuState["inMenu"]=True
            if menuState["popUpJGame"]: 
                menuState["popUpJGame"]=pu_jgame.event_handler(event)
                if not menuState["popUpJGame"]:
                    menuState["inMenu"]=True
                
        
        
        text_title.update()
        input_box1.update()
        btn_cgame.update()
        btn_jgame.update()  
        text_htp.update()
        
        pygame.draw.line(screen,CLR_TTL,(570,254),(874,254),1)   
        input_box1.draw()
        btn_cgame.draw()    
        btn_jgame.draw()
        if menuState["popUpCGame"]:
            pu_cgame.draw()
        if menuState["popUpJGame"]: 
            pu_jgame.draw()
          
        pygame.display.flip()
        pygame.display.update()
        clock.tick()
    pygame.quit()

if __name__ == '__main__':
    menu()
