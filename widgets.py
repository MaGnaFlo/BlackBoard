import pygame as pg
from parameters import *

class Widget(pg.sprite.Sprite):
	def __init__(self, x, y, width, height, color, parent=None, name=""):
		super().__init__()
		self.parent = super()
		self.image = pg.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.name = name

	def belongs(self, pos):
		x_, y_ = pos 
		xcond = self.rect.x <= x_ <= self.rect.x + self.rect.width
		ycond = self.rect.y <= y_ <= self.rect.y + self.rect.height
		return xcond and ycond


class ToolBar(Widget):
	def __init__(self, x, y, width, height, color, parent=None, name=""):
		super().__init__(x, y, width, height, color)
		self.parent = super()
		self.name = name


class Slider(Widget):
	def __init__(self, x, y, width, height, color, init_value, min_value, max_value, parent=None, name=""):
		super().__init__(x, y, width, height, color)
		self.parent = super()
		self.block_size = height * 4 # TODO: careful with the '4'. changing it changes the centering
		self.slider_block = Widget(x-self.block_size//4, y-self.block_size//4-height//2, 
									self.block_size, self.block_size, WHITE, parent)
		
		# set block pos according to init_value
		self.slider_block.rect.x = init_value / (max_value-min_value) * width + x

		self.width = width
		self.height = height
		self.x = x 
		self.y = y

		self.min_value = min_value
		self.max_value = max_value
		self.value = min_value
		self.name = name

	def update_block_pos(self, pos): # set for horizontal slider
		x, y = pos
		if self.rect.x <= x <= self.rect.x + self.rect.width:
			self.slider_block = Widget(x-self.block_size//4, self.y-self.block_size//4-self.height//2, 
										self.block_size, self.block_size, WHITE, self.parent)
			self.value = x - self.x
			self.value = self.value / self.width * (self.max_value - self.min_value) + self.min_value
			self.value = int(self.value)

		return self.slider_block, self.value # arbitrary value

	def belongs(self, pos):
		x_, y_ = pos 
		xcond = self.slider_block.rect.x <= x_ <= self.slider_block.rect.x + self.slider_block.rect.width
		ycond = self.slider_block.rect.y <= y_ <= self.slider_block.rect.y + self.slider_block.rect.height

		if xcond and ycond:
			return 2
		elif self.parent.belongs(pos):
			return 1
		else:
			return 0