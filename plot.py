import numpy as np
import matplotlib.pyplot as plt
import os

from common import *

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    raise Exception("Data does not exist")

data = np.load(save_location+"/contact_time.npy")
# data = np.load("contact_num.npy")
json_data = load_json(save_location+"/details.json")

axis = (0,2)

axis1 = list(json_data.keys())[axis[0]]
axis2 = list(json_data.keys())[axis[1]]

print(axis1, axis2)

print(np.shape(data))
all_axis = np.arange(6)
all_axis = all_axis[all_axis!=axis[0]]
all_axis = all_axis[all_axis!=axis[1]]

data = np.nanmean(data, axis=tuple(all_axis.tolist()))


extent = [np.nanmin(json_data[axis1]), np.nanmax(json_data[axis1]),np.nanmax(json_data[axis2]),np.nanmin(json_data[axis2])]


plt.figure(figsize=(10,10))
plt.imshow(np.swapaxes(data,0,1), extent=extent, aspect="auto")
plt.xlabel(axis1)
plt.ylabel(axis2)
plt.gca().invert_yaxis()
plt.savefig("test3.png")