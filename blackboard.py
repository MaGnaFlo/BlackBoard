import pygame as pg 
from parameters import PARAMS
from widgets import Widget
from functions import *


if __name__ == "__main__":

	pg.init()
	screen = pg.display.set_mode(
				(1000, 700))

	# add widgets
	widgets = init_widgets()

	

	# main loop
	loop(screen, widgets)

	pg.quit()