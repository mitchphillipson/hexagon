#! usr/bin/python

from hex.constants import *

from hex.tile import Tile

from math import sqrt

class State(object):

    def __init__(self):
        self.dimension = (40,25)#(15,8)
        self.radius = 20
        self.make_grid(self.dimension)
        self.screen_coords = [0,0]
        self.visible_tiles = self.find_visible_tiles()
        self.draw_tiles()

        self.tile = None

    def make_grid(self,dimension):
        w,h = dimension
        self.grid = {}
        for i in range(w):
            for j in range(h):
                self.grid[(i,j)] = Tile(i,j,self.radius,self.get_tile_center((i,j)))
        
    

    def select(self,tile):
        "In -> Instance of Tile class"
        
        if self.tile is not None:
            self.tile.add_to_tile()
            self.tile.draw()
        self.tile = tile
        tile.add_to_tile('./hdhd.png')
        tile.draw()

    def find_visible_tiles(self):
        x,y = self.dimension
        return [0,0,x,y]

    def draw_tiles(self):
        w1,h1,w2,h2 = self.visible_tiles
        for i in range(w2-w1):
            for j in range(h2-h1):
                self.grid[(w1+i,h1+j)].draw()

    def get_size(self):
        return self.dimension

    def __getitem__(self,key):
        return self.grid[key]

    def pixel_to_tile(self,pixel):
        """
        The input is raw pixel information. The pixel information is tile based, not screen based. 
        """
        L = [tile for tile in self.grid if pixel in self[tile]]

        if L != []:
            return L[0]    
        return None
        


    def get_tile_center(self,tile):
        r = self.radius
        delta_x = 3/2*r
        delta_y = sqrt(3)*r
        cent_x = (tile[0]+1)*delta_x-r/2
        cent_y = (tile[1]+1)*delta_y - delta_y/2
        y_shift =  0 if tile[0]%2 == 0 else delta_y/2
        cent_y += y_shift
        return cent_x,cent_y







