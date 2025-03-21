import numpy as np
import matplotlib.pyplot as plt

from matplotlib import cm, ticker

# grid = np.load("grid_100_manual_t.npy")
grid = np.load("grid.npy")



# Make data.
X = range(20)
Y = range(20)
X, Y = np.meshgrid(X, Y)
Z = grid

# Z[Z == 100] = np.nan
Z_collisions = Z
Z_collisions[Z < 100] == np.nan
Z[Z == 100] = np.nan
Z[Z == 50] = np.nan
Z[Z > 1] = 1
# Z[Z >= 1] = np.nan

# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
fig, axs = plt.subplots(1,1, figsize=(12,10))
# fig.tight_layout()


# Plot the surface.
# surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=True)
# fig.colorbar(surf, shrink=0.5, aspect=5)


# Z_log = 1/(Z)
Z_log = np.log10(Z)

Z_log = np.ma.array(Z_log, mask=np.isnan(Z_log))

colors = axs.contourf(np.linspace(-1,1,np.shape(Z)[0]), np.linspace(-1,1,np.shape(Z)[0]), Z_log, levels=30, cmap="inferno_r")

# colors = axs.imshow(Z_log)
# axs.invert_yaxis()
ticker_steps = 10
ticker = np.arange(0,np.nanmax(Z_log)+1, (np.nanmax(Z_log)+1)/ticker_steps)
cbar = plt.colorbar(colors, ticks=ticker)
# cbar.ax.set_yticklabels(np.array(np.around(1/ticker, decimals=3),dtype=str))

# CROSS
# plt.plot([0,0],[-1,1], c="orange")
# plt.plot([-1,1],[0,0], c="orange")

# CIRCLE
M = 1000
angle = np.exp(1j * 2 * np.pi / M)
angles = np.cumprod(np.ones(M + 1) * angle)
x, y = np.real(angles), np.imag(angles)
r = 0.9
plt.plot(r*x, r*y)

# plt.xticks(np.linspace(0,np.shape(grid)[0],5), np.array(np.linspace(0,1,5),dtype=str))
# plt.yticks(np.linspace(0,np.shape(grid)[0],5), np.array(np.linspace(0,1,5),dtype=str))

plt.axis('equal')
# limiter = np.arange(np.shape(Z)[0])[np.nansum(Z, axis=0) == 0][1]/np.shape(Z)[0]

plt.xlim([-1,1])
plt.ylim([-1,1])

plt.xlabel("V2")
plt.ylabel("V1")

plt.title("Standard deviation of the Hausdorff distance per repeating orbit (Classified by T = 6.325)")

plt.savefig("data/fig8_grid.png", dpi=500)

plt.clf()
