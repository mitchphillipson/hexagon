#! usr/bin/env python

import sys

import cPickle

from constants import *
from events import Human_Events
from map import Map
from ImageHandler import ImageHandler
from tile import TileHandler


SIZE = WIDTH, HEIGHT = 1200, 800
pygame.display.set_caption("Mitch Rocks!")
icon = pygame.image.load(IMAGE_ROOT_FOLDER+"icon.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode(SIZE)
screen.convert()
screen.fill(WHITE)
pygame.display.update()


class Engine(object):

	def __init__(self,save_location,images = IMAGES):
		self.save = save_location
		self.load()
		self.clock = pygame.time.Clock()
		self.images = IMAGES
		self.ImageHandler = ImageHandler(images)
		self.map = Map(self.ImageHandler,self.TileHandler)

	def play(self):
		while 1:
			for player in self.players:
				player.reset()
				turn = True
				while turn:
					self.clock.tick(60)
					out = player.turn_loop()
					turn = out['turn']
					if out['Quit']:
						self.quit()
				player.end_turn()

	def quit(self):
		del self.map
		out = {}
		self.TileHandler.prepare_delete()
		out['TileHandler'] = self.TileHandler
		out['players'] = self.players
		cPickle.dump(out,open(self.save,'w'),-1)
		sys.exit()

	def load(self):
		game = cPickle.load(open(self.save,'r'))
		self.TileHandler = game['TileHandler']
		self.players = game['players']
		for player in self.players:
			for army in player.armies:
				self.TileHandler.modify_tile(army.get_location(),'army',army)



if __name__ == '__main__':

#	out = {}
#	
#	tiles = TileHandler('./campaign.map')
#
#	out['TileHandler'] = tiles
#
#	out['players'] = []
#
#	cPickle.dump(out,open('./save.gam','w'),-1)
	
	tmp = cPickle.load(open('./save.gam','r'))

	TileHandler = tmp['TileHandler']

	print TileHandler[0,0]








