#!usr/bin/env python
"""
Just constants and basic imports.
"""
#from __future__ import division

import pygame
#from pygame.locals import *
#import pygame.font

#pygame.init()

#from math import *


#Colors

T_GREEN = pygame.Color(0,0,255,255)
T_CLEAR = pygame.Color(0,0,0,255)

WHITE = (255,255,255)
WHITE1 = (254,254,254)
RED = (255,0,0)
BLACK = (0,0,0)
GREY = (150,150,150)
BLUE = (0,0,255)
GREEN = (0,255,0)
#TILE_INVISIBLE = (204,51,255)
INVISIBLE = (204,51,255)


#Image Files
IMAGE_ROOT_FOLDER = './Images/'
GRASS = IMAGE_ROOT_FOLDER + 'grass.png'
ARMY = IMAGE_ROOT_FOLDER + 'army.png'
ARMY1 = IMAGE_ROOT_FOLDER + 'army_1.png'


IMAGES = [GRASS,ARMY,ARMY1]
