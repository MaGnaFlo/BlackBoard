import pygame as pg
from parameters import *

class Widget():
	def __init__(self, surface, x, y, width, height, color):
		self.surface = surface
		self.zone = pg.Rect(x, y, width, height)
		self.surface = surface
		self.width = width
		self.color = color

	def belongs(self, pos):
		x_, y_ = pos 
		xcond = self.zone.x <= x_ <= self.zone.x + self.zone.width
		ycond = self.zone.y <= y_ <= self.zone.y + self.zone.height
		return xcond and ycond

	def draw(self): # color not used yet
		pg.draw.rect(self.surface, self.color, self.zone)


class ToolBar(Widget):
	def __init__(self, surface, x, y, width, height, color):
		super().__init__(surface, x, y, width, height, color)

	# def addSlider(self, bar_length, bar_thickness):
	# 	block_size = bar_thickness * 4
	# 	self.slider_block = pg.Rect(self.zone.x//4-block_size//2, 
	# 						   self.zone.height-(self.zone.height-self.zone.y)-block_size//2+bar_thickness//2, 
	# 							block_size, block_size)
	# 	self.block_pos = (self.slider_block.x, self.slider_block.y)

	
	
		# pg.draw.rect(self.surface, BLACK, self.slider_bar)
		# pg.draw.rect(self.surface, WHITE, self.slider_block)

class Slider(Widget):
	def __init__(self, surface, x, y, width, height, color):
		super().__init__(surface, x, y, width, height, color)
		block_size = height * 4
		self.slider_block = pg.Rect(
								x-block_size//4, y-block_size//4-height//2, block_size, block_size)

	def draw(self):
		super().draw()
		pg.draw.rect(self.surface, GREY, self.slider_block)