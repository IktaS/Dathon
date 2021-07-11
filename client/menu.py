import sys
import pygame
import os
class Button():
    def __init__(self,font,text,text_def_color,text_act_color,bg_def_color,bg_act_color,rect_w,rect_h,rect_x,rect_y,border,edge):
        self.font = font
        self.text = text
        self.def_text_color = text_def_color
        self.act_text_color = text_act_color
        self.text_color=self.def_text_color
        self.def_bg_color=bg_def_color
        self.act_bg_color=bg_act_color
        self.bg_color=self.def_bg_color
        self.width=rect_w
        self.height=rect_h
        self.x=rect_x
        self.y=rect_y
        self.border=border
        self.edge=edge
        self.default_surface=font.render(text, True, text_def_color)
        self.active_surface=font.render(text, True, text_act_color)
        self.surface=self.default_surface
        self.bg_default_rect = self.default_surface.get_rect(width=self.width,height=self.height,x=self.x,y=self.y)
        self.bg_active_rect = self.active_surface.get_rect(width=self.width,height=self.height,x=self.x,y=self.y)
        self.bg_rect = self.bg_default_rect
        self.text_default_rect = self.default_surface.get_rect(center=self.bg_default_rect.center)
        self.text_active_rect = self.active_surface.get_rect(center=self.bg_active_rect.center)
        self.text_rect=self.text_default_rect
        self.hovered= False
        self.state=False

        
    def update(self):
        if self.hovered:
            self.text_rect=self.text_active_rect
            self.bg_color=self.act_bg_color
            self.surface=self.active_surface
            self.bg_rect = self.bg_active_rect
        else:
            self.text_rect=self.text_default_rect
            self.bg_color=self.def_bg_color
            self.surface=self.default_surface
            self.bg_rect = self.bg_default_rect
    def draw(self,screen):
        if self.hovered:
            pygame.draw.rect(screen, self.bg_color, self.bg_rect,0,self.edge)
        else:
            pygame.draw.rect(screen, self.bg_color, self.bg_rect,self.border,self.edge)
        screen.blit(self.surface, self.text_rect)
    def hover(self,event):
        # self.popupObj.event_handler(event)
        if event.type == pygame.MOUSEMOTION:
            self.hovered= self.bg_rect.collidepoint(event.pos)
                
class TextStatic():
    def __init__(self,font,text_content,text_color,x,y):
        self.font=font
        self.text=text_content
        self.color=text_color
        self.x=x
        self.y=y
        self.surface=self.font.render(self.text, True, self.color)
    # Text
    def draw(self,screen):
        screen.blit(self.surface, (self.x,self.y))

class TextButton():
    def __init__(self,font,text_content,text_color,x,y,active_color):
        self.font=font
        self.text= text_content
        self.color= text_color
        self.active_color = active_color
        self.x=x
        self.y=y
        self.surface=self.font.render(self.text, True, self.color)
        self.rect=self.surface.get_rect(x=self.x,y=self.y)
        self.hovered= False
    # Text
    def update(self):
        if self.hovered:
                self.surface=self.font.render(self.text, True, self.active_color)
        else:
            self.surface=self.font.render(self.text, True, self.color)
    def draw(self,screen):
        screen.blit(self.surface, (self.x,self.y))
    def hover(self,event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered= self.rect.collidepoint(event.pos)

class PopUpMenu():
    def __init__(self):
        self.font=pygame.font.Font(os.path.join("assets","fonts",'Poppins-Bold.ttf'),48)
        self.font_code=pygame.font.Font(os.path.join("assets","fonts",'Poppins-Bold.ttf'),54)
        self.sf_text1=self.font.render("This is your code", True, (0,0,0))
        self.sf_text2=self.font_code.render("ABCDEF", True, (255,255,255))
        self.sf_text3=self.font.render("Click ‘enter’ to continue", True, (0,0,0))
        
        self.bg_rect=self.sf_text2.get_rect(width=699,height=378,x=370,y=308)
        self.sf_text1_rect = self.sf_text1.get_rect(center=self.bg_rect.center,y=self.bg_rect.y+46)
        self.sf_text2_rect = self.sf_text2.get_rect(center=self.bg_rect.center,y=self.bg_rect.y+148)
        self.sf_text3_rect = self.sf_text3.get_rect(center=self.bg_rect.center,y=self.bg_rect.y+259)
        self.inputed=False
        
        
    def draw(self):
        pygame.draw.rect(self.screen, (207, 166, 124,255), self.bg_rect, 0,20)
        self.screen.blit(self.sf_text1, self.sf_text1_rect)
        self.screen.blit(self.sf_text2, self.sf_text2_rect)
        self.screen.blit(self.sf_text3, self.sf_text3_rect)
        
    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pass

class InputBox:
    def __init__(self, server, font, x, y, w, h,color,active_color, text=''):
        self.server = server

        self.font=font
        self.color_inactive = color
        self.color_active = active_color
        self.color=self.color_inactive
        self.text = text
        self.text_limit=15
        self.display = "Enter name..."
        self.txt_surface = self.font.render(self.display, True, self.color)
        self.rect=self.txt_surface.get_rect(width=w,height=h,x=x,y=y)
        self.text_rect = self.txt_surface.get_rect(center=self.rect.center)
        self.active = False

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color if self.color_active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.server.send('username|update|' + self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.display = self.text[-self.text_limit:]
                else:
                    self.text += event.unicode
                    self.display = self.text[-self.text_limit:]
                self.txt_surface = self.font.render(self.display, True, self.color)       
                self.rect=self.txt_surface.get_rect(width=self.rect.w,height=self.rect.h,x=self.rect.x,y=self.rect.y)
                self.text_rect = self.txt_surface.get_rect(center=self.rect.center)

    def update(self):
        self.display = self.text[-self.text_limit:]
    
    def draw(self,screen):
        screen.blit(self.txt_surface, self.text_rect)
        pygame.draw.rect(screen, self.color, self.rect, 2,20)
