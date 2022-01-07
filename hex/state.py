#! usr/bin/python

from hex.constants import *

from hex.tile import Tile

class State(object):

	def __init__(self):
		self.dimension = (15,8)
		self.radius = 50
		self.grid = self.make_grid(self.dimension)
		self.screen_coords = [0,0]
		self.visible_tiles = self.find_visible_tiles()
		self.draw_tiles()

	def make_grid(self,dimension):
		w,h = dimension
		tmp = {}
		for i in range(w):
			for j in range(h):
				tmp[(i,j)] = Tile(i,j,self.radius)
		return tmp
	

	def find_visible_tiles(self):
		return [0,0,15,8]

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
		wide,high = self.get_size()
		r = self.radius
		delta_x = 3/2*r
		delta_y = sqrt(3)*r
		x_values = list(range(wide))
		y_values = list(range(high))
		x_pos,y_pos = pixel
		x1 = min(x_values,key = lambda x: abs((x+1)*delta_x-r/2-x_pos))
		x_values.remove(x1)
		x2 = min(x_values,key = lambda x: abs((x+1)*delta_x-r/2-x_pos))
		y1 = min(y_values,key = lambda y: abs((y+1)*delta_y-delta_y/2-y_pos))
		y_values.remove(y1)
		y2 = min(y_values,key = lambda y: abs((y+1)*delta_y-delta_y/2-y_pos))
		testHexes = [(x1,y1),(x1,y2),(x2,y1),(x2,y2)]
		return min(testHexes, key = lambda pt: (self.get_tile_center(pt)[0]-x_pos)**2  
											+ (self.get_tile_center(pt)[1]-y_pos)**2)


	def get_tile_center(self,tile):
		r = self.radius
		delta_x = 3/2*r
		delta_y = sqrt(3)*r
		cent_x = (tile[0]+1)*delta_x-r/2
		cent_y = (tile[1]+1)*delta_y - delta_y/2
		y_shift =  0 if tile[0]%2 == 0 else delta_y/2
		cent_y += y_shift
		return cent_x,cent_y







