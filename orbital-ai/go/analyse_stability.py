import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm
from tqdm import tqdm

grid_size = 200

grid_big = np.zeros((2*grid_size,2*grid_size))
grid_big[grid_big == 0] = np.nan
for j in tqdm(range(grid_size)):
    try:    
        grid = np.load("data-np/stabilities/orbit_deviation_"+str(j)+".npy")
        grid_big[:np.shape(grid)[0],j] = np.nanstd(grid,axis=1)
    except:
        continue
    

grid_big[int(np.shape(grid_big)[0]/2):] = np.flip(grid_big[:int(np.shape(grid_big)[0]/2)],axis=0)
grid_big[:,int(np.shape(grid_big)[1]/2):] = np.flip(grid_big[:,:int(np.shape(grid_big)[1]/2)],axis=1)


np.save("data-np/more-data/orbit_deviation_std", grid_big)

fig = plt.figure(figsize=(10,10))
plt.imshow(np.log10(grid_big), extent=[-1,1,1,-1])
fig.gca().invert_yaxis()
plt.colorbar()
plt.savefig("test.png",dpi=500)