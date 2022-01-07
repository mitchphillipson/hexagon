#!usr/bin/env python
from __future__ import division
from constants import *

import cPickle

from tile import Tile,TileHandler

class Map(object):

	def __init__(self,ImageHandler,TileHandler,file_name = './campaign.map',location = [0,0],radius = 50):
#		self.load_map(file_name)
		self.TileHandler = TileHandler
		self.size = TileHandler.get_size()
		self.radius = radius
		self.Images = ImageHandler
		self.Images.resize_images(2*radius,sqrt(3)*radius)
		self.location = [0,0]
		self.set_buffer()
		self.visible_tiles = [[0,0],[0,0]]
		self.update_visible_tiles()
		self.load_visible_tiles()
		self.draw_tiles()

	def __del__(self):
		for tile in self:
			del tile
		#del self.tiles

	def __iter__(self):
		return self.tile_grid.itervalues()
	
	def __getitem__(self,key):
		try:
			tile = self.tile_grid[key]
		except KeyError:
			tile = None
		return tile
	
	def __setitem__(self,key,value):
		self.tile_grid[key] = value

	def pixel_to_tile(self,pixel):
		"""
		The input is raw pixel information. The pixel information is tile based, not screen based. 
		"""
		wide,high = self.get_size()
		r = self.radius
		delta_x = 3/2*r
		delta_y = sqrt(3)*r
		x_values = range(wide)
		y_values = range(high)
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

	def find_visible_tiles(self, location = None):
		wide,high = self.get_size()
		s_x,s_y = self.get_location() if location is None else location
		screen = pygame.display.get_surface()
		L_x,L_y = screen.get_size()
		delta = self.get_buffer()
		x_values = range(wide)
		y_values = range(2*high)
		x1_pos = filter( lambda x: self.get_tile_center([x,0])[0] < s_x-delta,x_values)
		x1 = max(x1_pos) if x1_pos != [] else 0
		y1_pos = filter( lambda y: self.get_tile_center([0,y])[1] < s_y-delta,y_values)
		y1 = max(y1_pos) if y1_pos != [] else 0
		x2_pos = filter( lambda x: self.get_tile_center([x,0])[0] > s_x+L_x+delta,x_values)
		x2 = min(x2_pos) if x2_pos != [] else wide
		y2_pos = filter( lambda y: self.get_tile_center([0,y])[1] > s_y+L_y+delta,y_values)
		y2 = min(y2_pos) if y2_pos != [] else high
		return [[x1,y1],[x2,y2]]

	def update_visible_tiles(self):
		self.visible_tiles = self.find_visible_tiles()
	
	def load_visible_tiles(self):
		self.tile_grid = {}
		m_1,n_1 = self.visible_tiles[0]
		m_2,n_2 = self.visible_tiles[1]
		for w in xrange(m_2-m_1):
			for h in xrange(n_2-n_1):
				self.load_tile(m_1+w,n_1+h)

	def zoom(self,quantity):
		radius = self.get_radius()
		newradius = radius + quantity
		if 5<= newradius <= 120:
			self.set_radius(newradius)
			self.set_buffer()
			self.scroll([0,0])
			self.Images.resize_images(2*newradius,sqrt(3)*newradius)
			self.update_visible_tiles()
			self.load_visible_tiles()
			self.draw_tiles()

	def draw_tiles(self):
		screen = pygame.display.get_surface()
		screen.fill(WHITE)
		for tile in self:
			tile.shift(self.location)
			tile.draw(False)
		pygame.display.update()

	def scroll(self,direction,magnitude = None):
		speed = 10 if magnitude is None else magnitude
		dx,dy = direction
		old_location = [elm for elm in self.location]
		self.location[0]+=dx*speed
		self.location[1]+=dy*speed
		width,height = self.get_map_size()
		screen = pygame.display.get_surface()	
		screenWidth,screenHeight = screen.get_size()
		if self.location[0]<0:
			self.location[0] = 0
		elif self.location[0]>width - screenWidth:
			self.location[0] = width - screenWidth
		if self.location[1]<0:
			self.location[1] = 0
		elif self.location[1]> height - screenHeight:
			self.location[1] = height - screenHeight
		if width < screenWidth:
			self.location[0] = 0
		if height < screenHeight:
			self.location[1] = 0
		if old_location != self.location:
			are_new = self.find_visible_tiles()
			if are_new != self.visible_tiles:
				v00,v01 = self.visible_tiles[0]
				v10,v11 = self.visible_tiles[1]
				n00,n01 = are_new[0]
				n10,n11 = are_new[1]
				if n00 < v00 or n10 < v10:
					col_num = max(v00-n00 , v10-n10)
					for column in xrange(col_num):
						for row in xrange(n11-n01):
							self.load_tile(n00+column,n01+row)
							self.unload_tile(n10+column,n01+row)
				elif n00 > v00 or n10 > v10:
					col_num = max(n00-v00 , n10-v10)
					for column in xrange(col_num):
						for row in xrange(v11-v01):
							self.load_tile(v10+column,v01+row)
							self.unload_tile(v00+column,v01+row)
				if n01 < v01 or n11 < v11:
					row_num = max( v01-n01, v11-n11)
					for row in xrange(row_num):
						for column in xrange(n10-n00):
							self.load_tile(n00+column,n01+row)
							self.unload_tile(n00+column,n11+row)
				elif n01 > v01 or n11 > v11:
					row_num = max( n01-v01, n11-v11)
					for row in xrange(row_num):
						for column in xrange(v10-v00):
							self.load_tile(v00+column,v11+row)
							self.unload_tile(v00+column,v01+row)
				self.update_visible_tiles()
			#	self.load_visible_tiles()
			self.draw_tiles()

	def get_map_size(self):
		"""
		Returns the width and height of the map in pixels.
		"""
		radius = self.radius
		tilesWide,tilesHigh = self.get_size()
		width = int(ceil(radius*1.5*tilesWide)+radius)
		height = int(ceil(radius*sqrt(3)*tilesHigh)+radius)
		return width,height

	def get_visible_tiles(self):
		return self.visible_tiles

	def get_radius(self):
		return self.radius

	def set_radius(self,newradius):
		self.radius = newradius

	def get_size(self):
		return self.size

	def load_tile(self,w,h):
		try:
			tile = self.get_tile_info(w,h)
			self[w,h] = Tile(w,h,tile,self.radius,self.location,self.Images,self.TileHandler)
		except KeyError:
			pass

	def unload_tile(self,w,h):
		if self[w,h] is not None:
			del self.tile_grid[w,h]
		
	def exportMap(self):
		screen = pygame.display.get_surface()
		pygame.image.save(screen,"./HEY.png")

#	def load_map(self,file_name):
#		self.tiles = TileHandler(file_name)
#		self.size = self.tiles.get_size()
	
	def get_tile_info(self,w,h):
		return self.TileHandler[w,h] 

	def get_location(self):
		return self.location

	def get_buffer(self):
		return self.buffer

	def set_buffer(self):
		self.buffer = self.radius


	def get_adjacent_tiles(self,tile):
		"""
		Note that tile = [m,n], not an instance of Tile. This will return a list representing all tiles
		adjacent to the input. It will not check for armies or other obstacles, but it will filter out 
		the tiles on the side of the map.
		"""
		m,n = tile
		if m%2 == 0:
			t_adjacent_tiles = [(m-1,n-1),(m,n-1),(m+1,n-1),(m+1,n),(m,n+1),(m-1,n)]
		else:
			t_adjacent_tiles = [(m-1,n),(m,n-1),(m+1,n),(m+1,n+1),(m,n+1),(m-1,n+1)]
		out = []
		wide,high = self.get_size()
		for elm in t_adjacent_tiles:
			x,y = elm
			if 0<=x<wide and 0<=y<high:
				out.append(elm)
		return out




if __name__=='__main__':


	print "HEHE"

	













