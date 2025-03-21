import numpy as np
import matplotlib.pyplot as plt
import os

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"figures")
if not os.path.exists(save_location):
    os.makedirs(save_location)


try:
    load_location = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"data-np", "more-data")
    grid = np.load(load_location+"/period_map.npy")
    grid_score = np.load(load_location+"/period_std_score.npy")
    grid_prom = np.load(load_location+"/period_prominence_score.npy")
    grid_fft = np.load(load_location+"/period_fft.npy")

    fig = plt.figure(figsize=(10,10), constrained_layout=True)
    plt.imshow((grid/1000), interpolation=None, extent=[-1,1,1,-1], cmap="turbo")
    fig.gca().invert_yaxis()
    plt.colorbar()
    plt.title("Orbit period")
    plt.savefig(save_location+"/period_map.png",dpi=1000)
    plt.clf()

    fig = plt.figure(figsize=(12,10), constrained_layout=True)
    X,Y = np.meshgrid(np.linspace(-1,1,np.shape(grid)[0]),np.linspace(-1,1,np.shape(grid)[1]))
    plt.contourf(X,Y,(grid/1000), levels=200, extent=[-1,1,1,-1], cmap="turbo")
    plt.colorbar()
    plt.title("Orbit period")
    plt.savefig(save_location+"/period_map_countour.png",dpi=1000)
    plt.clf()

    fig = plt.figure(figsize=(10,10), constrained_layout=True)
    plt.imshow((grid_fft/1000), interpolation=None, extent=[-1,1,1,-1], cmap="turbo")
    fig.gca().invert_yaxis()
    plt.colorbar()
    plt.title("Orbit period from fft")
    plt.savefig(save_location+"/period_fft.png",dpi=1000)
    plt.clf()

    fig = plt.figure(figsize=(10,10), constrained_layout=True)
    plt.imshow(np.log10(grid_prom))
    plt.colorbar()
    plt.title("Prominence score")
    plt.savefig(save_location+"/period_prominence_score.png",dpi=500)
    plt.clf()

    fig = plt.figure(figsize=(10,10), constrained_layout=True)
    plt.imshow(np.log10(grid_score))
    plt.colorbar()
    plt.title("Standard distribution score")
    plt.savefig(save_location+"/period_std_score.png",dpi=500)
    plt.clf()
except:
    print("Files dont exist")
    pass



