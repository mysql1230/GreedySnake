'''
Created on 2013-8-25

@author: Burke
'''
import unittest
from game import *

class Test(unittest.TestCase):

    def testInitFood(self):
        food = Food()
        self.assertEquals(food.locations, [(0,0)])
        self.assertTrue(food.alive)
        
    def testInitSnake(self):
        snake = Snake()
        self.assertEquals(snake.locations, [(0,0)])
        self.assertTrue(snake.alive)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()