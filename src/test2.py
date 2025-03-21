from scipy.spatial.distance import directed_hausdorff
from scipy.spatial import procrustes
import numpy as np
import cv2
import csv
from tqdm import tqdm
import matplotlib.pyplot as plt

grid = np.load("big_grid.npy")




def hu_moments_similarity(line1, line2):
    # Convert to contour format
    contour1 = np.array(line1, dtype=np.float32).reshape((-1, 1, 2))
    contour2 = np.array(line2, dtype=np.float32).reshape((-1, 1, 2))

    # Compute Hu Moments
    hu1 = cv2.HuMoments(cv2.moments(contour1)).flatten()
    hu2 = cv2.HuMoments(cv2.moments(contour2)).flatten()

    # Compute Euclidean distance between moments
    return np.linalg.norm(hu1 - hu2)




grid_out = np.zeros((np.shape(grid)[0], np.shape(grid)[1]))

print(np.shape(grid))
print(np.shape(grid_out))

# w = 1

# fig = plt.figure(figsize=(15,15), layout="constrained")
# for i in tqdm(range(w,np.shape(grid)[0]-w), desc="Test against neighbours"):
#     for j in range(w,np.shape(grid)[1]-w):
#         neighbours = grid[i-w:i+w+1,j-w:j+w+1].reshape(-1,3000,8)
#         summer = 0
#         counter = 0
#         for neighbour in neighbours:
#             setter = [
#                 hu_moments_similarity(grid[i,j,:,0:2], neighbour[:,0:2]),
#                 hu_moments_similarity(grid[i,j,:,2:4], neighbour[:,2:4]),
#                 hu_moments_similarity(grid[i,j,:,4:6], neighbour[:,4:6]),
#                 hu_moments_similarity(grid[i,j,:,6:8], neighbour[:,6:8])
#             ]
#             summer += np.nanmean(setter)
#             counter += 1
#         if counter == 0:
#             grid_out[i,j] = np.nan
#         else:
#             grid_out[i,j] = summer / counter

# plt.imshow(np.log10(grid_out))
# plt.colorbar()
# plt.savefig("test_neighbours.png",dpi=300)
# plt.clf()



# grid_out = np.zeros((np.shape(grid)[0], np.shape(grid)[1]))

# num_points = 3000
# radius = 1
# theta = np.linspace(0, 2 * np.pi, num_points)
# circle = np.column_stack((radius * np.cos(theta), radius * np.sin(theta)))

# fig = plt.figure(figsize=(15,15), layout="constrained")
# for i in tqdm(range(np.shape(grid)[0]), desc="Test against circle"):
#     for j in range(np.shape(grid)[1]):
#         # print(np.shape(grid[i,j]), np.shape(circle))
#         setter = [
#             hu_moments_similarity(grid[i,j,:,0:2], circle[:,0:2]),
#             hu_moments_similarity(grid[i,j,:,2:4], circle[:,2:4]),
#             hu_moments_similarity(grid[i,j,:,4:6], circle[:,4:6]),
#             hu_moments_similarity(grid[i,j,:,6:], circle[:,6:])
#         ]
#         grid_out[i,j] = np.nanmean(setter)

# plt.imshow(np.log10(grid_out),cmap="tab20")
# plt.colorbar()
# plt.savefig("test_circle.png",dpi=300)
# plt.clf()





grid_out = np.zeros((np.shape(grid)[0], np.shape(grid)[1]))


selected_orbit = grid[175,175]

plt.clf()
plt.plot(selected_orbit[:,0],selected_orbit[:,1])
plt.plot(selected_orbit[:,2],selected_orbit[:,3])
plt.plot(selected_orbit[:,4],selected_orbit[:,5])
plt.plot(selected_orbit[:,6],selected_orbit[:,7])
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



plt.imshow(grid_out)
plt.colorbar()
plt.savefig("test_selected_orbit.png",dpi=300)
plt.clf()

grid_out = (grid_out-np.nanmin(grid_out)) + 0.00000001
grid_out = grid_out[~np.isnan(grid_out)]
plt.hist(grid_out.flatten(), bins=np.logspace(np.log10(np.nanmin(grid_out)),np.log10(np.nanmax(grid_out)), 50))
plt.savefig("hist_test.png")
