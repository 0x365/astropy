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

data_location = "data_big/raw_orbits/"

grid_size = 200

loops = 50
per_loop = 1000
time = loops
timestep = loops*per_loop
total_steps = loops*per_loop

period = np.load("data_big/periods.npy")
collision_map = np.load("data_big/collisions.npy")

period2 = period[period != np.inf]
max_period = np.nanmax(period2)

grid = np.zeros((grid_size,grid_size,int(max_period*per_loop)))
grid[grid==0] = np.nan


counters = np.linspace(-1,1, grid_size)
for ii, i in enumerate(tqdm(counters)):
    for jj, j in enumerate(counters):
        
        if not np.isnan(period[ii,jj]):
            
            if period[ii,jj] == np.inf:
                grid[ii,jj,0] = np.inf
                continue

            orbit_data = np.load(data_location+str(ii)+"_"+str(jj)+".npz")

            t = orbit_data["t"]
            r1x, r1y, r2x, r2y, r3x, r3y, v1x, v1y, v2x, v2y, v3x, v3y = orbit_data["y"]
            success = orbit_data["success"]
            # print(period[ii,jj]*1000)

            r1x_s = r1x[0:int(period[ii,jj]*per_loop)]
            r1y_s = r1y[0:int(period[ii,jj]*per_loop)]
            r2x_s = r2x[0:int(period[ii,jj]*per_loop)]
            r2y_s = r2y[0:int(period[ii,jj]*per_loop)]
            r3x_s = r3x[0:int(period[ii,jj]*per_loop)]
            r3y_s = r3y[0:int(period[ii,jj]*per_loop)]

            r1x_dis = []
            r1y_dis = []
            r2x_dis = []
            r2y_dis = []
            r3x_dis = []
            r3y_dis = []

            for k in np.arange(0,len(t)-int(period[ii,jj]*per_loop),int(period[ii,jj]*per_loop)):
                # plt.plot(r1x[k:k+int(period[ii,jj]*per_loop)])
                r1x_dis.append(r1x[k:k+int(period[ii,jj]*per_loop)]-r1x_s)
                r1y_dis.append(r1y[k:k+int(period[ii,jj]*per_loop)]-r1y_s)
                r2x_dis.append(r2x[k:k+int(period[ii,jj]*per_loop)]-r2x_s)
                r2y_dis.append(r2y[k:k+int(period[ii,jj]*per_loop)]-r2y_s)
                r3x_dis.append(r3x[k:k+int(period[ii,jj]*per_loop)]-r3x_s)
                r3y_dis.append(r3y[k:k+int(period[ii,jj]*per_loop)]-r3y_s)

            r1_n = np.sum(norm([r1x_dis,r1y_dis], axis=0), axis=1)
            r2_n = np.sum(norm([r1x_dis,r1y_dis], axis=0), axis=1)
            r3_n = np.sum(norm([r1x_dis,r1y_dis], axis=0), axis=1)

            r_n = r1_n+r2_n+r3_n

            # print(np.shape(r1_n))

            # plt.plot(r_n)
            # plt.plot(r2_n)
            # plt.plot(r3_n)

            grid[ii,jj,:len(r_n)] = r_n

print("Saving large file, may take a moment")        
np.save("data_big/orbit_deviation", grid)

stability = np.nanstd(grid, axis=2)
stability[grid[:,:,0] == np.inf] = np.inf
np.save("data_big/orbit_deviation_std", stability)

del grid