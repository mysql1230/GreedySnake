'''
Created on 2013-8-23

@author: Burke
'''

from Tkinter import *
import tkMessageBox
from random import randint
from gui import *
import pygame
from pygame.locals import *

INTERVAL_TIME = 130
SCREEN_SIZE = (900, 600)
WORLD_SIZE = (30, 20)
CELL_WIDTH = SCREEN_SIZE[0]/WORLD_SIZE[0]
CELL_HEIGHT = SCREEN_SIZE[1]/WORLD_SIZE[1]

class World():
    def __init__(self):
        self.entities = {}
        self.entity_id = 0
        self.gui = TkinterGUI()
    
    def add_entity(self,entity):
        if self.get_entity(entity.id) == None:
            self.entities[self.entity_id] = entity
            entity.id = self.entity_id
            entity.world = self
            self.entity_id += 1
    
    def remove_entity(self,entity):
        del self.entities[entity.id]
        
    def get_entity(self,entity_id):
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None
        
    def render(self, surface):
        for entity in self.entities.itervalues():
            entity.gui = self.gui
            entity.render(surface)
    
    def process(self, time_passed):
        for entity in self.entities.values():
            entity.process(time_passed)
            
    
    
class Entity():
    def __init__(self):
        self.world = None
        self.id = -1
        self.locations = [(0., 0.),]
        self.speed = (0., 0.)
        self.alive = True
        self.gui = TkinterGUI()
        self.passed_time = 0
        
    def render(self, surface):
        pass
    
    def process(self, time_passed):
        pass
        
        
class Snake(Entity):
    def render(self, surface):
        is_header = True
        for loc in self.locations:
            self.gui.create_rectangle(surface, (loc[0]-1)*CELL_WIDTH, (loc[1]-1)*CELL_HEIGHT, loc[0]*CELL_WIDTH, loc[1]*CELL_HEIGHT, fill="blue")
            if is_header:
                self.gui.create_line(surface, (loc[0]-1)*CELL_WIDTH, (loc[1]-1)*CELL_HEIGHT, loc[0]*CELL_WIDTH, loc[1]*CELL_HEIGHT, fill="red", dash=(4, 4))
                self.gui.create_line(surface, (loc[0]-1)*CELL_WIDTH, loc[1]*CELL_HEIGHT, loc[0]*CELL_WIDTH, (loc[1]-1)*CELL_HEIGHT, fill="red", dash=(4, 4))
                is_header = False
            
        
    def process(self, time_passed):
        self.passed_time += time_passed
        
        if self.passed_time < INTERVAL_TIME:
            return
        
        self.passed_time = 0
        x = self.locations[0][0] + self.speed[0]
        y = self.locations[0][1] + self.speed[1]
        
        if x <= 0 or x > WORLD_SIZE[0] or y <= 0 or y > WORLD_SIZE[1]:
            self.alive = False
            return
        
        if self.locations.__contains__((x,y)):
            self.alive = False
            return
        
        self.locations.insert(0, (x, y))
        
        for entity in self.world.entities.values():
            if entity.__class__ == Food and entity.locations.__contains__((x,y)):
                entity.alive = False
                return
            
        self.locations.remove(self.locations[-1])
                

class Food(Entity):
    def render(self, surface):
        for loc in self.locations:
            self.gui.create_rectangle(surface, (loc[0]-1)*CELL_WIDTH, (loc[1]-1)*CELL_HEIGHT, loc[0]*CELL_WIDTH, loc[1]*CELL_HEIGHT, fill="red")
    
    def process(self, time_passed):
        if self.alive == False:
            self.locations = [self._get_random_location()]
            self.alive = True
        
            
    def _get_random_location(self):
        locations = []
        for entity in self.world.entities.values():
            locations.extend(entity.locations)
        while True:
            x = randint(1, WORLD_SIZE[0])
            y = randint(1, WORLD_SIZE[1])
            if not locations.__contains__((x,y)):
                return (x,y)


class Message(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.text = ''
        
    def render(self, surface):
        for loc in self.locations:
            self.gui.create_text(surface, (loc[0]-1)*CELL_WIDTH, (loc[1]-1)*CELL_HEIGHT, self.text)
    
    
def Tkinter_mainloop():
    def key_pressed_handle(event):
        key = event.keysym
        if (key == 'space'):
            world.remove_entity(tip_message)
            win.after(INTERVAL_TIME, loop)
        elif (key == 'Up' and snake.speed[0] != 0) :
            snake.speed = (0,-1)
        elif (key == 'Down' and snake.speed[0] != 0):
            snake.speed = (0,1)
        elif (key == 'Left' and snake.speed[1] != 0):
            snake.speed = (-1,0)
        elif (key == 'Right' and snake.speed[1] != 0):
            snake.speed = (1,0)
        
    def loop():
        world.process(INTERVAL_TIME)
        if snake.alive == False:
            if tkMessageBox.showwarning("Game Over!!!", "Game Over!!!"):
                exit(0)
                
        canvas.delete(ALL)
        world.render(canvas)
        win.after(INTERVAL_TIME, loop)
    
    win = Tk()
    canvas = Canvas(win, width=SCREEN_SIZE[0], height=SCREEN_SIZE[1] )
    canvas.bind('<Key>', key_pressed_handle)
    canvas.pack()
    canvas.focus_set()
    win.title('Greedy Snake')
    world.render(canvas)
    win.mainloop()
    
    
def Pygame_mainloop():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    clock = pygame.time.Clock()
    is_ready = False
     
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
        
        screen.fill((255,255,255))
        pressed_keys = pygame.key.get_pressed()
        
        if is_ready:
            if pressed_keys[K_LEFT] and snake.speed[1] != 0:
                snake.speed = (-1,0)
            elif pressed_keys[K_RIGHT] and snake.speed[1] != 0:
                snake.speed = (1,0)
            elif pressed_keys[K_UP] and snake.speed[0] != 0:
                snake.speed = (0,-1)
            elif pressed_keys[K_DOWN] and snake.speed[0] != 0:
                snake.speed = (0,1)
            
            time_passed = clock.tick(30)
            
            if snake.alive:
                world.process(time_passed)
            if snake.alive == False:
                world.add_entity(tip_message)
                if pressed_keys[K_SPACE]:
                    pygame.quit()
                    sys.exit(0)
        else:
            if pressed_keys[K_SPACE]:
                is_ready = True
                world.remove_entity(tip_message)
      
        world.render(screen)
        pygame.display.update()


if __name__ == '__main__':
    world = World()
    snake = Snake()
    snake.locations = [(3,10),(2,10),(1,10)]
    snake.speed = (1,0)
    world.add_entity(snake)
    food = Food()
    food.locations = [(15,5)]
    world.add_entity(food)
    tip_message = Message()
    tip_message.text = 'Press Space to Continue .....'
    tip_message.locations = [(10, 15)]
    world.add_entity(tip_message)
    
    # uncomment next line to use Tkinter GUI Interface 
#     Tkinter_mainloop()
    
    # Below is Pygame GUI ...
    pygame_gui = PygameGUI()
    world.gui = pygame_gui
    Pygame_mainloop()

