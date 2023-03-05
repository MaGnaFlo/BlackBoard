import pygame as pg 
from parameters import PARAMS
from widgets import Widget
from functions import *


if __name__ == "__main__":

	pg.init()
	screen = pg.display.set_mode((PARAMS["screen"]["width"], PARAMS["screen"]["height"]), 
									pg.RESIZABLE)

	# add widgets
	widgets = init_widgets()

	# main loop
	loop(screen, widgets)

	pg.quit()