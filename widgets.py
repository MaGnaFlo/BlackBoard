import pygame as pg
from parameters import *

class Widget(pg.sprite.Sprite):
	def __init__(self, x, y, width, height, color, parent=None):
		super().__init__()
		self.parent = super()
		self.image = pg.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.type = ""

	def belongs(self, pos):
		x_, y_ = pos 
		xcond = self.rect.x <= x_ <= self.rect.x + self.rect.width
		ycond = self.rect.y <= y_ <= self.rect.y + self.rect.height
		return xcond and ycond


class ToolBar(Widget):
	def __init__(self, x, y, width, height, color, parent=None):
		super().__init__(x, y, width, height, color)
		self.parent = super()
		self.type = "toolbar"


class Slider(Widget):
	def __init__(self, x, y, width, height, color, parent=None):
		super().__init__(x, y, width, height, color)
		self.parent = super()
		self.block_size = height * 4 # TODO: careful with the '4'. changing it changes the centering
		self.slider_block = Widget(x-self.block_size//4, y-self.block_size//4-height//2, 
									self.block_size, self.block_size, WHITE, parent)
		self.width = width
		self.height = height

		self.x = x 
		self.y = y

		self.value = 0

		self.type = "slider"

	def update_block_pos(self, pos): # set for horizontal slider
		x, y = pos
		if self.rect.x <= x <= self.rect.x + self.rect.width:
			self.slider_block.kill()
			self.slider_block = Widget(x-self.block_size//4, self.y-self.block_size//4-self.height//2, 
										self.block_size, self.block_size, WHITE, self.parent)
			self.value = self.rect.width - x + self.x
		return self.slider_block

	def belongs(self, pos):
		x_, y_ = pos 
		xcond = self.slider_block.rect.x <= x_ <= self.slider_block.rect.x + self.slider_block.rect.width
		ycond = self.slider_block.rect.y <= y_ <= self.slider_block.rect.y + self.slider_block.rect.height

		if xcond and ycond:
			print('ok')
			return 2
		elif self.parent.belongs(pos):
			print("bar")
			return 1
		else:
			print("nope")
			return 0