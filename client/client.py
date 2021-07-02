#import library
import pygame

#initialize
pygame.init()
# screen = pygame.display.set_mode((1440, 1024))
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
pygame.display.set_caption("Dathon")

#define RGB value
white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font('assets/fonts/Poppins-Medium.ttf', 54)
title = font.render('Dathon', True, black)
title_dest = (620, 48)

dakon_board = pygame.image.load("assets/DakonBoard.png")
dakon_board_dest = (42, 290)

while True:
    screen.fill(white)
   
    screen.blit(title, title_dest)
    screen.blit(dakon_board, dakon_board_dest)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()
