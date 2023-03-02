import numpy as np

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (100, 100, 100)

w, h = 1000, 700
TOOLBAR_THICKNESS = 100
SLIDER_THICKNESS = 6

SIZE = 2
N_POINTS_SMOOTH = 50
SMOOTH_MODE = "gaussian"
GAUSS_SIGMA = 5
SAVGOL_WIN = N_POINTS_SMOOTH // 4
SAVGOL_WIN = SAVGOL_WIN+1 if np.mod(SAVGOL_WIN, 2) == 0 else SAVGOL_WIN
SAVGOL_ORDER = 2