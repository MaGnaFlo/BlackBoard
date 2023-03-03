import pygame as pg
from parameters import *

class Widget(pg.sprite.Sprite):
	''' General class handling widgets. '''
	def __init__(self, x, y, width, height, color, parent=None, name=""):
		super().__init__()
		self.parent = super()
		self.image = pg.Surface([width, height])
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.name = name

	def belongs(self, pos):
		''' Check if pos is on the widget. '''
		x_, y_ = pos 
		xcond = self.rect.x <= x_ <= self.rect.x + self.rect.width
		ycond = self.rect.y <= y_ <= self.rect.y + self.rect.height
		return xcond and ycond


class ToolBar(Widget):
	''' General widget for creating the tool bar. '''
	def __init__(self, x, y, width, height, color, parent=None, name=""):
		super().__init__(x, y, width, height, color)
		self.parent = super()
		self.name = name
		self.image.fill(color)


class Label(Widget):
	''' Label widget'''
	def __init__(self, x, y, text, font='Verdana', fontsize=14, color=WHITE, name=""):
		super().__init__(x, y, len(text), fontsize, color, name=name)
		self.font = pg.font.SysFont(font, fontsize)
		self.image = self.font.render(text, 1, color)
		

class Slider(Widget):
	''' Slider widget.
		Includes a slider block. 
	'''
	def __init__(self, x, y, width, height, color, init_value, min_value, max_value, parent=None, name=""):
		super().__init__(x, y, width, height, color)
		self.parent = super()
		self.image.fill(color)

		self.block_size = height * 4 # TODO: careful with the '4'. changing it changes the centering
		self.slider_block = Widget(x-self.block_size//4, y-self.block_size//4-height//2, 
									self.block_size, self.block_size, WHITE, parent)
		self.slider_block.image.fill(BLACK) # change color to parameter later
		
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
		''' Sets the position of the slider block along the slider.
		    Sets the corresponding value accordingly.'''
		x, y = pos
		if self.rect.x <= x <= self.rect.x + self.rect.width:
			self.slider_block = Widget(x-self.block_size//4, self.y-self.block_size//4-self.height//2, 
										self.block_size, self.block_size, WHITE, self.parent)
			self.value = x - self.x
			self.value = self.value / self.width * (self.max_value - self.min_value) + self.min_value
			self.value = int(self.value)

		return self.slider_block, self.value

	def belongs(self, pos):
		''' Checks if pos is in the slider.
			Essentially useful only for the block.
			Returns 2 when on the block.
		'''
		x_, y_ = pos 
		xcond = self.slider_block.rect.x <= x_ <= self.slider_block.rect.x + self.slider_block.rect.width
		ycond = self.slider_block.rect.y <= y_ <= self.slider_block.rect.y + self.slider_block.rect.height

		if xcond and ycond:
			return 2
		elif self.parent.belongs(pos):
			return 1
		else:
			return 0