import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"figures")
if not os.path.exists(save_location):
    os.makedirs(save_location)



load_location = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"data-np", "more-data")
grid_fft = np.load(load_location+"/period_fft_big.npy")

fig = plt.figure(figsize=(10,10))


print(np.shape(grid_fft))

grid_fft = grid_fft[:,:,1:]

for i in range(len(grid_fft[0])):
    for j in range(len(grid_fft[1])):
        grid_fft[i,j] = (grid_fft[i,j]-np.nanmin(grid_fft[i,j]))/(np.nanmax(grid_fft[i,j])-np.nanmin(grid_fft[i,j]))
        # print(np.amax(grid_fft[i,j]))

grid_fft2 = grid_fft[:np.shape(grid_fft)[0]//2,:np.shape(grid_fft)[1]//2,]

# grid = np.zeros_like(grid_fft[:,:,0])
grid = np.zeros((np.shape(grid_fft2)[0]*2, np.shape(grid_fft2)[0]*2))
grid_close = np.zeros((np.shape(grid_fft)[0], np.shape(grid_fft)[0]))
mean_trend = np.nanmean(grid_fft2,axis=(0,1))
median_trend = np.nanmedian(grid_fft2,axis=(0,1))
grid_fft2[np.isnan(grid_fft2)] = 0
grid_fft[np.isnan(grid_fft)] = 0


# # Compare whole grid against itself
# flatter_grid = grid_fft2.reshape(np.shape(grid_fft2)[0]*np.shape(grid_fft2)[0], np.shape(grid_fft2)[2])
# meaned_grid = flatter_grid-np.swapaxes([np.nanmean(flatter_grid,axis=1)]*np.shape(grid_fft2)[2],0,1)
# dot_prod = np.zeros((np.shape(meaned_grid)[0],np.shape(meaned_grid)[0]))
# for i in tqdm(range(np.shape(meaned_grid)[1])):
#     dot_prod += np.dot(np.swapaxes([meaned_grid[:,i]],0,1), [meaned_grid[:,i]])
# sq_grid = np.nansum(meaned_grid**2, axis=1)
# # print(sq_grid)
# under_grid = np.sqrt(np.dot(np.swapaxes([sq_grid],0,1),[sq_grid]))
# under_grid[under_grid == 0] = np.nan
# # print(dot_prod)
# grid[:np.shape(grid_fft2)[0],:np.shape(grid_fft2)[0]] = np.nanmean(abs(dot_prod/under_grid), axis=1).reshape(np.shape(grid_fft2)[0],np.shape(grid_fft2)[1])

# # Mirror Array
# grid[int(np.shape(grid)[0]/2):] = np.flip(grid[:int(np.shape(grid)[0]/2)],axis=0)
# grid[:,int(np.shape(grid)[1]/2):] = np.flip(grid[:,:int(np.shape(grid)[1]/2)],axis=1)

# grid[grid == 0] = np.nan
# np.save(load_location+"/fft_processed", grid)
# print(grid)
# plt.imshow((grid), interpolation=None, extent=[-1,1,1,-1], cmap="turbo_r")
# fig.gca().invert_yaxis()
# plt.colorbar()
# plt.title("Orbit period")
# plt.savefig(save_location+"/fft_map_whole.png",dpi=1000)
# plt.clf()


# Compare in local area
squarer = 3
unsquarer = np.shape(grid_fft)[0]-squarer+1
windows = np.lib.stride_tricks.sliding_window_view(grid_fft, [squarer,squarer,np.shape(grid_fft)[2]])[:,:,0]
windows = windows.reshape((unsquarer,unsquarer,squarer**2,np.shape(grid_fft)[2]))
print(np.shape(windows))
for i in tqdm(range(squarer//2, np.shape(grid_fft)[0]-squarer//2)):

    for j in range(squarer//2, np.shape(grid_fft)[1]-squarer//2):
        y = grid_fft[i,j]
        this_window = windows[i-squarer//2,j-squarer//2]

        # Standard Distribution of surroundings


        # Euclidean Distace
        # coeff = np.mean(np.sqrt(x**2 + y**2))

        # Pearson Coeff
        coeff = 0
        for k in range(len(this_window)):
            x = this_window[k]
            coeff += abs((np.sum((x-np.mean(x))*(y-np.mean(y))))/(np.sqrt(np.sum((x-np.mean(x))**2)*np.sum((y-np.mean(y))**2))))
        coeff = coeff / np.shape(this_window)[0]
        # Pearson coeff from median
        # x = median_trend
        # coeff = ((np.sum((x-np.mean(x))*(y-np.mean(y))))/(np.sqrt(np.sum((x-np.mean(x))**2)*np.sum((y-np.mean(y))**2))))
        # coeff = np.sum(np.dot([y], flatter_grid.T))

        # Correlation to surroundings        
        # coeff = 0
        # for k in range(len(this_window)):
        #     coeff += np.correlate(y, this_window[k])
        # coeff = coeff / np.shape(this_window)[0]

        grid_close[i,j] = coeff


def normalise(grid):
    return (grid-np.nanmin(grid))/(np.nanmax(grid)-np.nanmin(grid))

# # Mirror Array
# grid_close[int(np.shape(grid_close)[0]/2):] = np.flip(grid_close[:int(np.shape(grid_close)[0]/2)],axis=0)
# grid_close[:,int(np.shape(grid_close)[1]/2):] = np.flip(grid_close[:,:int(np.shape(grid_close)[1]/2)],axis=1)
print(np.shape(grid_close))
fig = plt.figure(figsize=(10,10), constrained_layout=True)
plt.imshow(normalise((grid_close)), interpolation=None, extent=[-1.5,1.5,1.5,-1.5])#, cmap="turbo_r")
fig.gca().invert_yaxis()
plt.colorbar(label="Average Pearson Correlation Coefficient of Surrounding FFT")
plt.xlabel("VX(t=0) Initial X Velocity")
plt.ylabel("VY(t=0) Initial Y Velocity")
plt.title("FFT comparison of Neighbours")
plt.savefig(save_location+"/fft_map_close.png",dpi=1000)
plt.clf()

np.save(load_location+"/fft_map_close", grid_close)


for i in range(np.shape(grid_fft)[1]):
    plt.plot(grid_fft[int(0.75*np.shape(grid_fft)[2]),i,:]-median_trend,alpha=0.1, c="black")
# plt.plot(np.median(grid_fft,axis=(0,1)), c="red")
# plt.xscale("log")
plt.savefig("test.png")
plt.clf()


plt.hist(abs(grid.flatten()), bins=np.linspace(0,1,100))
plt.yscale("log")
plt.savefig("test2.png")
plt.clf()






