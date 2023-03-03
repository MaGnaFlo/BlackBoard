import pygame as pg 
from pygame.locals import QUIT
from parameters import *
from widgets import ToolBar, Slider, Widget
from scipy.ndimage import gaussian_filter1d
from functions import *


if __name__ == "__main__":

	pg.init()
	screen = pg.display.set_mode((W,H))

	background = Widget(0, 0, W, H, BLACK, name="background")

	tool_bar = ToolBar(0, H-TOOLBAR_THICKNESS, W, TOOLBAR_THICKNESS, GREY, name='tool_bar')
	thickness_slider = Slider(50, 630, SLIDER_LENGTH, SLIDER_THICKNESS, BLACK, 1, 50, name="thickness")
	smoothness_slider = Slider(50, 670, SLIDER_LENGTH, SLIDER_THICKNESS, BLACK, 50, 200, name="smoothness")

	# widgets = pg.sprite.Group()
	widgets = {}
	widgets[background.name] = background
	widgets[tool_bar.name] = tool_bar
	widgets[thickness_slider.name] = thickness_slider
	widgets[thickness_slider.name + "_block"] = thickness_slider.slider_block
	widgets[smoothness_slider.name] = smoothness_slider
	widgets[smoothness_slider.name + "_block"] = smoothness_slider.slider_block

	draw_on = False
	thickness_slider_move = False
	smoothness_slider_move = False

	points_list = []
	current_points_index = -1
	start_smooth_index = 0

	current_size = SIZE
	current_smoothness = N_POINTS_SMOOTH
	sizes = []
	smoothnesses = []

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
					if start_smooth_index >= current_smoothness:
						points_list = smooth_step(background, points_list, sizes,
							current_points_index, start_smooth_index,
							sizes[current_points_index], mode=SMOOTH_MODE)
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
						[draw_step(background, WHITE, pts[j], pts[j+1], sizes[i]) for j in range(len(pts)-1)]
					
					last_pos = event.pos
					points_list[current_points_index].append(last_pos)
					start_smooth_index += 1

					if start_smooth_index >= current_smoothness:
						points_list = smooth_step(background, points_list, sizes,
							current_points_index, start_smooth_index, 
							sizes[current_points_index], mode=SMOOTH_MODE)
						start_smooth_index = 0

			# keyboard TODO WITH WIDGET!
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_e:
					points_list = [[]]
					current_points_index = 0
					background.fill(BLACK)

		temp = pg.sprite.Group()
		[temp.add(w) for w in widgets.values()]
		temp.update()
		temp.draw(screen)
		pg.display.flip()
		del temp

	pg.quit()