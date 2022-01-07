#!usr/bin/env python

import sys

from constants import *
from army import Army

#Movement Variables
SCROLL_RIGHT = [1,0]
SCROLL_LEFT = [-1,0]
SCROLL_UP = [0,-1]
SCROLL_DOWN = [0,1]

class Events(object):
	"""
Events(mapname)

Description of Inputs:
 1. mapname - An instance of the map class currently being used. This might be removed.

Local Variables:
 1. map - mapname.
 2. LEFTMOUSE,RIGHTMOUSE,MIDDLEMOUSE,SCROLLIN,SCROLLOUT - Key codes for these buttons.
 3. scroll - A dictionary telling how the arrow keys and asdw scroll.
 4. keys - (Bad name) A boolean dictionary telling if a key is being held down.

What this class should do:
 1. Contain only enough information to be useful by the human during AI turns.
 2. Be general enough to be subclassed by the Human player class.
	"""

	def __init__(self):
		self.SCROLL_SPEED = 10
		self.LEFTMOUSE = 1
		self.MIDDLEMOUSE = 2
		self.RIGHTMOUSE = 3
		self.SCROLLIN = 4
		self.SCROLLOUT = 5
		self.scroll = { K_RIGHT : SCROLL_RIGHT , K_LEFT : SCROLL_LEFT , K_UP : SCROLL_UP , K_DOWN : SCROLL_DOWN,
						K_d: SCROLL_RIGHT , K_a : SCROLL_LEFT , K_w : SCROLL_UP , K_s : SCROLL_DOWN}
		self.keys =	{	K_RIGHT : False, K_LEFT : False, K_UP : False, K_DOWN : False,
						K_a : False, K_w : False, K_s : False, K_d : False,K_LSHIFT:False}

	def listen(self):
		"""	
You should really never need to modify this function. It basicially listens for events to happen 
and reacts by either calling a helper function (if it's a one time key press) or updating 
self.keys to indicate that a key is being held down. Finally it calls act() so whatever keys are
being held qdown can perform their duty.
		"""
		eventlist= pygame.event.get()
		for event in eventlist:
			if event.type ==   QUIT: 
				self.on_QUIT()
			if event.type == KEYDOWN:
				if event.key in self.keys:
					self.keys[event.key] = True
				else:
					self.on_keyDown(event.key)
			if event.type == KEYUP:
				if event.key in self.keys:
					self.keys[event.key] = False
				else:
					self.on_keyUp(event.key)
			if event.type == MOUSEBUTTONDOWN:
				self.on_mouseDown(event.pos,event.button)
			if event.type == MOUSEBUTTONUP:
				self.on_mouseUp(event.pos,event.button)
			if event.type == MOUSEMOTION:
				self.on_mouseMotion(event.pos,event.rel,event.buttons)
		self.act()
		return self.return_dict
	
	def on_QUIT(self):
		self.return_dict['Quit'] = True
			
	def act(self):
		"""
		Find the keys that repeat and apply the on_keyDown function.
		"""
		map(self.on_keyDown, filter(lambda x: self.keys[x], self.keys.keys()))

	def on_keyDown(self,key):
		"""
A description of what happens when keys are pressed down. For additional keys it's safe to 
overwrite the add_keyDown function.

This should be private or protected or something.
		"""
		if key == K_ESCAPE:
			sys.exit()
		if key in self.scroll.keys():
			scroll = 2*self.SCROLL_SPEED if self.keys[K_LSHIFT] else self.SCROLL_SPEED
			self.map.scroll(self.scroll[key],scroll)
		if key == K_LSHIFT:
			self.on_LSHIFT_down()
		if key == K_TAB:
			self.on_TAB_down()
		self.add_keyDown(key)
	
	def add_keyDown(self,key):
		"""
Overwrite this function to add keys to your program. The content of this program should be 
a series of if statements such as:
		if key == KEYCODE:
			function()
		"""
		pass

	def on_keyUp(self,key):
		"""
A description of what happens when keys are released. For additional keys it's safe to 
overwrite the add_keyUp function.

This should be private or protected or something.
		"""
		if key == K_LSHIFT:
			self.on_LSHIFT_up()
		self.add_keyUp(key)

	def add_keyUp(self,key):
		"""
Overwrite this function to add keys to your program. The content of this program should be 
a series of if statements such as:
		if key == KEYCODE:
			function()
		"""
		pass

	def on_mouseDown(self,position,button):
		"""
A description of what happens when a mouse event occurs.

This should be private or protected or something.
		"""
		if button == self.LEFTMOUSE:
			self.on_leftMouseClick(position)
		if button == self.RIGHTMOUSE:
			self.on_rightMouseClick(position)
		if button == self.MIDDLEMOUSE:
			self.on_middleMouseClick(position)
		if button == self.SCROLLIN:
			self.map.zoom(10)
		if button == self.SCROLLOUT:
			self.map.zoom(-10)

	def on_leftMouseClick(self,position):
		"""
Overwrite this function to add left mouse events to your program.
		"""
		pass

	def on_rightMouseClick(self,position):
		"""
Overwrite this function to add right mouse events to your program.
		"""
		pass

	def on_middleMouseClick(self,position):
		"""
Overwrite this function to add middle mouse events to your program.
		"""
		pass

	def on_mouseUp(self,position,button):
		"""
List will be similar to on_mouseDown, but nothing is happening here :(
		"""
		pass

	def on_mouseMotion(self,position,relative,button):
		"""
List will be similar to on_mouseDown, but nothing is happening here :(
		"""
		pass

	def on_LSHIFT_down(self):
		"""
A built in method that increases the scroll speed when the left shift is held down.
		"""
		#self.map.increaseScrollSpeed(2)
		pass

	def on_LSHIFT_up(self):
		"""
A built in method that resets the scroll speed when the left shift is released.
		"""
		#self.map.resetScrollSpeed()
		pass

	def on_TAB_down(self):
		"""
A built in method that writes tile coordinates to the screen.
		"""
		#self.map.writeCoords()
		pass

class Human_Events(Events):
	
	def __init__(self):
		super(Human_Events,self).__init__()

	def on_leftMouseClick(self,position):
		tile =  self.pixel_to_tile(position)
		army = self.map[tile].get_army()
		selected_army = self.get_selected_army()
		#Make sure there is an army on the tile and the army belongs to the Player.
		if army is not None and tile in self.get_army_locations():
			#Is there an army selected? Is it this army? If either is so, don't do this.
			if selected_army is not army and selected_army is not None:
				selected_army.select()
			army.select()
		#Is an army selected and did you not click an army?
		elif tile not in self.get_army_locations() and selected_army is not None:
			selected_army.select()

	def on_rightMouseClick(self,position):
		tile =  self.pixel_to_tile(position)
		print tile
		print self.map[tile].tile_info
		tmp = self.map.get_adjacent_tiles(tile)
		
		for til in tmp:
			print self.map.TileHandler[til]

		print '-'*50

		#self.map[tile].clear()
		#self.map[tile].highlight((0,0,255,150))
		#self.map[tile].draw()

		#army_tile = self.map[tile].get_army()
		#if army_tile is not None and tile in self.get_army_locations():
		#		self.remove_army(army_tile)

	def pixel_to_tile(self,position):
		px,py = position
		lx,ly = self.map.get_location()
		return self.map.pixel_to_tile([px+lx,py+ly])

	def on_TAB_down(self):
		#out = filter(lambda x: x.is_selected(),self.armies)
		#print out
		for army in self.armies:
			print army.get_moves()
		print '-'*50

	def on_RETURN_down(self):
		self.return_dict['turn'] = False

	def add_keyDown(self,key):
		if key == K_RETURN:
			self.on_RETURN_down()

if __name__=='__main__':
	help(Events)



	










