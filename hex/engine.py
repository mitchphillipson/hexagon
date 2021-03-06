#! usr/bin/python

#System imports

import sys

import pygame



#My imports
from hex.constants import BLACK
from hex.state import State


#Set up the screen
SIZE = WIDTH, HEIGHT = 1200, 800
pygame.display.set_caption("Mitch Rocks!")
#icon = pygame.image.load(IMAGE_ROOT_FOLDER+"icon.png")
#pygame.display.set_icon(icon)
screen = pygame.display.set_mode(SIZE)
screen.convert()
screen.fill(BLACK)
pygame.display.update()


class Events(object):

    def __init__(self):
        self.LEFTMOUSE = 1
        self.MIDDLEMOUSE = 2
        self.RIGHTMOUSE = 3
        self.SCROLLIN = 4
        self.SCROLLOUT = 5
        self.key_down = {pygame.locals.K_ESCAPE : self.on_QUIT,pygame.locals.K_RETURN : self.on_ENTER}

#        self.scroll = { K_RIGHT : SCROLL_RIGHT , K_LEFT : SCROLL_LEFT , K_UP : SCROLL_UP , K_DOWN : SCROLL_DOWN,
#                        K_d: SCROLL_RIGHT , K_a : SCROLL_LEFT , K_w : SCROLL_UP , K_s : SCROLL_DOWN}
#        self.keys =    {    K_RIGHT : False, K_LEFT : False, K_UP : False, K_DOWN : False,
#                        K_a : False, K_w : False, K_s : False, K_d : False,K_LSHIFT:False}



    def listen(self):
        eventlist= pygame.event.get()
        for event in eventlist:
            if event.type ==   pygame.locals.QUIT: 
                self.on_QUIT()
            if event.type == pygame.locals.KEYDOWN:
                self.on_key_down(event.key)
            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                self.on_mouse_down(event.pos,event.button)
            if event.type == pygame.locals.MOUSEBUTTONUP:
                self.on_mouse_up(event.pos,event.button)
            if event.type == pygame.locals.MOUSEMOTION:
                self.on_mouse_motion(event.pos,event.rel,event.buttons)
                
    def on_QUIT(self):
        pygame.quit()
        sys.exit()


    def on_ENTER(self):
        pass

    def on_key_down(self,key):
        try:
            self.key_down[key]()
        except KeyError:
            pass

    def on_mouse_down(self,position,button):
        #button = 1 -> Left
        #button = 2 -> Middle Click
        #button = 3 -> Right
        #button = 4 -> Scroll Up
        #button = 5 -> Scroll Down
        
        pass

    def on_mouse_up(self,position,button):
        pass

    def on_mouse_motion(self,position,velocity,buttons):
        pass

class Engine(Events):
    
    def __init__(self):
        super(Engine,self).__init__()
        self.state = State()
        self.mouse = (0,0)

    def play(self):
        self.clock = pygame.time.Clock()
        while 1:
            self.clock.tick(60)
            self.listen()

    def on_mouse_down(self,position,button):
        tile_key = self.state.pixel_to_tile(position)
        if tile_key is not None:
            tile = self.state[tile_key]
            self.state.select(tile)
        #    tile.add_to_tile('./hdhd.png')
        #    tile.draw()


    #def on_mouse_up(self,position,button):
    #    tile_key = self.state.pixel_to_tile(position)
    #    if tile_key is not None:
    #        tile = self.state[tile_key]
    #        tile.add_to_tile()
    #        tile.draw()

    def on_ENTER(self):
        print(self.state.grid)

























