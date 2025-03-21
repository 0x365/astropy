import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy as sy
import scipy.fftpack as syfp
# from scipy.fft import fft, fftfreq
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
from scipy.signal import butter, lfilter
import os
from tqdm import tqdm

def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)
    f.close()
    return output



plt.figure(figsize=(10,10))
found = False
c = 0

counter = 0
stopper_points = 50

num_num = 100

grid_std = np.zeros((2*num_num,2*num_num))
grid_mean = np.zeros((2*num_num,2*num_num))
# grid_stop = np.zeros((stopper_points,2*num_num,2*num_num))
grid_std[grid_std == 0] = np.nan
grid_mean[grid_mean == 0] = np.nan
# grid_stop[grid_stop == 0] = np.nan


stopper_loc = np.linspace(1,50000-1,stopper_points)

for j in tqdm(range(-num_num, num_num)):
    try:    
        data = np.load("data-np/set_"+str(j+0.5)+".npy", allow_pickle=True)
    except:
        continue
    
    for i in range(len(data)):
        if len(data[i]) > 1000:
            counter += 1
            vals = np.array(data[i], dtype=float)
            grid_std[i,j+num_num] = np.nanstd(vals)
            grid_mean[i,j+num_num] = np.nanmean(vals)
            # for k, stopper in enumerate(stopper_loc):
            #     try:
            #         if vals[int(stopper)] == vals[0]:
            #             grid_stop[k,i,j+num_num] = 0.000001
            #         else:
            #             grid_stop[k,i,j+num_num] = vals[int(stopper)]-vals[0]
            #     except:
            #         pass



# Mirror Array
# grid_std[:int(np.shape(grid_std)[0]/2)] = np.flip(grid_std[int(np.shape(grid_std)[0]/2):],axis=0)
# grid_std[:,:int(np.shape(grid_std)[1]/2)] = np.flip(grid_std[:,int(np.shape(grid_std)[1]/2):],axis=1)
# grid_mean[:int(np.shape(grid_mean)[0]/2)] = np.flip(grid_mean[int(np.shape(grid_mean)[0]/2):],axis=0)
# grid_mean[:,:int(np.shape(grid_mean)[1]/2)] = np.flip(grid_mean[:,int(np.shape(grid_mean)[1]/2):],axis=1)
# grid_stop[:,:int(np.shape(grid_stop)[1]/2)] = np.flip(grid_stop[:,int(np.shape(grid_stop)[1]/2):],axis=1)
# grid_stop[:,:,:int(np.shape(grid_stop)[2]/2)] = np.flip(grid_stop[:,:,int(np.shape(grid_stop)[2]/2):],axis=2)

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"data-np")
if not os.path.exists(save_location):
    os.makedirs(save_location)
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"data-np", "more-data")
if not os.path.exists(save_location):
    os.makedirs(save_location)

np.save(save_location+"/energy_std", grid_std)
np.save(save_location+"/energy_mean", grid_mean)
# np.save(save_location+"/energy_stop", grid_stop)

print("Counter", counter)

