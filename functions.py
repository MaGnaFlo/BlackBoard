import pygame as pg
from parameters import *
from scipy.ndimage import gaussian_filter1d

def draw_step(surface, color, start, end, size):
	pg.draw.line(surface, color, start, end, 2*size)

def smooth_step(surface, points, points_index, smooth_index, size, mode="gaussian"):
	# wipe
	surface.fill(BLACK)

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
		[draw_step(surface, WHITE, pts[i], pts[i+1], size) for i in range(len(pts)-1)]

	return points
