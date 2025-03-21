import csv
import numpy as np

# from scipy.fft import fft, fftfreq
import math
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
import itertools

import os

total_num = 200

grid_abs_distance = np.zeros((total_num*2,total_num*2))
grid_euc_distance = np.zeros((total_num*2,total_num*2, len(range(50,3000,50))))
grid_mse = np.zeros((total_num*2,total_num*2))

def get_data(i,j):
    return np.swapaxes(np.load("data-np/"+str(i)+"_"+str(j)+".npy"), 0,1)


def get_abs_distance(mid, left, right, up, down):
    diff_left = np.linalg.norm(mid - left,axis=0)
    diff_right = np.linalg.norm(mid - right,axis=0)
    diff_up = np.linalg.norm(mid - up,axis=0)
    diff_down = np.linalg.norm(mid - down,axis=0)
    diff_all = np.sum([diff_left, diff_right, diff_up, diff_down], axis=1)
    diff_mean = np.mean(diff_all)
    return diff_mean


def get_euc_distance(mid, left, right, up, down):
    diff_left = np.sqrt(np.sum(np.square(mid - left)))
    diff_right = np.sqrt(np.sum(np.square(mid - right)))
    diff_up = np.sqrt(np.sum(np.square(mid - up)))
    diff_down = np.sqrt(np.sum(np.square(mid - down)))
    diff_mean = np.mean([diff_left, diff_right, diff_up, diff_down])
    return diff_mean

def get_mse(mid, left, right, up, down):
    diff_left = np.sum(np.square(mid - left))
    diff_right = np.sum(np.square(mid - right))
    diff_up = np.sum(np.square(mid - up))
    diff_down = np.sum(np.square(mid - down))
    diff_mean = np.mean([diff_left, diff_right, diff_up, diff_down])
    return diff_mean




combos = list(itertools.product([0, *range(-total_num, total_num+1)], repeat=2))
c = 0
for ii in tqdm(combos):
    i = ii[0]
    j = ii[1]
    # if j <= 0 and i <= 0:
    if not os.path.exists("data-np/"+str(i)+"_"+str(j)+".npy"):
        continue
    try:
        mid = get_data(i,j)
        left = get_data(i,j+1)
        right = get_data(i,j-1)
        up = get_data(i+1,j)
        down = get_data(i-1,j)

        for jj, xx in enumerate(range(50,3000,50)):
            
            grid_euc_distance[i+total_num,j+total_num,jj] = get_euc_distance(mid[:,:xx], left[:,:xx], right[:,:xx], up[:,:xx], down[:,:xx])
        grid_abs_distance[i+total_num,j+total_num] = get_abs_distance(mid, left, right, up, down)
        grid_mse[i+total_num,j+total_num] = get_mse(mid, left, right, up, down)
        c += 1
    except:
        pass
    if c % int(len(combos)/10) == 0 and c != 0:
        plt.figure(figsize=(11,10), layout="constrained")
        grid_plot = np.log10(grid_euc_distance[:,:,-1])
        grid_plot = np.log10(grid_plot+2)
        plt.imshow(grid_plot, cmap="cividis_r")
        plt.colorbar()
        plt.gca().invert_yaxis()
        plt.savefig("grid.png")
        plt.clf()

print(c, "completed")

# grid_euc_distance[:,total_num:] = np.flip(grid_euc_distance[:,:total_num], axis=1)
# grid_euc_distance[total_num:,:] = np.flip(grid_euc_distance[:total_num,:], axis=0)


# grid_euc_distance[:,total_num:] = np.rot90(grid_euc_distance[:,:total_num], k=2)
# grid_abs_distance[:,total_num:] = np.rot90(grid_abs_distance[:,:total_num], k=2)
# grid_mse[:,total_num:] = np.rot90(grid_mse[:,:total_num], k=2)

np.save("datasets/grid_euc_distance", grid_euc_distance)
np.save("datasets/grid_abs_distance", grid_abs_distance)
np.save("datasets/grid_mse", grid_mse)

print(grid_euc_distance)

grid_euc_distance[grid_euc_distance == 0] = np.nan

plt.figure(figsize=(11,10), layout="constrained")
grid_plot = np.log10(grid_euc_distance[:,:,-1])
grid_plot = np.log10(grid_plot+2)
plt.imshow(grid_plot, cmap="cividis_r")
plt.colorbar()
plt.gca().invert_yaxis()
plt.savefig("grid.png")