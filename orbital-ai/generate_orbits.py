import matplotlib.pyplot as plt
import numpy as np
import csv
from numpy.linalg import norm

from scipy.integrate import solve_ivp

from prop_simple import prop
from skimage import metrics
from shapely import LineString, hausdorff_distance, frechet_distance
from scipy.optimize import minimize
from scipy.optimize import curve_fit
import scipy

from pytictoc import TicToc
from tqdm import tqdm


def fit_func(v_in, file_name):
    v_1, v_2 = v_in

    m1,m2,m3 = 1,1,1

    r1x = -1
    r1y = 0
    r2x = 1
    r2y = 0
    r3x = 0
    r3y = 0
    v1x = v_1
    v1y = v_2
    v2x = v_1
    v2y = v_2
    v3x = -2*v_1/m3
    v3y = -2*v_2/m3
    initial = [m1,m2,m3,r1x,r1y,r2x,r2y,r3x,r3y,v1x,v1y,v2x,v2y,v3x,v3y]

    loops = 50
    per_loop = 1000
    time = loops
    timestep = loops*per_loop
    total_steps = loops*per_loop
    file_name = "data_big/raw_orbits/"+file_name

    prop(initial, file_name, time=time, timestep=timestep)
    


grid_size = 200


counters = np.linspace(-1,1, grid_size)

print(counters)
for ii, i in enumerate(tqdm(counters)):
    # if ii == grid_size-1 or np.sum(grid_bool[ii+1]) == 0:
    for jj, j in enumerate(counters):
            # if np.sqrt(i**2 + j**2) <= 0.9:
        # if ii == 48 and jj == 28:
        fit_func([float(i), float(j)], str(ii)+"_"+str(jj))
        # np.save("grid", grid)
# np.save("grid", grid)