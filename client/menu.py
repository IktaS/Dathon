import sys
import pygame
import os
class Button():
    def __init__(self, screen,font,text,text_def_color,text_act_color,bg_def_color,bg_act_color,rect_w,rect_h,rect_x,rect_y,border,edge,popup):
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
        self.popupObj= popup
        self.state=False

        
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
        if self.state:
            self.popupObj.update()
    def event_handler(self,event):
        self.popupObj.event_handler(event)
        if event.type == pygame.MOUSEMOTION:
            self.hovered= self.rect.collidepoint(event.pos)
            # self.state=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                self.state=True
                print(self.text)
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                self.state=False
                print(self.text)
            if event.key==pygame.K_ESCAPE:
                self.state=False
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
    def __init__(self,screen,font,text_content,text_color,x,y,active_color):
        self.font=font
        self.screen=screen
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
        self.screen.blit(self.surface, (self.x,self.y))
    def event_handler(self,event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered= self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                print(self.text)

class PopUpMenu():
    def __init__(self, screen):
        self.font=pygame.font.Font(os.path.join("assets","fonts",'Poppins-Bold.ttf'),48)
        self.font_code=pygame.font.Font(os.path.join("assets","fonts",'Poppins-Bold.ttf'),54)
        self.screen=screen
        self.sf_text1=self.font.render("This is your code", True, (0,0,0))
        self.sf_text2=self.font_code.render("ABCDEF", True, (255,255,255))
        self.sf_text3=self.font.render("Click ‘enter’ to continue", True, (0,0,0))
        
        self.bg_rect=self.sf_text2.get_rect(width=699,height=378,x=370,y=308)
        self.sf_text1_rect = self.sf_text1.get_rect(center=self.bg_rect.center,y=self.bg_rect.y+46)
        self.sf_text2_rect = self.sf_text2.get_rect(center=self.bg_rect.center,y=self.bg_rect.y+148)
        self.sf_text3_rect = self.sf_text3.get_rect(center=self.bg_rect.center,y=self.bg_rect.y+259)
        self.hovered= False
        
        
    def update(self):
        pygame.draw.rect(self.screen, (207, 166, 124,255), self.bg_rect, 0,20)
        self.screen.blit(self.sf_text1, self.sf_text1_rect)
        self.screen.blit(self.sf_text2, self.sf_text2_rect)
        self.screen.blit(self.sf_text3, self.sf_text3_rect)
        
    def event_handler(self,event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered= self.bg_rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                print("pop")
class InputBox:
    def __init__(self,screen,font, x, y, w, h,color,active_color, text=''):
        self.font=font
        self.screen=screen
        self.color_inactive = color
        self.color_active = active_color
        self.color=self.color_inactive
        self.text = text
        self.text_limit=15
        self.display = text[-self.text_limit:]
        self.txt_surface = self.font.render(self.display, True, self.color)
        self.rect=self.txt_surface.get_rect(width=w,height=h,x=x,y=y)
        self.text_rect = self.txt_surface.get_rect(center=self.rect.center)
        # self.rect = pygame.Rect(x, y, w, h)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color if self.color_active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                print("hi")
                if event.key == pygame.K_RETURN:
                    print(self.text)
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
    
    def draw(self):
        self.screen.blit(self.txt_surface, self.text_rect)
        pygame.draw.rect(self.screen, self.color, self.rect, 2,20)
