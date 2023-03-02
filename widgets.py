import pygame as pg
from parameters import *

class ToolBar():
	def __init__(self, screen, thickness=100):
		self.bar = pg.Rect(0, h-thickness, w, thickness)
		self.thickness = thickness
		self.screen = screen
		self.xmin, self.xmax = self.bar.x, self.bar.x + self.bar.w 
		self.ymin, self.ymax = self.bar.y, self.bar.y + self.bar.h 

	def addSlider(self, bar_length, bar_thickness):
		self.slider_bar = pg.Rect(w//4, h-self.thickness//2, bar_length, bar_thickness)
		block_size = bar_thickness * 4
		self.slider_block = pg.Rect(w//4-block_size//2, 
							   h-self.thickness//2-block_size//2+bar_thickness//2, 
								block_size, block_size)
		self.block_pos = (self.slider_block.x, self.slider_block.y)

	def belongs(self, pos):
		x, y = pos 
		xcond = self.xmin <= x <= self.xmax
		ycond = self.ymin <= y <= self.ymax
		return xcond and ycond

	def draw(self): # color not used yet
		pg.draw.rect(self.screen, GREY, self.bar)
		pg.draw.rect(self.screen, BLACK, self.slider_bar)
		pg.draw.rect(self.screen, WHITE, self.slider_block)