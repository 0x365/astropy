import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from commons import *
import ephem
from datetime import datetime
from get_sat_statistics import *
from itertools import product
import xarray as xr
import netCDF4

#################

START_TIME = 1709222233

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

# View grid pattern


grid_data = np.array(csv_input(save_location+"/grid_search.csv"), dtype=float)

# print(grid_data)

labels = ["Consensus Time", "Completeness","Inclination", "RAAN", "Eccentricity", "Argument of Periapsis", "Anomaly", "Mean Motion"]

# num_1 = np.unique(grid_data[:,on_x])
# num_2 = np.unique(grid_data[:,on_y])
# # print(num_1)
# # print(num_2)

# new_grid = np.zeros((len(num_2), len(num_1)))
# comp_new_grid = np.zeros((len(num_2), len(num_1)))
# new_grid[new_grid == 0] = np.nan
# comp_new_grid[comp_new_grid == 0] = np.nan
# for i, x in enumerate(num_1):
#     grid_2 = grid_data[grid_data[:,on_x] == x]
#     grid_2_comp = grid_data[grid_data[:,on_x] == x]
#     for j, y in enumerate(num_2):
#         try:
#             new_grid[j,i] = np.nanmin(grid_2[grid_2[:,on_y] == y][:,0])
#         except:
#             pass
#         comp_new_grid[j,i] = np.nanmean(grid_2_comp[grid_2_comp[:,on_y] == y][:,1])
#         # comp_new_grid[j,i] = np.nanmax(grid_2_comp[grid_2_comp[:,on_y] == y][:,1])


# new_grid[new_grid == 9999999999999.0] = np.nan

# print("Min value:", np.nanmin(new_grid), "| Mean Value:", np.nanmean(new_grid))

c_range = []
for i in range(2,8):
    if len(np.unique(grid_data[:,i])) >= 2:
        c_range.append(i)

# fig1, axs1 = plt.subplots(len(c_range),len(c_range), figsize=(30,30), dpi=300)
# fig2, axs2 = plt.subplots(len(c_range),len(c_range), figsize=(30,30), dpi=300)



fig3, axs3 = plt.subplots()
grid_inc = np.sort(np.unique(grid_data[:,2]))
grid_raan = np.unique(grid_data[:,3])
grid_ecc = np.unique(grid_data[:,4])
grid_argp = np.unique(grid_data[:,5])
grid_anom = np.unique(grid_data[:,6])
grid_moti = np.unique(grid_data[:,7])
grid_z0 = grid_data[:,0]
grid_z1 = grid_data[:,1]



dims = (len(grid_inc), len(grid_raan), len(grid_ecc), len(grid_argp), len(grid_anom), len(grid_moti))
grid_other = np.zeros(dims, dtype=float)



item_num = np.array(list(product(np.arange(len(grid_inc),dtype=int),np.arange(len(grid_raan),dtype=int),np.arange(len(grid_ecc),dtype=int),np.arange(len(grid_argp),dtype=int),np.arange(len(grid_anom),dtype=int),np.arange(len(grid_moti),dtype=int))))
permutations = np.array(list(product(grid_inc, grid_raan, grid_ecc, grid_argp, grid_anom, grid_moti)), dtype=tuple)

indx = np.lexsort(np.rot90(permutations), axis=0)
permutations = permutations[indx]
item_num = item_num[indx]

indx2 = np.lexsort(np.rot90(grid_data[:,2:]), axis=0)
grid_data = grid_data[indx2]
grid_vals = grid_data[:,2:]

c = 0
for i in range(len(grid_vals)):
    while not np.all(grid_vals[i] == permutations[c]) and c < len(permutations)-1:
        c += 1
    if c>len(grid_vals)-1:
        break
    grid_other[tuple(item_num[c])] = grid_data[i, 1]




print(np.shape(grid_other))
other = np.mean(grid_other, axis=(1,2,3,4))
print(np.shape(other))
other[other == 0] = np.nan

axs3.contour(grid_inc, grid_moti, other, np.linspace(0, np.amax(other), 100))
# fig3.savefig("temp.png")
plt.show()

"""
for c_i, x_c in enumerate(c_range):
    for c_j, y_c in enumerate(c_range):
        if c_i!=c_j:
            on_x = x_c
            on_y = y_c
            num_1 = np.unique(grid_data[:,on_x])
            num_2 = np.unique(grid_data[:,on_y])
            # new_grid = np.zeros((len(num_2), len(num_1)))
            comp_new_grid_mean = np.zeros((len(num_2), len(num_1)))
            # new_grid[new_grid == 0] = np.nan
            comp_new_grid_mean[comp_new_grid_mean == 0] = np.nan
            comp_new_grid_max = np.zeros((len(num_2), len(num_1)))
            # new_grid[new_grid == 0] = np.nan
            comp_new_grid_max[comp_new_grid_max == 0] = np.nan
            for i, x in enumerate(num_1):
                # grid_2 = grid_data[grid_data[:,on_x] == x]
                grid_2_comp = grid_data[grid_data[:,on_x] == x]
                for j, y in enumerate(num_2):
                    # try:
                    #     new_grid[j,i] = np.nanmin(grid_2[grid_2[:,on_y] == y][:,0])
                    # except:
                    #     pass
                    comp_new_grid_mean[j,i] = np.nanmean(grid_2_comp[grid_2_comp[:,on_y] == y][:,1])
                    # print("Test")
                    try:
                        comp_new_grid_max[j,i] = np.nanmax(grid_2_comp[grid_2_comp[:,on_y] == y][:,1])
                    except:
                        pass
            # new_grid = np.ma.array(new_grid, mask=np.isnan(new_grid))
            comp_new_grid_mean = np.ma.array(comp_new_grid_mean, mask=np.isnan(comp_new_grid_mean))
            comp_new_grid_max = np.ma.array(comp_new_grid_max, mask=np.isnan(comp_new_grid_max))

            # new_grid[new_grid == 9999999999999.0] = np.nan

            comp_new_grid_mean = np.power(comp_new_grid_mean,3)/math.pow(27,3)
            # comp_new_grid_mean = np.log10(comp_new_grid_mean)
            comp_new_grid_max = comp_new_grid_max/27
            # if np.shape(comp_new_grid_mean)[0] >= 2 and np.shape(comp_new_grid_mean)[1] >= 2:
            temp1 = axs1[c_i,c_j].contour(num_1, num_2, comp_new_grid_mean, np.linspace(0,1,400))
            temp2 = axs2[c_i,c_j].contour(num_1, num_2, comp_new_grid_max, np.linspace(0,1,100))
            # else:
            #     continue
            sat_data = get_sat_statistics(START_TIME)

            fig1.colorbar(temp1)
            axs1[c_i,c_j].scatter(sat_data[:,on_x-2], sat_data[:,on_y-2], c="red", alpha=0.2)
            axs1[c_i,c_j].set_xlabel(labels[on_x])
            axs1[c_i,c_j].set_ylabel(labels[on_y])
            axs1[c_i,c_j].set_xlim([np.amin(num_1), np.amax(num_1)])
            axs1[c_i,c_j].set_ylim([np.amin(num_2), np.amax(num_2)])

            fig2.colorbar(temp2)
            axs2[c_i,c_j].scatter(sat_data[:,on_x-2], sat_data[:,on_y-2], c="red", alpha=0.2)
            axs2[c_i,c_j].set_xlabel(labels[on_x])
            axs2[c_i,c_j].set_ylabel(labels[on_y])
            axs2[c_i,c_j].set_xlim([np.amin(num_1), np.amax(num_1)])
            axs2[c_i,c_j].set_ylim([np.amin(num_2), np.amax(num_2)])

fig1.suptitle("Completeness Mean Values")
fig1.savefig(results_location+"/grid_search_completeness_mean.png")
fig2.suptitle("Completeness Max Values")
fig2.savefig(results_location+"/grid_search_completeness_max.png")

# fig = plt.figure(figsize=(10,10), dpi=300)
# plt.contourf(num_1, num_2, new_grid, np.linspace(0,np.nanmax(new_grid)+1,100))
# plt.colorbar()
# plt.xlabel(labels[on_x])
# plt.ylabel(labels[on_y])
# plt.savefig(results_location+"/grid_search.png")

# plt.clf()



# fig = plt.figure(figsize=(10,10), dpi=300)


"""



