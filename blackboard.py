import pygame as pg 
from pygame.locals import QUIT
from parameters import PARAMS
from widgets import ToolBar, Slider, Widget, Label
from scipy.ndimage import gaussian_filter1d
from functions import draw_step, smooth
from collections import OrderedDict


if __name__ == "__main__":

	pg.init()
	screen = pg.display.set_mode(
				(PARAMS["background"]["width"],
				 PARAMS["background"]["height"]))

	# add widgets
	background = Widget(0, 0, PARAMS["background"]["width"],
							  PARAMS["background"]["height"], 
							  PARAMS["color"]["k"], 
							  name="background")
	tool_bar = ToolBar(0, PARAMS["background"]["height"]-PARAMS["toolbar"]["thickness"], 
						  PARAMS["background"]["width"],
						  PARAMS["toolbar"]["thickness"],
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

	widgets = OrderedDict()
	widgets[background.name] = background
	widgets[tool_bar.name] = tool_bar

	widgets[thickness_label.name] = thickness_label
	widgets[thickness_slider.name] = thickness_slider
	widgets[thickness_slider.name + "_block"] = thickness_slider.slider_block

	widgets[smoothness_label.name] = smoothness_label
	widgets[smoothness_slider.name] = smoothness_slider
	widgets[smoothness_slider.name + "_block"] = smoothness_slider.slider_block

	# init parameters and lists
	draw_on = False
	thickness_slider_move = False
	smoothness_slider_move = False

	points_list = []
	current_points_index = -1
	start_smooth_index = 0

	current_size = PARAMS["pencil"]["size_init"]
	current_smoothness = PARAMS["smoothing"]["sigma_init"]
	sizes = []
	smoothnesses = []

	# main loop
	running = True
	while running:
		for event in pg.event.get():
			if event.type == QUIT:
				running = False

			# mouse
			if event.type == pg.MOUSEBUTTONDOWN:
				for w in widgets.values():
					if w.name == "background":
						if not w.belongs(event.pos):
							continue
					if w.name == "tool_bar":
						continue
					if w.name == "thickness":
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
					else:
						last_pos = event.pos
						points_list.append([])
						sizes.append(current_size)
						current_points_index += 1
						draw_on = True

			if event.type == pg.MOUSEBUTTONUP:
				draw_on = False
				thickness_slider_move = False
				smoothness_slider_move = False

			if event.type == pg.MOUSEMOTION:
				if not widgets["background"].belongs(event.pos):
					continue
				elif tool_bar.belongs(event.pos):
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

				elif smoothness_slider_move:
					w = widgets["smoothness"]
					block, smoothness = w.update_block_pos(event.pos)
					widgets["smoothness_block"] = block
					current_smoothness = smoothness
						
				elif draw_on:
					for i, pts in enumerate(points_list):
						[draw_step(background, PARAMS["color"]["w"], pts[j], pts[j+1], sizes[i]) for j in range(len(pts)-1)]
					
					last_pos = event.pos
					points_list[current_points_index].append(last_pos)
					start_smooth_index += 1

					if start_smooth_index >= PARAMS["smoothing"]["n_steps"]:
						points_list = smooth(background, points_list, sizes,
							current_points_index, start_smooth_index, 
							current_smoothness, mode=PARAMS["smoothing"]["mode"])
						start_smooth_index = 0

			# keyboard TODO WITH WIDGET!
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_e:
					points_list = [[]]
					current_points_index = 0
					background.fill(PARAMS["color"]["k"])

		# display widgets
		temp = pg.sprite.Group()
		[temp.add(w) for w in widgets.values()]
		temp.update()
		temp.draw(screen)
		pg.display.flip()
		del temp

	pg.quit()