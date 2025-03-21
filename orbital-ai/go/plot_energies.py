import numpy as np
import matplotlib.pyplot as plt
import os

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"figures")
if not os.path.exists(save_location):
    os.makedirs(save_location)

def normalise(grid):
    return (grid-np.nanmin(grid))/(np.nanmax(grid)-np.nanmin(grid))


try:
    load_location = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"data-np", "more-data")
    grid_std = np.load(load_location+"/energy_std.npy")
    grid_mean = np.load(load_location+"/energy_mean.npy")
    # grid_stop = np.load(load_location+"/energy_stop.npy")

    fig = plt.figure(figsize=(10,10), constrained_layout=True)
    # fig.tight_layout()
    plt.imshow(np.log10((grid_std)), interpolation=None, extent=[-1.5,1.5,1.5,-1.5])#, cmap="turbo")
    fig.gca().invert_yaxis()
    plt.colorbar(label="Standard Distribution of Energy")
    plt.title("Standard Distribution of Energy")
    plt.xlabel("VX(t=0) Initial X Velocity")
    plt.ylabel("VY(t=0) Initial Y Velocity")
    plt.savefig(save_location+"/energies_std.png",dpi=1000)
    plt.clf()

    fig = plt.figure(figsize=(10,10), constrained_layout=True)
    plt.imshow(np.log10(normalise(grid_std)*normalise(grid_mean)), interpolation=None, extent=[-1.5,1.5,1.5,-1.5])#, cmap="turbo")
    fig.gca().invert_yaxis()
    plt.colorbar()
    plt.title("Thing")
    plt.savefig(save_location+"/energies_mean.png",dpi=1000)
    plt.clf()

    # grid_stop = np.log10(grid_stop)
    # for i in range(np.shape(grid_stop)[0]):
    #     fig = plt.figure(figsize=(10,10), constrained_layout=True)
    #     fig.tight_layout()
    #     plt.imshow(grid_stop[i], vmin=0.000001, vmax=np.nanmax(grid_stop[-1]), interpolation=None, extent=[-1,1,1,-1])#, cmap="turbo")
    #     fig.gca().invert_yaxis()
    #     plt.colorbar()
    #     plt.title("Orbit period")
    #     plt.savefig(save_location+"/stoppers/energies_stop_"+str(i)+".png",dpi=250)
    #     plt.clf()

except:
    print("Files dont exist")
    pass



