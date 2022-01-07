#! usr/bin/python

from hex.constants import *


class RegularPolygon(object):
	
	def __init__(self,center,radius,numofsides):
		self.theta = 2*pi / numofsides
		self.radius = radius
		self.center = center
		self.sides = numofsides	
		self.points = self.create_points(self.radius,self.theta,self.center,self.sides)

	def create_points(self,radius,theta,center,sides):
		return [(radius*cos(i*theta)+center[0],radius*sin(i*theta)+center[1]) for i in range(sides)]
	
	def get_affine_points(self):
		affineCenter = 	[self.radius , sqrt(3)*self.radius/2]
		return self.create_points(self.radius,self.theta,affineCenter,self.sides)

	def get_points(self):
		return self.points

	def move(self,newCenter):
		self.center = newCenter
		#self.radius = newRadius
		self.points = self.createPoints(self.radius,self.theta,self.center,self.sides)

	def expand(self,newRadius):
		self.radius = newRadius
		self.points = self.createPoints(self.radius,self.theta,self.center,self.sides)

class Tile(RegularPolygon):

	def __init__(self,w,h,radius):
		super(Tile,self).__init__((0,0),radius,6)
		self.position = (w,h)
		self.tile = None
		
		self.full_image = pygame.image.load('./hex1.png').convert()		

		self.build()

	def build(self):
		self.make_tile()
		self.draw_border()


	def make_tile(self):
		width,height = self.get_size()
		self.tile = pygame.Surface((int(width),int(height))).convert()
		self.tile.fill(WHITE)
		self.tile.set_colorkey(INVISIBLE)

		image = pygame.transform.scale(self.full_image,(int(width),int(height))).convert()

		self.tile.blit(image,(0,0))

		self.set_rect()

	def draw(self,update = None):
		screen = pygame.display.get_surface()
		screen.blit(self.tile,self.get_location())
		if update is None:
			pygame.display.update(self.get_location())

	def draw_border(self,color = BLACK,size = 2):
		"""
		Gets the points of the hexagon and draws them to the tile.
		"""
		points = self.get_affine_points()
		pygame.draw.polygon(self.tile,color,points,size)

	def get_position(self):
		return self.position

	def get_size(self):
		"""
		Return the current dimensions of the tile. Typically called if the dimensions are changing.
		"""
		return 2*self.radius,sqrt(3)*self.radius

	def shift(self,new_location):
		tile_rect = self.get_rect()
		dx,dy = new_location
		self.location_rect = tile_rect.move(-dx,-dy)

	def get_location(self):
		try:
			return self.location_rect
		except AttributeError:
			self.shift((0,0))
			return self.location_rect

	def set_rect(self):
		width,height = self.get_size()
		w,h = self.get_position()
		x = w*width*3/4
		y = h*height
		if w%2 == 1:
			y += height/2
		self.rect = Rect( x, y , width , height)
	
	def get_rect(self):
		return self.rect
	

	def add_to_tile(self,image):
		width,height = self.get_size()
		nimage = pygame.image.load(image).convert()			
		nimage = pygame.transform.scale(nimage,(int(width),int(height))).convert()
		
		self.tile.blit(nimage,(0,0))





