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

minimum_period = 4

grid_size = 200

loops = 50
per_loop = 1000
time = loops
timestep = loops*per_loop
total_steps = loops*per_loop

period = np.zeros((grid_size,grid_size))
collisions_map = np.zeros((grid_size,grid_size))
# collisions_map[collisions_map == 0] = np.nan


counters = np.linspace(-1,1, grid_size)
for ii, i in enumerate(tqdm(counters)):
    for jj, j in enumerate(counters):

        if True:#ii == 53 and jj == 28:

            try:
                orbit_data = np.load(data_location+str(ii)+"_"+str(jj)+".npz")
            except:
                period[ii,jj] = np.nan
                continue

            t = orbit_data["t"]
            r1x, r1y, r2x, r2y, r3x, r3y, v1x, v1y, v2x, v2y, v3x, v3y = orbit_data["y"]
            success = orbit_data["success"]


            # ender = 100000
            # plt.plot(r1x[:ender],r1y[:ender])
            # plt.scatter(r2x[-1],r2y[-1])
            # plt.scatter(r3x[-1],r3y[-1])
            # plt.savefig("data_big/tester2.png")
            # plt.clf()


            if len(t) != total_steps:
                collisions_map[ii,jj] = 1
                period[ii,jj] = np.nan
            else:
                r1 = norm([r1x, r1y], axis=0)
                r2 = norm([r2x, r2y], axis=0)
                r3 = norm([r3x, r3y], axis=0)

                r1_rel = norm([r1x-r1x[0], r1y-r1y[0]], axis=0)
                r2_rel = norm([r2x-r2x[0], r2y-r2y[0]], axis=0)
                r3_rel = norm([r3x-r3x[0], r3y-r3y[0]], axis=0)

                inverted = (1/(r1_rel+r2_rel+r3_rel))[int(per_loop/10):]
                peaks = scipy.signal.find_peaks(inverted, height=inverted[0]/3)[0]

                # print(peaks)
                # plt.plot(inverted)
                # plt.scatter(peaks, [2]*len(peaks))
                # plt.savefig("data_big/tester.png")
                # plt.clf()
            

                if len(peaks) >= 1:
                    c = 0
                    while c < len(peaks) and peaks[c]/per_loop <= minimum_period:
                        c += 1
                    if c < len(peaks) and peaks[c] < total_steps/2:
                        period[ii,jj] = peaks[c]
                    else:
                        period[ii,jj] = np.inf   # np.nan
                else:
                    period[ii,jj] = np.inf   # np.nan


period = period/per_loop

np.save("data_big/periods", period)
np.save("data_big/collisions", collisions_map)

fig, axs = plt.subplots(1,1, figsize=(12,10))
plt.imshow(period, extent=[-1,1,1,-1])
axs.invert_yaxis()
plt.colorbar()
plt.savefig("data_big/period_map.png")
plt.clf()

fig, axs = plt.subplots(1,1, figsize=(12,10))
plt.imshow(collisions_map, extent=[-1,1,1,-1])
axs.invert_yaxis()
plt.savefig("data_big/collisions_map.png")
plt.clf()