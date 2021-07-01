import sys
import pygame
import os
class Button():
    def __init__(self, screen,font,text,text_def_color,text_act_color,bg_def_color,bg_act_color,rect_w,rect_h,rect_x,rect_y,border,edge):
        self.font = font
        self.text = text
        self.def_text_color = text_def_color
        self.act_text_color = text_act_color
        self.def_bg_color=bg_def_color
        self.act_bg_color=bg_act_color
        self.width=rect_w
        self.height=rect_h
        self.x=rect_x
        self.y=rect_y
        self.border=border
        self.edge=edge
        self.default_surface=font.render(text, True, text_def_color)
        self.active_surface=font.render(text, True, text_act_color)
        self.bg_default_rect = self.default_surface.get_rect(width=self.width,height=self.height,x=self.x,y=self.y)
        self.bg_active_rect = self.active_surface.get_rect(width=self.width,height=self.height,x=self.x,y=self.y)
        self.text_default_rect = self.default_surface.get_rect(center=self.bg_default_rect.center)
        self.text_active_rect = self.active_surface.get_rect(center=self.bg_active_rect.center)
        self.rect=self.bg_default_rect
        self.screen=screen
        self.hovered= False
        
    def update(self):
        # print(self.border,self.edge)
        if self.hovered:
            self.rect=self.bg_active_rect
            pygame.draw.rect(self.screen, self.act_bg_color, self.bg_active_rect,0,self.edge)
            self.screen.blit(self.active_surface, self.text_active_rect)
        else:
            self.rect=self.bg_default_rect
            pygame.draw.rect(self.screen, self.def_bg_color, self.bg_default_rect,self.border,self.edge)
            self.screen.blit(self.default_surface, self.text_default_rect)
    def event_handler(self,event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered= self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                print(self.text)
                
class TextStatic():
    def __init__(self,screen,font,text_content,text_color,x,y):
        self.font=font
        self.screen=screen
        self.text=text_content
        self.color=text_color
        self.x=x
        self.y=y
        self.surface=self.font.render(self.text, True, self.color)
        # self.rect=self.surface.get_rect(x=self.x,y=self.y)
    # Text
    def update(self):
        # print(self.color)
        self.screen.blit(self.surface, (self.x,self.y))

class TextButton():
    def __init__(self,screen,font,text_content,text_color,x,y):
        self.font=font
        self.screen=screen
        self.text=text_content
        self.color=text_color
        self.x=x
        self.y=y
        self.surface=self.font.render(self.text, True, self.color)
        self.rect=self.surface.get_rect(x=self.x,y=self.y)
    # Text
    def update(self):
        self.screen.blit(self.surface, (self.x,self.y))
    def event_handler(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print(self.text)
        