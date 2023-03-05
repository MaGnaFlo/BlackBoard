import pygame as pg
from parameters import PARAMS


class Widget(pg.sprite.Sprite):
	''' General class handling widgets. '''
	def __init__(self, x, y, width, height, color, parent=None, name=""):
		super().__init__()
		self.parent = super()

		self.image = pg.Surface([width, height])
		self.image.fill(color)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect.width = width
		self.rect.height = height

		self.name = name
		self.color = color

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
	''' Label widget. '''
	def __init__(self, x, y, text, font='Verdana', fontsize=14, color=PARAMS["color"]["w"], parent=None, name=""):
		if parent is not None:
			x += parent.rect.x + parent.rect.width//2
			y += parent.rect.y + parent.rect.height//2
			print(parent.name, x, y)
		super().__init__(x, y, len(text), fontsize, color, name=name)
		self.font = pg.font.SysFont(font, fontsize)
		self.image = self.font.render(text, 1, color)
		

class Button(Widget):
	''' Button widget - contains a label. '''
	def __init__(self, x, y, width, height, color, 
					text="", font='Verdana', fontsize=14, text_color=PARAMS["color"]["k"],
					parent=None, name=""):
		if parent is not None:
			x += parent.rect.x + parent.rect.width//2
			y += parent.rect.y + parent.rect.height//2
		super().__init__(x, y, width, height, color, parent=self, name=name)
		x_text = x + width//2 - pg.font.SysFont(font, fontsize).size(text)[0]//2
		self.text = Label(x_text, y, text, font=font, fontsize=fontsize, color=text_color)


class ColorPalette(Button):
	def __init__(self, x, y, cell_size=20, margin=5, parent=None, name=""):

		if parent is not None:
			x += parent.rect.x + parent.rect.width//2
			y += parent.rect.y + parent.rect.height//2

		# for now, hard code the palette in this class.
		# in the future, possibility to add colors as args and
		# deduce the palette shape and behavior.
		
		self.n_cols = 4 
		self.n_rows = 1

		self.cell_size = cell_size
		self.margin = margin
		

		self.colors = {c:PARAMS["color"][c] for c in ["k","w","r","g"]}# hard-coded

		self.color_surfaces = []
		for i, (name_, c) in enumerate(self.colors.items()):
			xc = x + i*(cell_size+margin) + margin
			# for y, I consider i=0 systematically for one row (for now).
			yc = y + 0*(cell_size+margin) + margin
			surf = Widget(xc, yc, cell_size, cell_size, c, name=name+"c="+name_)
			self.color_surfaces.append(surf)

		# build layout
		width = self.n_cols * cell_size + (self.n_cols+1)*margin
		height = self.n_rows * cell_size + (self.n_rows+1)*margin
		super().__init__(x, y, width, height, (90,0,150), name=name)


class Block(Widget):
	''' Slider block '''
	def __init__(self, x, y, width, height, color, parent=None, name=""):
		if parent is not None:
			x += parent.rect.x + parent.rect.width//2
			y += parent.rect.y + parent.rect.height//2
		super().__init__(x, y, width, height, color)


class Slider(Widget):
	''' Slider widget.
		Includes a slider block. 
	'''
	def __init__(self, x, y, width, height, color, block_color, init_value, min_value, max_value, parent=None, name=""):
		if parent is not None:
			x += parent.rect.x + parent.rect.width//2
			y += parent.rect.y + parent.rect.height//2
		super().__init__(x, y, width, height, color)

		self.parent = super()
		self.image.fill(color)

		self.block_size = height * 4 # TODO: careful with the '4'. changing it changes the centering
		self.slider_block = Block(-self.block_size//4, -self.block_size//4-height,
									self.block_size, self.block_size, 
									block_color, parent=self, name=name+"_block")
		self.block_color = block_color
		self.slider_block.image.fill(block_color) # change color to parameter later
		
		# set block pos according to init_value
		self.slider_block.rect.x = init_value / (max_value-min_value) * width + x

		self.width = width
		self.height = height
		self.x = x
		self.y = y

		self.rect.x = x
		self.rect.y = y

		self.min_value = min_value
		self.max_value = max_value
		self.value = min_value
		self.name = name

		self.label = Label(-self.width, -PARAMS["slider"]["thickness"] - 4, name, color=PARAMS["color"]["w"], 
						parent=self, name=name)


	def update_block_pos(self, pos):
		''' Sets the position of the slider block along the slider.
		    Sets the corresponding value accordingly.
		    The current implementation is only for horizontal sliders.
		'''
		x, y = pos
		if self.rect.x <= x <= self.rect.x + self.rect.width:
			self.slider_block = Widget(x-self.block_size//4, self.y-self.block_size//4-self.height//2, 
										self.block_size, self.block_size, 
										(145,140,200), self.parent)
			self.block_color = PARAMS["slider"]["block_color"]
			self.slider_block.image.fill(self.block_color)

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
 

		