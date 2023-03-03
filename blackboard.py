import pygame as pg 
from pygame.locals import QUIT
from parameters import *
from widgets import ToolBar, Slider, Widget
from scipy.ndimage import gaussian_filter1d
from functions import *


if __name__ == "__main__":

	pg.init()
	screen = pg.display.set_mode((W,H))

	background = Widget(0, 0, W, H, BLACK)

	tool_bar = ToolBar(0, H-TOOLBAR_THICKNESS, W, TOOLBAR_THICKNESS, GREY)
	thickness_slider = Slider(50, 670, SLIDER_LENGTH, SLIDER_THICKNESS, BLACK)

	widgets = pg.sprite.Group()
	widgets.add(background)
	widgets.add(tool_bar)
	widgets.add(thickness_slider)
	widgets.add(thickness_slider.slider_block)

	draw_on = False
	slider_move_on = False
	points_list = []
	current_points_index = -1
	start_smooth_index = 0

	current_size = SIZE
	sizes = []
	n_points_smooth = N_POINTS_SMOOTH

	running = True
	while running:
		for event in pg.event.get():
			if event.type == QUIT:
				running = False

			# mouse
			if event.type == pg.MOUSEBUTTONDOWN:
				for w in widgets:
					if w.type == "slider":
						belong = w.belongs(event.pos)
						if belong == 2:
							slider_move_on = True
					elif w.type == "":
						print(sizes)
						last_pos = event.pos
						points_list.append([])
						sizes.append(current_size)
						current_points_index += 1
						draw_on = True
					# else:
					# 	belong = -1

					# if belong == 2:
					# 	slider_move_on = True
					# elif belong == 1:
					# 	pass
					# else:
					# 	last_pos = event.pos
					# 	points_list.append([])
					# 	sizes.append(current_size)
					# 	current_points_index += 1
					# 	draw_on = True

			if event.type == pg.MOUSEBUTTONUP:
				# sizes.append(current_size)
				draw_on = False
				slider_move_on = False

			if event.type == pg.MOUSEMOTION:
				if tool_bar.belongs(event.pos):
					if start_smooth_index >= n_points_smooth:
						points_list = smooth_step(background, points_list, sizes,
							current_points_index, start_smooth_index,
							sizes[current_points_index], mode=SMOOTH_MODE)
						start_smooth_index = 0

				if slider_move_on:
					w = widgets.sprites()[2] # careful with that! index may change!
					w.__class__ = Slider # ugly? but works (cast)
					w, size = w.update_block_pos(event.pos)
					# sizes.append(size)
					current_size = size
					print(size)
					widgets.add(w)
						
				elif draw_on:
					

					for i, pts in enumerate(points_list):
						[draw_step(background, WHITE, pts[j], pts[j+1], sizes[i]) for j in range(len(pts)-1)]
					
					last_pos = event.pos
					
					points_list[current_points_index].append(last_pos)

					#print("points_list:", points_list)
					
					start_smooth_index += 1
					if start_smooth_index >= n_points_smooth:
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

		
		widgets.update()
		widgets.draw(screen)

		# update screen
		# screen.blit(background, (0,0))
		pg.display.flip()


	pg.quit()