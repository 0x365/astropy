import numpy as np

import matplotlib.pyplot as plt

big_grid_out = np.load("big_grid_out_w1.npy")

fig = plt.figure(figsize=(16,15), layout="constrained")


big_grid_out = np.delete(big_grid_out, np.arange(50, big_grid_out.shape[0], 50), axis=0)
big_grid_out = np.delete(big_grid_out, np.arange(50, big_grid_out.shape[0], 50), axis=1)


# big_grid_out = np.delete(big_grid_out, [49,50,51,99,100,101], axis=0)
# big_grid_out = np.delete(big_grid_out, np.arange(49, big_grid_out.shape[0], 51), axis=0)
# big_grid_out = np.delete(big_grid_out, np.arange(49, big_grid_out.shape[0], 51), axis=0)



big_grid_out = big_grid_out - np.nanmin(big_grid_out)

# big_grid_out = np.square(big_grid_out)
# big_grid_out = np.square(big_grid_out)
# big_grid_out = np.log10(big_grid_out)


img = plt.imshow(big_grid_out, extent=[-2,2,-2,2])
plt.xlim([-2,2])
plt.ylim([-2,2])
plt.colorbar(img)
plt.savefig("4_body_orbit_neighbour_similarity.png",dpi=300)
plt.clf()
plt.close()








from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import gaussian_filter

# big_grid_out = np.sqrt(big_grid_out)
# big_grid_out = gaussian_filter(big_grid_out, sigma=4)
big_grid_out = np.log10(big_grid_out)
big_grid_out = gaussian_filter(big_grid_out, sigma=2)

# Define the spatial extent
x = np.linspace(-2, 2, big_grid_out.shape[1])  # X-coordinates
y = np.linspace(-2, 2, big_grid_out.shape[0])  # Y-coordinates
X, Y = np.meshgrid(x, y)

# Create a 3D plot
fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot surface
surf = ax.plot_surface(X, Y, big_grid_out, cmap='viridis', edgecolor='none')

# Labels and limits
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlabel("Value")  # Adjust based on your data meaning
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")

# Add color bar
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

# Save figure
plt.savefig("4_body_orbit_neighbour_similarity_3d.png", dpi=300)
# plt.show()
plt.clf()
plt.close()



fig = plt.figure(figsize=(16, 16))
ax = fig.add_subplot(111)
contour = ax.contourf(X, Y, big_grid_out, levels=25, cmap='viridis')
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
plt.savefig("4_body_orbit_neighbour_similarity_contour.png", dpi=300)
plt.clf()
plt.close()