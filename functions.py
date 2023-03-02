import pygame as pg
import pygame.gfxdraw
from parameters import *
from scipy.ndimage import gaussian_filter1d
import numpy as np

def draw_step(widget, color, start, end, size):
	# pg.draw.line(widget.image, color, start, end, size)
	# pg.draw.circle(widget.image, color, start, size)
	center_L1 = [(start[0]+end[0]) / 2., (start[1]+end[1]) / 2.]
	length = 5  # Total length of line
	thickness = size
	angle = np.arctan2(start[1] - end[1], start[0] - end[0])

	UL = (center_L1[0] + (length/2.) * np.cos(angle) - (thickness/2.) * np.sin(angle),
      center_L1[1] + (thickness/2.) * np.cos(angle) + (length/2.) * np.sin(angle))
	UR = (center_L1[0] - (length/2.) * np.cos(angle) - (thickness/2.) * np.sin(angle),
	      center_L1[1] + (thickness/2.) * np.cos(angle) - (length/2.) * np.sin(angle))
	BL = (center_L1[0] + (length/2.) * np.cos(angle) + (thickness/2.) * np.sin(angle),
	      center_L1[1] - (thickness/2.) * np.cos(angle) + (length/2.) * np.sin(angle))
	BR = (center_L1[0] - (length/2.) * np.cos(angle) + (thickness/2.) * np.sin(angle),
	      center_L1[1] - (thickness/2.) * np.cos(angle) - (length/2.) * np.sin(angle))
	pg.gfxdraw.aapolygon(widget.image, (UL, UR, BR, BL), color)
	pg.gfxdraw.filled_polygon(widget.image, (UL, UR, BR, BL), color)

def smooth_step(widget, points, points_index, smooth_index, size, mode="gaussian"):
	# wipe
	widget.image.fill(BLACK)

	# target last points
	points_to_smooth = points[points_index]
	if len(points_to_smooth) > smooth_index:
		points_to_smooth = points_to_smooth[-smooth_index:]

	# smooth
	if mode == "gaussian":
		func = lambda x: gaussian_filter1d(x, GAUSS_SIGMA)
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
	for pts in points[:points_index]:
		[draw_step(widget, WHITE, pts[i], pts[i+1], size) for i in range(len(pts)-1)]

	return points
