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
	thickness_slider = Slider(100, 100, SLIDER_LENGTH, SLIDER_THICKNESS, WHITE)

	widgets = pg.sprite.Group()
	widgets.add(background)
	widgets.add(tool_bar)
	widgets.add(thickness_slider)
	widgets.add(thickness_slider.slider_block)

	draw_on = False
	points_list = []
	current_points_index = -1
	start_smooth_index = 0

	running = True
	while running:
		for event in pg.event.get():
			if event.type == QUIT:
				running = False

			# mouse
			if event.type == pg.MOUSEBUTTONDOWN:
				last_pos = event.pos
				points_list.append([])
				current_points_index += 1
				draw_on = True

			if event.type == pg.MOUSEBUTTONUP:
				draw_on = False

			if event.type == pg.MOUSEMOTION:
				if tool_bar.belongs(event.pos):
					if start_smooth_index >= N_POINTS_SMOOTH:
						points_list = smooth_step(background, points_list, 
							current_points_index, start_smooth_index,
							SIZE, mode=SMOOTH_MODE)
						start_smooth_index = 0
						
				if draw_on:
					# draw_step(background, WHITE, last_pos, event.pos, SIZE)

					for pts in points_list:
						[draw_step(background, WHITE, pts[i], pts[i+1], SIZE) for i in range(len(pts)-1)]

					
					last_pos = event.pos
					
					points_list[current_points_index].append(last_pos)

					#print("points_list:", points_list)
					
					start_smooth_index += 1
					if start_smooth_index >= N_POINTS_SMOOTH:
						points_list = smooth_step(background, points_list, 
							current_points_index, start_smooth_index, 
							SIZE, mode=SMOOTH_MODE)
						start_smooth_index = 0

			# keyboard
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