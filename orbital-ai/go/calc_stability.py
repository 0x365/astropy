import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm
from tqdm import tqdm

grid_size = 200


period = np.load("data-np/more-data/period_map.npy", allow_pickle=True)

period = period[:grid_size,:grid_size]

for j in tqdm(range(grid_size)):
    try:    
        orbit_data = np.load("data-np/set_"+str(j)+".npy", allow_pickle=True)
    except:
        continue
    
    min_period = np.nanmin(period[:,j])
    if np.isnan(min_period):
        continue
    grid = np.zeros((grid_size,int((50000/min_period)+1)))
    grid[grid == 0] = np.nan

    # print(np.shape(grid))

    for i in range(len(orbit_data)):

        # if period[i,j] == np.inf:
        #     grid[i,j,0] = np.inf
        #     continue
        if np.isnan(period[i,j]):
            continue

        data = np.array(orbit_data[i],dtype=float)

        r1x_s = data[0:int(period[i,j])]

        r1x_dis = []
        for k in np.arange(0,len(data)-int(period[i,j]),int(period[i,j])):
            r1x_dis.append(norm(data[k:k+int(period[i,j])]-r1x_s))
            r1x_s = data[k:k+int(period[i,j])]
        grid[i,:len(r1x_dis)] = r1x_dis

    np.save("data-np/stabilities/orbit_deviation_"+str(j), grid)
    del grid
