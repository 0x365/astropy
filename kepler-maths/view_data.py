import matplotlib.pyplot as plt
import numpy as np
import os
import csv

#################

# Select orbits to display
orbit_nums = [1, 2, 3]

orbit_nums2 = np.arange(0, 81)

################

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)

results_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
if not os.path.exists(results_location):
    os.makedirs(results_location)

def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)
    f.close()
    return output

# fig = plt.figure(figsize=(10,10), dpi=300).add_subplot(projection='3d')
# for i in orbit_nums:
#     data = csv_input(save_location+"/pos_real/"+str(i)+".csv")
#     data = np.array(data,dtype=float)
#     plt.plot(data[:,0], -data[:,1], data[:,2])

fig = plt.figure(figsize=(10,10), dpi=300).add_subplot(projection='3d')
data = csv_input(save_location+"/pos_sim/temp.csv")
data = np.array(data,dtype=float)
plt.plot(data[:,0], -data[:,1], data[:,2])

plt.savefig(results_location+"/orbit_display.png")
plt.clf()

# Interactions with no zeros

fig = plt.figure(figsize=(10,10), dpi=300)
data_big = []
for i in orbit_nums2:
    data = csv_input(save_location+"/interactions/"+str(i)+".csv")
    data = np.array(data,dtype=int)
    for j in data:
        data_big.append(j)
data_big = np.array(data_big)
plt.imshow(data_big, interpolation='none', aspect='auto')

plt.savefig(results_location+"/interactions.png")
plt.clf()

# Interactions with no zeros

fig = plt.figure(figsize=(10,10), dpi=300)
data_big_no_zero = data_big[np.sum(data_big, axis=1) > 0]
plt.imshow(data_big_no_zero, interpolation='none', aspect='auto')
plt.savefig(results_location+"/interactions_no_zero.png")
plt.clf()

# Interactions with no zeros sorted

fig = plt.figure(figsize=(10,10), dpi=300)
indx = np.flip(np.argsort(np.sum(data_big_no_zero, axis=1)))
plt.imshow(data_big_no_zero[indx], interpolation='none', aspect='auto')
plt.savefig(results_location+"/interactions_no_zero_sorted.png")
plt.clf()
