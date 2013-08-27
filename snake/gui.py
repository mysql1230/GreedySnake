'''
Created on 2013-8-26

@author: Burke
'''

import pygame
from pygame.locals import *

class GUI():
    def __init__(self):
        pass
    
    def create_rectangle(self, surface, x1, y1, x2, y2, **args):
        pass
        
    def create_line(self, surface, x1, y1, x2, y2, **args):
        pass
    
    def create_text(self, surface, x, y, text):
        pass
    

class TkinterGUI(GUI):
    def create_rectangle(self, surface, x1, y1, x2, y2, **args):
        surface.create_rectangle(x1, y1, x2, y2, args)
        
    def create_line(self, surface, x1, y1, x2, y2, **args):
        surface.create_line(x1, y1, x2, y2, args)
    
    def create_text(self, surface, x, y, text):
        surface.create_text((x, y), text=text, font=('Arial', 28), anchor='nw')


class PygameGUI(GUI):
    def create_rectangle(self, surface, x1, y1, x2, y2, **args):
        if args['fill'] == 'red':
            color = (255, 0, 0)
        else:
            color = (0, 0, 255)
        surface.fill(color, Rect((x1, y1), (x2-x1, y2-y1)))
        pygame.draw.rect(surface, (0, 150, 150), Rect((x1, y1), (x2-x1, y2-y1)), 1)
        
    def create_line(self, surface, x1, y1, x2, y2, **args):
        pygame.draw.line(surface, (255, 0, 0), (x1, y1), (x2, y2))
        
    def create_text(self, surface, x, y, text):
        my_font = pygame.font.SysFont('arial',28)
        message = my_font.render(text, True, (0, 0, 0), (255, 255, 255))
        surface.blit(message, (x, y))
        