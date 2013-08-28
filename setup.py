'''
Created on 2013-8-26

@author: Burke
'''

from distutils.core import setup
import py2exe
import sys

sys.path.append('snake')


setup(console = ["snake/game.py"],
      options = {'py2exe':{'bundle_files':1,'compressed':1,'optimize':2}},
      zipfile= None
      )