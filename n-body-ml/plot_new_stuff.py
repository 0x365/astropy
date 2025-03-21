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
grid_abs_distance = np.load("datasets/grid_abs_distance.npy")
grid_mse = np.load("datasets/grid_mse.npy")

grid = grid_euc_distance
# print(grid)



grid[grid == 0] = np.nan
ranks = pd.Series(grid.flatten()).rank(method="average")
ranks_normalized = ranks / (len(grid.flatten()) + 1)
grid = np.reshape(ranks_normalized, np.shape(grid))
# grid = norm.ppf(grid)

grid = (grid -np.nanmin(grid)) / (np.nanmax(grid)-np.nanmin(grid))


# grid_sign = grid.copy()
# grid_sign = grid_sign - 0.5
# grid = np.abs(grid-0.5)

# grid = np.log10(grid+0.01)
# grid[grid_sign < 0] = grid[grid_sign < 0]*-1


# grid = (grid -np.nanmin(grid)) / (np.nanmax(grid)-np.nanmin(grid))

# grid[grid > 0.8] = 0.8
# grid[grid > 0.5] = grid[grid>0.5]*-1
# grid = np.log10(grid+0.01)

plt.figure(figsize=(21,20), layout="constrained")
plt.imshow(grid, extent=[-max_val,max_val,max_val,-max_val], cmap="cividis_r", interpolation=None)
plt.xlabel("V1")
plt.ylabel("V2")
plt.colorbar()
plt.gca().invert_yaxis()
plt.savefig("grid.png", dpi=500)
plt.clf()

plt.figure(figsize=(21,20), layout="constrained")
plt.imshow(grid, extent=[-max_val,max_val,max_val,-max_val], cmap="tab20c", interpolation=None)
plt.xlabel("V1")
plt.ylabel("V2")
plt.colorbar()
plt.gca().invert_yaxis()
plt.savefig("grid_colourful.png", dpi=500)
plt.clf()





# fig = plt.figure(figsize=(11,10), layout="constrained")
# ax = fig.add_subplot(111, projection='3d')
# # x = np.arange(grid.shape[1])  # Columns
# # y = np.arange(grid.shape[0])  # Rows
# x, y = np.meshgrid(x, y)
# surf = ax.plot_surface(x, y, grid, cmap='cividis_r', edgecolor='k')

# # plt.xlabel("V1")
# # plt.ylabel("V2")
# fig.colorbar(surf)
# plt.gca().invert_yaxis()
# plt.show()
# plt.savefig("grid_3d.png", dpi=500)
# plt.clf()



# Histograms
# plt.figure(figsize=(15,10), layout="constrained")

# grid_rem_0 = (grid_rem_0 -np.nanmin(grid_rem_0)) / (np.nanmax(grid_rem_0)-np.nanmin(grid_rem_0))
# grid_rem_1 = (grid_rem_1 -np.nanmin(grid_rem_1)) / (np.nanmax(grid_rem_1)-np.nanmin(grid_rem_1))
# grid_rem_2 = (grid_rem_2 -np.nanmin(grid_rem_2)) / (np.nanmax(grid_rem_2)-np.nanmin(grid_rem_2))
# grid_rem_3 = (grid_rem_3 -np.nanmin(grid_rem_3)) / (np.nanmax(grid_rem_3)-np.nanmin(grid_rem_3))
# grid_rem_4 = (grid_rem_4 -np.nanmin(grid_rem_4)) / (np.nanmax(grid_rem_4)-np.nanmin(grid_rem_4))
# axs[0].hist(grid_rem_0.flatten(), bins=200, alpha=0.5, label="Incoming")
# axs[0].set_title("Incoming")
# axs[1].hist(grid_rem_1.flatten(), bins=200, alpha=0.5, label="Change 1")
# axs[1].set_title("Change 1")
# axs[2].hist(grid_rem_2.flatten(), bins=200, alpha=0.5, label="Change 2")
# axs[2].set_title("Change 2")
# axs[3].hist(grid_rem_3.flatten(), bins=200, alpha=0.5, label="Change 3")
# axs[3].set_title("Change 3")
# axs[4].hist(grid_rem_4.flatten(), bins=200, alpha=0.5, label="Change 4")
# axs[4].set_title("Change 4")

# plt.hist(grid.flatten(), bins=200, alpha=0.5, label="Final")

# plt.savefig("hist.png")