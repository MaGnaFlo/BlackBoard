import pygame as pg
import pygame.gfxdraw
from parameters import PARAMS
from widgets import *
from collections import OrderedDict
from scipy.ndimage import gaussian_filter1d
import numpy as np
from pygame.locals import QUIT


def draw_step(widget, color, start, end, size):
	''' Draws the link between two points in a drawing iteration. '''
	pg.draw.circle(widget.image, color, start, size)
	pg.draw.line(widget.image, color, start, end, 2*size)

def smooth(widget, points, sizes, points_index, smooth_index, sigma, mode="gaussian"):
	''' Smoothes a portion of the drawing line.
		points_index: index of the current line (set of points).
		smooth_index: start index of the drawn line.
	'''
	# wipe
	widget.image.fill(PARAMS["background"]["color"])

	# target last points
	points_to_smooth = points[points_index]
	if len(points_to_smooth) > smooth_index:
		points_to_smooth = points_to_smooth[-smooth_index:]

	# smooth
	if mode == "gaussian":
		func = lambda x: gaussian_filter1d(x, sigma) if sigma>0 else x
	elif mode == "savgol":
		func = lambda x: savgol_filter(x, SAVGOL_WIN, SAVGOL_ORDER)
	
	x = list(np.array(points_to_smooth)[:,0])
	y = list(np.array(points_to_smooth)[:,1])
	xs = np.concatenate(([x[0]], func(x), [x[-1]]))
	ys = np.concatenate(([y[0]], func(y), [y[-1]]))
	
	# reconstruct
	points_smoothed = list(zip(xs,ys))
	points = points[:points_index] + [points[points_index][:-smooth_index] + points_smoothed]

	# redraw
	for i, pts in enumerate(points[:points_index]):
		[draw_step(widget, PARAMS["pencil"]["color"], pts[j], pts[j+1], sizes[i]) for j in range(len(pts)-1)]

	return points


def init_widgets():
	''' Creates and stores widgets in a diciotnary
		which keys depends on the (custom) name
		of the widget.
		The current implementation does not take into
		account recursive drawing of widgets.
		One has to create separate widgets for
		nested ones.
	'''

	# create all widgets
	background = ToolBar(0, 0, PARAMS["background"]["width"],
							  PARAMS["background"]["height"], 
							  PARAMS["background"]["color"], 
							  name="background")

	tool_bar = ToolBar(   PARAMS["toolbar"]["x"], 
						  PARAMS["toolbar"]["y"],
						  PARAMS["toolbar"]["width"],
						  PARAMS["toolbar"]["height"],
						  PARAMS["toolbar"]["color"], 
						  PARAMS["slider"]["block_color"], 
						  name='tool_bar')

	thickness_slider = Slider(-350, -25, PARAMS["slider"]["length"], 
							PARAMS["slider"]["thickness"],
							PARAMS["color"]["k"], 
							PARAMS["slider"]["block_color"],
							PARAMS["pencil"]["size_init"],
							1, 20, 
							parent=tool_bar, name="thickness")

	smoothness_slider = Slider(-350, 15, PARAMS["slider"]["length"], 
							PARAMS["slider"]["thickness"],
							PARAMS["color"]["k"],
							PARAMS["slider"]["block_color"],
							PARAMS["pencil"]["size_init"],
							0, 10, 
							parent=tool_bar, name="smoothness")

	eraser_button = Button(10, 15, 70, 20,
							PARAMS["color"]["w"], text="Eraser",
							parent=tool_bar,
							name="eraser_button")

	pencil_button = Button(10, -25, 70, 20,
							PARAMS["color"]["w"], text="Pencil",
							parent=tool_bar,
							name="pencil_button")

	color_palette = ColorPalette(200, -20, 30, 10, 
								 parent=tool_bar, name="palette")

	# store all widgets
	widgets = OrderedDict()

	widgets[background.name] = background
	widgets[tool_bar.name] = tool_bar

	widgets[thickness_slider.label.name+"_label"] = thickness_slider.label
	widgets[thickness_slider.name] = thickness_slider
	widgets[thickness_slider.name + "_block"] = thickness_slider.slider_block

	widgets[smoothness_slider.label.name+"_label"] = smoothness_slider.label
	widgets[smoothness_slider.name] = smoothness_slider
	widgets[smoothness_slider.name + "_block"] = smoothness_slider.slider_block

	widgets[eraser_button.name] = eraser_button
	widgets[eraser_button.name + "_text"] = eraser_button.text
	widgets[pencil_button.name] = pencil_button
	widgets[pencil_button.name + "_text"] = pencil_button.text

	widgets[color_palette.name] = color_palette
	for col in color_palette.color_surfaces:
		widgets[col.name] = col

	return widgets

def loop(screen, widgets):
	''' Main loop responsible for displaying the sprits
		and managing events
	'''
	# initialize parameters and lists
	draw_on = False
	eraser_on = False
	thickness_slider_move = False
	smoothness_slider_move = False

	points_list = []
	sizes = []
	smoothnesses = []
	colors = []
	pencil_types = []
	
	current_size = PARAMS["pencil"]["size_init"]
	current_smoothness = PARAMS["smoothing"]["sigma_init"]
	current_points_index = -1
	start_smooth_index = 0
	current_color = PARAMS["pencil"]["color"]

	# launching loop
	running = True
	while running:
		for event in pg.event.get():
			# MOUSE ##############################################
			# MOUSE DOWN
			if event.type == pg.MOUSEBUTTONDOWN:
				for w in widgets.values():
					if w.name == "background":
						if not w.belongs(event.pos):
							continue
						else:
							last_pos = event.pos
							points_list.append([])
							sizes.append(current_size)
							colors.append(PARAMS["pencil"]["color"])
							smoothnesses.append(current_smoothness)
							pencil_types.append("pencil")
							current_points_index += 1
							if eraser_on:
								pencil_types.append("eraser")
							else:
								pencil_types.append("pencil")
							draw_on = True

					elif w.name == "tool_bar":
						continue

					elif w.name == "thickness":
						belong = w.belongs(event.pos)
						if belong == 2:
							thickness_slider_move = True
						elif belong == 1:
							continue

					elif w.name == "smoothness":
						belong = w.belongs(event.pos)
						if belong == 2:
							smoothness_slider_move = True
						elif belong == 1:
							continue

					elif w.name == "eraser_button":
						if w.belongs(event.pos):
							PARAMS["pencil"]["color"] = PARAMS["background"]["color"]
							current_smoothness = 1
							eraser_on = True

					elif w.name == "pencil_button":
						if w.belongs(event.pos):
							if eraser_on and len(colors) > 1:
								found = False
								n = 0
								while not found and n < len(pencil_types):
									found = (pencil_types[-n]=="pencil")
									PARAMS["pencil"]["color"] = colors[n]
									current_smoothness = smoothnesses[n]

					elif w.name == "palette":
						if w.belongs(event.pos):
							for cell in w.color_surfaces:
								if cell.belongs(event.pos):
									PARAMS["pencil"]["color"] = cell.color


			# MOUSE UP
			if event.type == pg.MOUSEBUTTONUP:
				draw_on = False
				thickness_slider_move = False
				smoothness_slider_move = False

			# MOUSE MOVE
			if event.type == pg.MOUSEMOTION:
				if widgets["background"].belongs(event.pos):
					pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_CROSSHAIR)
				else:
					pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)

				if widgets["tool_bar"].belongs(event.pos):
					if start_smooth_index >= PARAMS["smoothing"]["n_steps"]:
						points_list = smooth(background, points_list, sizes,
							current_points_index, start_smooth_index,
							current_smoothness, mode=PARAMS["smoothing"]["mode"])
						start_smooth_index = 0

				if thickness_slider_move:
					w = widgets["thickness"]
					block, size = w.update_block_pos(event.pos)
					widgets["thickness_block"] = block
					current_size = size

				if smoothness_slider_move:
					w = widgets["smoothness"]
					block, smoothness = w.update_block_pos(event.pos)
					widgets["smoothness_block"] = block
					current_smoothness = smoothness
						
				if draw_on:
					for i, pts in enumerate(points_list):
						[draw_step(widgets["background"], colors[i], pts[j], pts[j+1], sizes[i]) for j in range(len(pts)-1)]
					
					last_pos = event.pos
					points_list[current_points_index].append(last_pos)
					start_smooth_index += 1

					if start_smooth_index >= PARAMS["smoothing"]["n_steps"]:
						points_list = smooth(widgets["background"], points_list, sizes,
							current_points_index, start_smooth_index, 
							current_smoothness, mode=PARAMS["smoothing"]["mode"])
						start_smooth_index = 0

			# KEYBOARD ##################################################
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_e:
					points_list = []
					colors = []
					sizes = []
					smoothnesses = []
					current_points_index = -1
					widgets["background"].image.fill(PARAMS["background"]["color"])

				elif event.key == pg.K_q:
					running = False

				elif event.key == pg.K_z and pg.key.get_mods() and pg.KMOD_LCTRL:
					if len(points_list) > 0:
						points_list = points_list[:-1]
						colors = colors[:-1]
						sizes = sizes[:-1]
						smoothnesses = smoothnesses[:-1]
						current_points_index -= 1
						widgets["background"].image.fill(PARAMS["background"]["color"])
						for i, pts in enumerate(points_list):
							[draw_step(widgets["background"], colors[i], pts[j], pts[j+1], sizes[i]) for j in range(len(pts)-1)]

			# GENERAL ######################################################
			elif event.type == QUIT:
				running = False

			elif event.type == pygame.VIDEORESIZE:
				# set parameters
				PARAMS["screen"]["width"] = event.w
				PARAMS["screen"]["height"] = event.h
				PARAMS["background"]["width"] = event.w
				PARAMS["background"]["height"] = event.h - 100
				PARAMS["toolbar"]["y"] = PARAMS["background"]["height"]
				PARAMS["toolbar"]["height"] = 100
				PARAMS["toolbar"]["width"] = event.w

				# re init and redraw
				widgets = init_widgets()
				for i, pts in enumerate(points_list):
					[draw_step(widgets["background"], colors[i], pts[j], pts[j+1], sizes[i]) for j in range(len(pts)-1)]

		# display widgets
		temp = pg.sprite.Group()
		[temp.add(w) for w in widgets.values()]
		temp.update()
		temp.draw(screen)
		pg.display.flip()
		del temp
