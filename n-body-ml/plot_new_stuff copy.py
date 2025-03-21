import csv
import numpy as np

# from scipy.fft import fft, fftfreq
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import pandas as pd
from scipy.stats import norm

from tqdm import tqdm
import itertools

from matplotlib.colors import LinearSegmentedColormap, ListedColormap

max_val = 2.0


def multi_sqrt(grid):
    for _ in range(2):
        grid = np.sqrt(grid)
    return grid

def rmse(grid):
    return np.sqrt(np.nanmean((grid)**2, axis=2))


grid_euc_distance = np.load("datasets/grid_euc_distance.npy")



for i in range(np.shape(grid_euc_distance)[2]):

    grid = grid_euc_distance.copy()
    grid = grid[:,:,i]

    grid[grid == 0] = np.nan
    ranks = pd.Series(grid.flatten()).rank(method="average")
    ranks_normalized = ranks / (len(grid.flatten()) + 1)
    grid = np.reshape(ranks_normalized, np.shape(grid))

    grid = (grid -np.nanmin(grid)) / (np.nanmax(grid)-np.nanmin(grid))

    plt.figure(figsize=(21,20), layout="constrained")
    plt.imshow(grid, extent=[-max_val,max_val,max_val,-max_val], cmap="cividis_r", interpolation=None)
    plt.xlabel("V1")
    plt.ylabel("V2")
    plt.colorbar()
    plt.gca().invert_yaxis()
    plt.savefig("tester/grid_"+str(i)+".png", dpi=100)
    plt.clf()

    plt.figure(figsize=(21,20), layout="constrained")
    plt.imshow(grid, extent=[-max_val,max_val,max_val,-max_val], cmap="tab20c", interpolation=None)
    plt.xlabel("V1")
    plt.ylabel("V2")
    plt.colorbar()
    plt.gca().invert_yaxis()
    plt.savefig("tester/grid_colourful_"+str(i)+".png", dpi=100)
    plt.clf()