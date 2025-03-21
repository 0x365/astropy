import numpy as np
import matplotlib.pyplot as plt
import os


TARGET = "line"






def get_minima(target):
    if target == "square":
        minima = np.load("datasets/square_2ms_3000steps/minima.npy")
        minima = minima - 200
        return minima
    elif target == "triangle":
        minima = np.load("datasets/triangle_2ms/minima.npy")
        minima = minima - 200
        minima = minima[minima[:,0] <= 0]
        return minima
    elif target == "line":
        minima = np.load("datasets/line_1ms/minima.npy")
        minima = minima - 200
        minima = minima[minima[:,0] <= 0]
        minima = minima[minima[:,1] <= 0]
        return minima
    
def get_orbit(target, i, j):
    if target == "square":
        return np.load("data-np-2ms-square/"+str(round(i))+"_"+str(round(j))+".npy")
    elif target == "triangle":
        return np.load("data-np-2ms-triangle/"+str(round(i))+"_"+str(round(j))+".npy")
    elif target == "line":
        return np.load("data-np-1ms-line/"+str(round(i))+"_"+str(round(j))+".npy")


minima = get_minima(TARGET)

print(np.shape(minima))

ids = []
for c, coord in enumerate(minima):
    j,i = coord
    print(i,j)
    orbit = get_orbit(TARGET, i, j)
    if np.mean(np.abs(orbit[-1])) <= 3:
        ids.append(c)
minima = minima[ids]

print(np.shape(minima))

squareness = int(np.ceil(np.sqrt(len(minima))))
print(np.sqrt(len(minima)))

fig, axs = plt.subplots(squareness,squareness, figsize=(40,40), layout="constrained")
axs = axs.flatten()
c = 0
for j,i in (minima):
    orbit = get_orbit(TARGET, i, j)
    axs[c].plot(orbit[:,0],orbit[:,1])
    axs[c].plot(orbit[:,2],orbit[:,3])
    axs[c].plot(orbit[:,4],orbit[:,5])
    if TARGET == "square":
        axs[c].plot(orbit[:,6],orbit[:,7])
    axs[c].set_aspect("equal")
    axs[c].axis("off")
    c += 1

plt.savefig("all_minima.png")