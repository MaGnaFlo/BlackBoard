import pygame as pg 
from parameters import PARAMS
from widgets import Widget
from functions import *


if __name__ == "__main__":

	pg.init()
	screen = pg.display.set_mode(
				(PARAMS["background"]["width"],
				 PARAMS["background"]["height"]))

	# add widgets
	widgets = init_widgets()

	# initialize parameters and lists
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
	colors = []

	# main loop
	loop(screen, widgets, points_list, current_points_index,
			draw_on, thickness_slider_move, current_size,
			start_smooth_index,
			smoothness_slider_move, current_smoothness,
			sizes, smoothnesses, colors)

	pg.quit()