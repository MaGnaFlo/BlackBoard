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

	def belongs(self, pos):
		x_, y_ = pos 
		xcond = self.rect.x <= x_ <= self.rect.x + self.rect.width
		ycond = self.rect.y <= y_ <= self.rect.y + self.rect.height
		return xcond and ycond


class ToolBar(Widget):
	def __init__(self, x, y, width, height, color, parent=None):
		super().__init__(x, y, width, height, color)
		self.parent = super()


class Slider(Widget):
	def __init__(self, x, y, width, height, color, parent=None):
		super().__init__(x, y, width, height, color)
		self.parent = super()
		block_size = height * 4
		slider_block = Widget(x-block_size//4, y-block_size//4-height//2, 
									block_size, block_size, WHITE, parent)
		self.slider_block = pg.sprite.Group()
		self.slider_block.add(slider_block)

	def update(self):
		self.parent.update()