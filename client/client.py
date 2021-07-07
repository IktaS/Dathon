import socket
import sys
import pygame
import os
import array as arr
from menu import Button
from menu import TextStatic
from menu import TextButton
from menu import PopUpMenu
from game_constant import *



def main():
    pygame.init()
    title="Dathon"
    screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    screen.fill(CLR_Parchment)
    # screen.fill(CLR_BG_MENU)
    
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
    
    is_running=True
    
    while is_running:
        screen.fill(CLR_Parchment)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running=False
            btn_cgame.event_handler(event)
            btn_jgame.event_handler(event)
            text_htp.event_handler(event)
        pygame.draw.line(screen,CLR_TTL,(570,254),(874,254),1)   
        btn_cgame.update()
        btn_jgame.update()  
        text_htp.update()
        text_title.update()
        pygame.display.flip()
        clock.tick()
        # print(screen.get)
    pygame.quit()

if __name__ == '__main__':
    main()
