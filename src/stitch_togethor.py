from scipy.spatial.distance import directed_hausdorff
from scipy.spatial import procrustes
import numpy as np
import cv2
import csv
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import itertools





def hu_moments_similarity(line1, line2):
    # Convert to contour format
    contour1 = np.array(line1, dtype=np.float32).reshape((-1, 1, 2))
    contour2 = np.array(line2, dtype=np.float32).reshape((-1, 1, 2))

    # Compute Hu Moments
    hu1 = cv2.HuMoments(cv2.moments(contour1)).flatten()
    hu2 = cv2.HuMoments(cv2.moments(contour2)).flatten()

    # Compute Euclidean distance between moments
    return np.linalg.norm(hu1 - hu2)






w = 1

comb_items = [["-2.0", "-1.5"], ["-1.5", "-1.0"], ["-1.0", "-0.5"], ["-0.5", "0.0"], ["0.0", "0.5"], ["0.5", "1.0"], ["1.0", "1.5"], ["1.5", "2.0"]]

pairs = list(itertools.product(comb_items, repeat=2))

# print(pairs)

xv0_li = []
xv1_li = []
yv0_li = []
yv1_li = []
for pair in pairs:
    xv0_li.append(pair[0][0])
    xv1_li.append(pair[0][1])
    yv0_li.append(pair[1][0])
    yv1_li.append(pair[1][1])

# xv0_li = ["-2.0", "-1.5", "-2.0", "-1.5", "-1.0", "-1.0"]
# xv1_li = ["-1.5", "-1.0", "-1.5", "-1.0", "-0.5", "-0.5"]
# yv0_li = ["-2.0", "-1.5", "-1.5", "-2.0", "-2.0", "-1.5"]
# yv1_li = ["-1.5", "-1.0", "-1.0", "-1.5", "-1.5", "-1.0"]

fig = plt.figure(figsize=(15,15), layout="constrained")

big_grid_out = np.full((401,401), np.nan)

counter = 0
for xv0, xv1, yv0, yv1 in zip(xv0_li, xv1_li, yv0_li, yv1_li):
    try:
        grid = np.load("np/big_grid_"+xv0+"_"+xv1+"_"+yv0+"_"+yv1+".npy")
        grid_out = np.zeros((np.shape(grid)[0], np.shape(grid)[1]))

        for i in tqdm(range(w,np.shape(grid)[0]-w), desc=xv0+" "+xv1+" "+yv0+" "+yv1):
            for j in range(w,np.shape(grid)[1]-w):
                neighbours = grid[i-w:i+w+1,j-w:j+w+1].reshape(-1,2500,8)
                summer = []
                
                for k, neighbour in enumerate(neighbours):
                    if k != 4:
                        setter = [
                            hu_moments_similarity(grid[i,j,:,0:2], neighbour[:,0:2]),
                            hu_moments_similarity(grid[i,j,:,2:4], neighbour[:,2:4]),
                            hu_moments_similarity(grid[i,j,:,4:6], neighbour[:,4:6]),
                            hu_moments_similarity(grid[i,j,:,6:8], neighbour[:,6:8])
                        ]
                        setter = np.log10(np.array(setter))
                        setter[setter == -np.inf] = np.nan
                        summer.append(np.nanmean(setter))
                if len(summer) == 0:
                    grid_out[i,j] = np.nan
                else:
                    grid_out[i,j] = np.nanmean(summer)

        big_grid_out[int((float(xv0)+2)*100):1+int((float(xv1)+2)*100),int((float(yv0)+2)*100):1+int((float(yv1)+2)*100)] = grid_out
        counter += 1
        if counter == 4:
            img = plt.imshow(big_grid_out,
                extent=[-2,2,-2,2]
            )
            plt.savefig("test_neighbours.png",dpi=300)
            plt.clf()
            counter = 0
        del grid
    except:
        print(xv0, xv1, yv0, yv1, "does not yet exist")

img = plt.imshow(big_grid_out, extent=[-2,2,-2,2])
plt.xlim([-2,2])
plt.ylim([-2,2])
plt.colorbar(img)
plt.savefig("test_neighbours.png",dpi=300)
plt.clf()

np.save("big_grid_out.npy", big_grid_out)























grid = np.load("big_grid.npy")

grid_out = np.zeros((np.shape(grid)[0], np.shape(grid)[1]))

num_points = 2500
radius = 1
theta = np.linspace(0, 2 * np.pi, num_points)
circle = np.column_stack((radius * np.cos(theta), radius * np.sin(theta)))

fig = plt.figure(figsize=(15,15), layout="constrained")
for i in tqdm(range(np.shape(grid)[0]), desc="Test against circle"):
    for j in range(np.shape(grid)[1]):
        # print(np.shape(grid[i,j]), np.shape(circle))
        setter = [
            hu_moments_similarity(grid[i,j,:,0:2], circle[:,0:2]),
            hu_moments_similarity(grid[i,j,:,2:4], circle[:,2:4]),
            hu_moments_similarity(grid[i,j,:,4:6], circle[:,4:6]),
            hu_moments_similarity(grid[i,j,:,6:], circle[:,6:])
        ]
        grid_out[i,j] = np.nanmean(setter)

plt.imshow(np.log10(grid_out))
plt.colorbar()
plt.savefig("test_circle.png",dpi=300)
plt.clf()

grid_out = np.zeros((np.shape(grid)[0], np.shape(grid)[1]))


selected_orbit = grid[0,0]

plt.clf()
plt.plot(selected_orbit[:,0],selected_orbit[:,1])
plt.plot(selected_orbit[:,2],selected_orbit[:,3])
plt.plot(selected_orbit[:,4],selected_orbit[:,5])
plt.plot(selected_orbit[:,6],selected_orbit[:,7])
plt.gca().set_aspect("equal")
plt.savefig("tester.png")
plt.clf()

fig = plt.figure(figsize=(15,15), layout="constrained")
for i in tqdm(range(np.shape(grid)[0]), desc="Test against selected orbit"):
    for j in range(np.shape(grid)[1]):
        setter = [
            hu_moments_similarity(grid[i,j,:,0:2], selected_orbit[:,0:2]),
            hu_moments_similarity(grid[i,j,:,2:4], selected_orbit[:,2:4]),
            hu_moments_similarity(grid[i,j,:,4:6], selected_orbit[:,4:6]),
            hu_moments_similarity(grid[i,j,:,6:8], selected_orbit[:,6:8])
        ]
        grid_out[i,j] = np.nanmean(setter)


grid_out[grid_out <= 0] = np.nan

logged_grid = np.log10(grid_out)

plt.imshow(logged_grid)
plt.colorbar()
plt.savefig("test_selected_orbit.png",dpi=300)
plt.clf()


bins = np.linspace(0,np.nanmax(logged_grid),100)
plt.hist(logged_grid.flatten(), bins=bins, alpha=0.5)
plt.yscale("log")
plt.savefig("hist_test.png")
plt.clf()