'''
Created on 2013-8-26

@author: Burke
'''

from distutils.core import setup
import py2exe

options = {
     "compressed": 1, 
     "optimize": 2,
     "ascii": 1,
     "bundle_files": 1 
    }

setup(console="snake\game.py")
# setup(
#     options = options,
#     zipfile=None,
#     console="snake\game.py"
#     )