import pygame as pg
import pygame.gfxdraw
from parameters import *
from scipy.ndimage import gaussian_filter1d
import numpy as np

def draw_step(widget, color, start, end, size):
	pg.draw.line(widget.image, color, start, end, 2*size)
	pg.draw.circle(widget.image, color, start, size)

def smooth_step(widget, points, sizes, points_index, smooth_index, sigma, mode="gaussian"):
	# wipe
	widget.image.fill(BLACK)
	print(sigma)
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
		[draw_step(widget, WHITE, pts[j], pts[j+1], sizes[i]) for j in range(len(pts)-1)]

	return points
