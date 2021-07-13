import pygame
import math
import os
from game_constant import *
class SeedHole():
    def __init__(self,radius,x,y,value=7):
        self.border_colour = CLR_Black
        self.outer_circle_radius = radius
        self.outer_border_width = 3
        self.inner_circle_radius= self.outer_circle_radius- self.outer_border_width
        self.inner_border_width = 0
        self.normal_color=  CLR_SpicyMix
        self.hover_color=  CLR_Tan
        self.inner_colour= self.normal_color
        self.image_size=(60,60)
        self.image_sedikit = pygame.transform.scale(pygame.image.load('./client/assets/BijiSedikit.png'),self.image_size)
        self.image_sedang= pygame.transform.scale(pygame.image.load('./client/assets/BijiSedang2.png'),self.image_size)
        self.image_banyak= pygame.transform.scale(pygame.image.load('./client/assets/BijiBanyak.png'),self.image_size)
        self.image_kosong= pygame.transform.scale(pygame.image.load('./client/assets/BijiKosong.png'),self.image_size)
        self.image = self.image_sedang
        self.x=x
        self.y=y
        self.rect=self.image.get_rect(x=self.x,y=self.y)
        self.circle_center = (self.rect.x+self.rect.width/2,self.rect.y+self.rect.height/2)
        self.value=value
        self.hovered=False
        
    def update(self):
        if self.value>7:
            self.image=self.image_banyak
        elif self.value > 3:
            self.image=self.image_sedang
        elif self.value <=3 and self.value > 0:
            self.image=self.image_sedikit
        elif self.value ==0:
            self.image=self.image_kosong
        if self.hovered:
            self.inner_colour= self.hover_color
        else:
            self.inner_colour= self.normal_color
    def draw(self,screen):
        pygame.draw.circle(screen,self.border_colour, self.circle_center, self.outer_circle_radius, self.outer_border_width)
        pygame.draw.circle(screen,self.inner_colour, self.circle_center, self.inner_circle_radius, self.inner_circle_radius)
        screen.blit(self.image,self.rect)
    def iscollide(self,position):
        x1,y1 = self.circle_center
        x2,y2 = position
        x_squared = ( x2 - x1 ) * ( x2 - x1 )
        y_squared = ( y2 - y1 ) * ( y2 - y1 )
        length = math.sqrt( x_squared + y_squared )
        if length > self.outer_circle_radius:
            return False
        else:
            return True
        
    def event_handler(self,event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered= self.iscollide(event.pos)
        # if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
        #     self.value+=1

            
class ValueBox():
    def __init__(self,x,y):
        self.border_colour = CLR_Black
        self.outer_h = 60
        self.outer_w = 80
        self.outer_border_width = 1
        self.inner_h = self.outer_h-2*self.outer_border_width
        self.inner_w = self.outer_w-2*self.outer_border_width
        self.inner_border_width = 0
        self.normal_color=  CLR_SpicyMix
        self.inner_colour= self.normal_color
        self.font=pygame.font.Font(os.path.join("./client/assets","fonts",'Poppins-Bold.ttf'),40)
        self.value=7
        self.textImage=self.font.render(str(self.value), True, self.border_colour)
        self.image = self.textImage
        self.outer_x=x
        self.outer_y=y
        self.inner_x=self.outer_x+self.outer_border_width
        self.inner_y=self.outer_y+self.outer_border_width
        self.outer_rect=self.image.get_rect(x=self.outer_x,y=self.outer_y,width=self.outer_w,height=self.outer_h)
        self.inner_rect=self.image.get_rect(x=self.inner_x,y=self.inner_y,width=self.inner_w,height=self.inner_h)
        self.text_rect = self.image.get_rect(center=self.outer_rect.center)
        self.hovered=False
        
    def update(self):
        self.textImage=self.font.render(str(self.value), True, self.border_colour)
        self.image = self.textImage
        
        # if self.hovered:
        #     self.inner_colour= self.hover_color
        # else:
        #     self.inner_colour= self.normal_color
    def draw(self,screen):
        pygame.draw.rect(screen,self.border_colour, self.outer_rect,self.outer_border_width)
        pygame.draw.rect(screen,self.inner_colour, self.inner_rect,self.inner_border_width)
        screen.blit(self.image,self.text_rect)
   
    def event_handler(self,event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered= self.outer_rect.collidepoint(event.pos)


            
class ScoreBox():
    def __init__(self,value,x,y,edge):
        self.edge=edge
        self.border_colour = CLR_Black
        self.outer_h = 77
        self.outer_w = 192
        self.outer_border_width = 0
        self.normal_color=  CLR_Paarl
        self.font=pygame.font.Font(os.path.join("./client/assets","fonts",'Poppins-Bold.ttf'),33)
        self.value=value
        # self.textImage=
        self.image = self.font.render(str(self.value), True, self.border_colour)
        self.outer_x=x
        self.outer_y=y
        self.outer_rect=self.image.get_rect(x=self.outer_x,y=self.outer_y,width=self.outer_w,height=self.outer_h)
        # self.inner_rect=self.image.get_rect(x=self.inner_x,y=self.inner_y,width=self.inner_w,height=self.inner_h)
        self.text_rect = self.image.get_rect(center=self.outer_rect.center)
        self.hovered=False
    def update(self):
        self.image=self.font.render(str(self.value), True, self.border_colour)
    def draw(self,screen):
        pygame.draw.rect(screen,self.normal_color, self.outer_rect,self.outer_border_width,self.edge)
        screen.blit(self.image,self.text_rect)

    def event_handler(self,event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered= self.outer_rect.collidepoint(event.pos)
