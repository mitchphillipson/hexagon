#!usr/bin/env python


from constants import *
import cPickle


class TileHandler(object):

	def __init__(self,file_name):
		self.file_name = file_name
		self.size,self.tiles = cPickle.load(open(file_name,'r'))

	def __del__(self):
		pass
		#cPickle.dump([self.size,self.tiles],open(self.file_name,'w'),-1)

	def __iter__(self):
		return self.tiles.iterkeys()	

	def __getitem__(self,tile):
		return self.tiles[tile]

	def prepare_delete(self):
		for tile in self.tiles:
			if 'army' in self[tile]:
				del self[tile]['army']
			if 'highlights' in self[tile]:
				if self[tile]['highlights'] == []:
					del self[tile]['highlights']

	def modify_tile(self,tile,key,value):
		self.tiles[tile][key] = value

	def get_attribute(self,tile,key):
		try:
			return self[tile][key]
		except KeyError:
			return None
	
	def get_size(self):
		return self.size

	def reset(self,tile):
		self.tiles[tile] = {}
	


class RegularPolygon(object):
	
	def __init__(self,center,radius,numofsides):
		self.theta = 2*pi / numofsides
		self.radius = radius
		self.center = center
		self.sides = numofsides	
		self.points = self.createPoints(self.radius,self.theta,self.center,self.sides)

	def createPoints(self,radius,theta,center,sides):
		return [(radius*cos(i*theta)+center[0],radius*sin(i*theta)+center[1]) for i in xrange(sides)]
	
	def getAffinePoints(self):
		affineCenter = 	[self.radius , sqrt(3)*self.radius/2]
		return self.createPoints(self.radius,self.theta,affineCenter,self.sides)

	def getPoints(self):
		return self.points

	def changeCenterRadius(self,newCenter,newRadius):
		self.center = newCenter
		self.radius = newRadius
		self.points = self.createPoints(self.radius,self.theta,self.center,self.sides)


class Tile(RegularPolygon):
	
	def __init__(self,w,h,tile_info,radius,current_location,ImageHandler,TileHandler):
		super(Tile,self).__init__((0,0),radius,6)
		self.position = (w,h)
		self.TileHandler = TileHandler
		self.tile_info = tile_info
		self.tile_function(tile_info)
		self.ImageHandler = ImageHandler
		self.tile = None
		self.build()
		self.shift(current_location)

	def __del__(self):
		self.inverse_tile_function()

	def tile_function(self,tile_info):
		self.weight = tile_info['weight']
		self.images = {}
		for img in tile_info['images']:
				self.images[img] = True

		if 'army' in tile_info:
			self.army = tile_info['army']
		else:
			self.army = None
		if 'highlights' in tile_info:
			self.highlights = tile_info['highlights']
		else:
			self.highlights = []

	def inverse_tile_function(self):
		"""
		:(
		"""
		pos = self.position
		self.TileHandler.reset(pos)
		self.TileHandler.modify_tile(pos,'images', [img for img in self.images.keys() if self.images[img]])
		self.TileHandler.modify_tile(pos,'weight',self.weight)
		if self.army is not None:
			self.TileHandler.modify_tile(pos,'army',self.army)
		if self.highlights is not []:
			self.TileHandler.modify_tile(pos,'highlights',self.highlights)

	def build(self):
		self.make_tile()
		for img in self.ImageHandler.get_order(self.images):
			self.ImageHandler.draw(self.tile,img)

		for color in self.highlights:
			self.draw_highlight(color)

		self.draw_border()
		#self.draw_border((0,0,255,150),0)
		if self.army is not None:
			army = self.army.get_image()
	#		army = self.ImageHandler.get_image(army_image)
			self.ImageHandler.draw(self.tile,army)

		#self.draw()

	def make_tile(self):
		width,height = self.get_size()
		self.tile = pygame.Surface((width,height)).convert()
		self.tile.fill(WHITE)
		self.tile.set_colorkey(WHITE)
		self.set_rect()

	def draw(self,update = None):
		screen = pygame.display.get_surface()
		screen.blit(self.tile,self.get_location())
		if update is None:
			pygame.display.update(self.get_location())

	def clear(self):
		self.draw_border(WHITE1,0)
		self.draw_border()
		self.draw()
		self.build()
		
	def draw_border(self,color = BLACK,size = 1):
		"""
		Gets the points of the hexagon and draws them to the tile.
		"""
		points = self.getAffinePoints()
		pygame.draw.polygon(self.tile,color,points,size)

	def draw_highlight(self,color):
		width,height = self.get_size()
		tmp = pygame.Surface((width,height),flags = SRCALPHA).convert_alpha()
		points = self.getAffinePoints()
		pygame.draw.polygon(tmp,color,points,0)
		self.tile.blit(tmp,(0,0))

	def highlight(self,color):
		if color in self.highlights:
			self.highlights.remove(color)
			self.clear()
		else:
			self.highlights.append(color)
			self.build()
		

	def get_size(self):
		"""
Return the current dimensions of the tile. Typically called if the dimensions are changing.
		"""
		return 2*self.radius,sqrt(3)*self.radius

	def get_position(self):
		return self.position

	def get_rect(self):
		return self.rect

	def shift(self,new_location):
		tile_rect = self.get_rect()
		dx,dy = new_location
		self.location_rect = tile_rect.move(-dx,-dy)

	def get_location(self):
		return self.location_rect

	def set_rect(self):
		width,height = self.get_size()
		w,h = self.get_position()
		x = w*width*3/4
		y = h*height
		if w%2 == 1:
			y += height/2
		self.rect = Rect( x, y , width , height)

	def change_radius(self,newRadius):
		"""
Not hard to figure out what it does. However, it will also rebuild the tile.
		"""
		super(Tile,self).changeCenterRadius((0,0),newRadius)
		self.build()

#	def add_image(self,image):
#		self.army = image
#		self.build(1)
#		self.draw()

#	def remove_image(self,image):
#		self.army = None
#		self.clear()
#		self.draw()

	def add_army(self,army):
		self.army = army
		self.build()
		self.draw()

	def remove_army(self):
		self.army = None
		self.clear()
		self.draw()		

	def get_army(self):
		return self.army














