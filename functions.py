import pygame as pg
import pygame.gfxdraw
from parameters import PARAMS
from widgets import Widget, ToolBar, Label, Slider, Button
from collections import OrderedDict
from scipy.ndimage import gaussian_filter1d
import numpy as np
from pygame.locals import QUIT

def init_widgets():
	background = ToolBar(0, 0, PARAMS["background"]["width"],
							  PARAMS["background"]["height"], 
							  PARAMS["background"]["color"], 
							  name="background")
	tool_bar = ToolBar(0, PARAMS["background"]["height"], 
						  PARAMS["background"]["width"],
						  PARAMS["toolbar"]["height"],
						  PARAMS["color"]["b"], 
						  PARAMS["slider"]["block_color"], 
						  name='tool_bar')
	
	thickness_label = Label(20, 630 - PARAMS["slider"]["thickness"] - 2, 
							"Thickness", color=PARAMS["color"]["w"], 
							name="thickness_label")

	thickness_slider = Slider(135, 630, PARAMS["slider"]["length"], 
							PARAMS["slider"]["thickness"],
							PARAMS["color"]["k"], 
							PARAMS["slider"]["block_color"],
							PARAMS["pencil"]["size_init"],
							1, 20, name="thickness")

	smoothness_label = Label(20, 670 - PARAMS["slider"]["thickness"] - 2, 
							"Smoothness", color=PARAMS["color"]["w"], 
							name="smoothness_label")

	smoothness_slider = Slider(135, 670, PARAMS["slider"]["length"], 
							PARAMS["slider"]["thickness"],
							PARAMS["color"]["k"],
							PARAMS["slider"]["block_color"],
							PARAMS["pencil"]["size_init"], 
							0, 10, name="smoothness")

	eraser_button = Button(500, 630, 70, 20,
							PARAMS["color"]["w"], text="Eraser",
							name="eraser_button")

	pencil_button = Button(500, 670, 70, 20,
							PARAMS["color"]["w"], text="Pencil",
							name="pencil_button")

	widgets = OrderedDict()

	widgets[background.name] = background
	widgets[tool_bar.name] = tool_bar

	widgets[thickness_label.name] = thickness_label
	widgets[thickness_slider.name] = thickness_slider
	widgets[thickness_slider.name + "_block"] = thickness_slider.slider_block

	widgets[smoothness_label.name] = smoothness_label
	widgets[smoothness_slider.name] = smoothness_slider
	widgets[smoothness_slider.name + "_block"] = smoothness_slider.slider_block

	widgets[eraser_button.name] = eraser_button
	widgets[eraser_button.name + "_text"] = eraser_button.text
	widgets[pencil_button.name] = pencil_button
	widgets[pencil_button.name + "_text"] = pencil_button.text

	return widgets

def loop(screen, widgets, 
			points_list, current_points_index,
			draw_on, thickness_slider_move, current_size,
			start_smooth_index,
			smoothness_slider_move, current_smoothness,
			sizes, smoothnesses, colors):
	running = True
	while running:
		for event in pg.event.get():
			# mouse
			if event.type == pg.MOUSEBUTTONDOWN:
				for w in widgets.values():
					print(w.name)
					if w.name == "background":
						if not w.belongs(event.pos):
							continue
						else:
							last_pos = event.pos
							points_list.append([])
							sizes.append(current_size)
							colors.append(PARAMS["pencil"]["color"])
							current_points_index += 1
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

					elif w.name == "pencil_button":
						if w.belongs(event.pos):
							if len(colors) > 0:
								print(colors)
								print(sizes)
								# PARAMS["pencil"]["color"] = colors[-2]
								# colors[-1]

			if event.type == pg.MOUSEBUTTONUP:
				draw_on = False
				thickness_slider_move = False
				smoothness_slider_move = False

			if event.type == pg.MOUSEMOTION:
				if not widgets["background"].belongs(event.pos):
					continue
				elif widgets["tool_bar"].belongs(event.pos):
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

			# keyboard TODO WITH WIDGET!
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_e:
					points_list = []
					current_points_index = -1
					widgets["background"].image.fill(PARAMS["color"]["k"])

				elif event.key == pg.K_q:
					running = False

			if event.type == QUIT:
				running = False

		# display widgets
		temp = pg.sprite.Group()
		[temp.add(w) for w in widgets.values()]
		temp.update()
		temp.draw(screen)
		pg.display.flip()
		del temp

def draw_step(widget, color, start, end, size):
	''' Draws the link between two points in a drawing iteration. '''
	pg.draw.line(widget.image, color, start, end, 2*size)
	pg.draw.circle(widget.image, color, start, size)

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
