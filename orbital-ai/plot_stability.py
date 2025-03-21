import matplotlib.pyplot as plt
from matplotlib import cm
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

plot_1_orbit = False

loops = 50
per_loop = 1000
total_steps = loops*per_loop

try:
    grid = np.load("data_big/orbit_deviation_adjusted.npy")
except:
    print("Loading large file, may take a moment")
    deviation = np.load("data_big/orbit_deviation.npy")

    grid = np.nanstd(deviation, axis=2)
    grid[deviation[:,:,0] == np.inf] = np.nan
    # grid[grid == 0] = np.nan
    # print(np.sum([grid==np.inf]))
    # grid = np.log10(grid)
    del deviation
    grid = 1-np.sqrt(1/grid)

    np.save("data_big/orbit_deviation_adjusted", grid)


period = np.load("data_big/periods.npy")
collision_map = np.load("data_big/collisions.npy")


def onclick(event):
    
    if event.xdata != None and event.ydata != None:
        counters = np.linspace(-1,1, grid_size)
        ii = np.argsort(np.square(counters - event.ydata))[0]
        jj = np.argsort(np.square(counters - event.xdata))[0]

        try:
            print("Plot", ii, jj)
            orbit_data = np.load(data_location+str(ii)+"_"+str(jj)+".npz")

            t = orbit_data["t"]
            r1x, r1y, r2x, r2y, r3x, r3y, v1x, v1y, v2x, v2y, v3x, v3y = orbit_data["y"]
            success = orbit_data["success"]

            fig2, axs2 = plt.subplots(1,1, figsize=(16,10))

            if np.isnan(period[ii,jj]) or np.isinf(period[ii,jj]) or not plot_1_orbit:
                ender = -1
            else:
                ender = int(period[ii,jj]*per_loop)
            axs2.plot(r1x[:ender],r1y[:ender])
            axs2.plot(r2x[:ender],r2y[:ender])
            axs2.plot(r3x[:ender],r3y[:ender])

            axs2.set_xlabel("X")
            axs2.set_ylabel("Y")

            if len(t) != total_steps:
                collisional = "True"
            else:
                collisional = "False"
            
            textstr = ""
            textstr += "V1=%.9f\n"%(counters[ii])
            textstr += "V2=%.9f\n"%(counters[jj])
            textstr += "\n"
            textstr += "Predicted Period=%.3f\n"%(period[ii,jj])
            textstr += "STD in Euclidean Distance=%.0f\n"%(1/((1-grid[ii,jj])**2))
            textstr += "\n"
            textstr += "Collisional Orbit="+collisional+"\n"
            textstr += "Total ODE Steps=%.0f\n"%(len(t))
            
            plt.text(-0.5, 0.5, textstr, transform=axs2.transAxes,va='center', ha="center", fontsize=20)
            plt.subplots_adjust(left=0.44)
            
            plt.title("Propagated Orbit for 1 of the predicted period")
            

            plt.axis('equal')
            
            fig2.savefig("data_big/chosen_orbit.png") #redraw
            plt.clf()
            plt.close()
        except:
            print("File does not exist for", ii, jj)
    


def main_map():

    fig, axs = plt.subplots(1,1, figsize=(12,10))
    # colors = axs.contourf(np.linspace(-1,1,np.shape(grid)[0]), np.linspace(-1,1,np.shape(grid)[0]), grid, levels=40, cmap="BuPu_r")
    colors = plt.imshow(grid, extent=[-1,1,1,-1], cmap="BuPu_r")
    axs.invert_yaxis()

    # ticker = np.arange(0,0.07)
    ticker = np.arange(0, np.nanmax(grid), 0.01)
    cbar = plt.colorbar(colors, ticks=[*ticker, np.nanmax(grid)])
    cbar.ax.set_yticklabels([*np.array(np.around((1/(np.square(1-ticker))),decimals=-2), dtype=str), "inf"])

    plt.axis('equal')

    # plt.xlim([-1,1])
    # plt.ylim([-1,1])

    plt.xlabel("V2")
    plt.ylabel("V1")

    plt.savefig("data_big/stability.png",dpi=1000)
    fig.canvas.mpl_connect('button_press_event',onclick)
    plt.show()
    plt.clf()
    plt.close()


main_map()


# fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(10,10))
# fig.tight_layout()

# X,Y= np.meshgrid(np.linspace(-1,1,np.shape(grid)[0]), np.linspace(-1,1,np.shape(grid)[0]))
# Z = grid
# c = np.sum(~np.isnan(deviation),axis=2)

# surf = ax.contourf3D(X, Y, Z, levels=20, cmap=cm.inferno, facecolors=cm.jet(c/np.nanmax(c)), linewidth=0, antialiased=True)
# fig.colorbar(surf, shrink=0.5, aspect=5)
# plt.xlabel("V2")
# plt.ylabel("V1")
# # plt.show()
# plt.savefig("data_big/stability2.png")

