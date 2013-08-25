'''
Created on 2013-8-23

@author: Burke
'''

from Tkinter import *
import tkMessageBox
from random import randint

INTERVAL_TIME = 130
MAX_WIN_WIDTH = 900
MAX_WIN_HEIGHT = 600
MAX_WORLD_WIDTH = 30
MAX_WORLD_HEIGHT = 20
CELL_WIDTH = MAX_WIN_WIDTH/MAX_WORLD_WIDTH
CELL_HEIGHT = MAX_WIN_HEIGHT/MAX_WORLD_HEIGHT

class World():
    def __init__(self):
        self.entities = {}
        self.entity_id = 0
    
    def add_entity(self,entity):
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
            entity.render(surface)
    
    def process(self):
        for entity in self.entities.values():
            entity.process()
    
    
class Entity():
    def __init__(self):
        self.world = None
        self.id = 0
        self.locations = [(0,0),]
        self.speed = (0,0)
        self.alive = True
        
    def render(self, surface):
        pass
    
    def process(self):
        pass
        
        
class Snake(Entity):
    def render(self, surface):
        is_header = True
        for loc in self.locations:
            surface.create_rectangle((loc[0]-1)*CELL_WIDTH, (loc[1]-1)*CELL_HEIGHT, loc[0]*CELL_WIDTH, loc[1]*CELL_HEIGHT, fill="blue")
            if is_header:
                surface.create_line((loc[0]-1)*CELL_WIDTH, (loc[1]-1)*CELL_HEIGHT, loc[0]*CELL_WIDTH, loc[1]*CELL_HEIGHT, fill="red", dash=(4, 4))
                surface.create_line((loc[0]-1)*CELL_WIDTH, loc[1]*CELL_HEIGHT, loc[0]*CELL_WIDTH, (loc[1]-1)*CELL_HEIGHT, fill="red", dash=(4, 4))
                is_header = False
            
        
    def process(self):
        x = self.locations[0][0] + self.speed[0]
        y = self.locations[0][1] + self.speed[1]
        
        if x <= 0 or x > MAX_WORLD_WIDTH or y <= 0 or y >MAX_WORLD_HEIGHT:
            self.alive = False
        
        if self.locations.__contains__((x,y)):
            self.alive = False
        
        self.locations.insert(0, (x, y))
        self.locations.remove(self.locations[-1])
        
        for entity in self.world.entities.values():
            if entity.__class__ == Food and entity.locations.__contains__((x,y)):
                self.locations.insert(0, (x + self.speed[0], y + self.speed[1]))
                entity.alive = False
                

class Food(Entity):
    def render(self, surface):
        for loc in self.locations:
            surface.create_rectangle((loc[0]-1)*CELL_WIDTH, (loc[1]-1)*CELL_HEIGHT, loc[0]*CELL_WIDTH, loc[1]*CELL_HEIGHT, fill="red")
    
    def process(self):
        if self.alive == False:
            self.locations = [self._get_random_location()]
            self.alive = True
        
            
    def _get_random_location(self):
        locations = []
        for entity in self.world.entities.values():
            locations.append(entity.locations)
        while True:
            x = randint(1, MAX_WORLD_WIDTH)
            y = randint(1, MAX_WORLD_HEIGHT)
            if not locations.__contains__((x,y)):
                return (x,y)
    
    
def run():
    def key_pressed_handle(event):
        key = event.keysym
        if (key == 'space'):
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
        world.process()
        if snake.alive == False:
            if tkMessageBox.showwarning("Game Over!!!", "Game Over!!!"):
                exit(0)
                
        canvas.delete(ALL)
        world.render(canvas)
        win.after(INTERVAL_TIME, loop)
    
    world = World()
    snake = Snake()
    snake.locations = [(3,10),(2,10),(1,10)]
    snake.speed = (1,0)
    world.add_entity(snake)
    food = Food()
    food.locations = [(15,5)]
    world.add_entity(food)
    
    win = Tk()
    win.title('Greedy Snake')
    canvas = Canvas(win, width=MAX_WIN_WIDTH, height=MAX_WIN_HEIGHT )
    canvas.bind('<Key>', key_pressed_handle)
    canvas.create_text(480,360,text='Press Space to Start Game .....', font=('Arial',28,))
    canvas.pack()
    canvas.focus_set()
    world.render(canvas)
    win.mainloop()
    

if __name__ == '__main__':
    run()
    