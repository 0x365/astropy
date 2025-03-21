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


from scipy.signal import butter, lfilter
from scipy import signal
from scipy.signal import find_peaks, peak_prominences

def butter_bandpass(lowcut, highcut, fs, order=5):
    return butter(order, [lowcut, highcut], fs=fs, btype='band')

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


plt.figure(figsize=(10,10))
found = False
c = 0

counter = 0

num_num = 100

grid = np.zeros((2*num_num,2*num_num))
grid_prom = np.zeros((2*num_num,2*num_num))
grid_score = np.zeros((2*num_num,2*num_num))
grid[grid == 0] = np.nan
grid_prom[grid_prom == 0] = np.nan
grid_score[grid_score == 0] = np.nan


for j in tqdm(range(-num_num, num_num)):
    try:    
        data = np.load("data-np/set_"+str(j)+".npy", allow_pickle=True)
    except:
        continue


    for i in range(len(data)):
        if len(data[i]) > 2:
            counter += 1
        vals = np.array(data[i],dtype=float)[500:]
        # plt.plot()
        if len(vals) > 0:

            # t = np.linspace(0,len(vals)/1000, len(vals))
            
            peaks, _ = find_peaks(vals)
            peaks = peaks[peaks < 25000]
            # peaks = peaks[peaks > 1000]
            
            if len(peaks) > 1:
                spot = []
                for k in range(len(peaks)-1):
                    nearest_neigh = peaks/peaks[k]
                    spot.append(np.std(abs(nearest_neigh-np.round(nearest_neigh))))
                # print(spot)
                chosen_peak = peaks[np.argmin(spot)]
            
                grid_score[i,j+num_num] = np.amin(spot)
                grid_prom[i,j+num_num] = peak_prominences(vals,[chosen_peak])[0]
                grid[i,j+num_num] = chosen_peak

            # grid_new[i+num_num,j+num_num] = 
            # if c < 500:
            #     plt.plot(t, vals, label="input")
            #     c+=1



# Mirror Array
# grid[:int(np.shape(grid)[0]/2)] = np.flip(grid[int(np.shape(grid)[0]/2):],axis=0)
# grid[:,:int(np.shape(grid)[1]/2)] = np.flip(grid[:,int(np.shape(grid)[1]/2):],axis=1)
# grid_score[:int(np.shape(grid_score)[0]/2)] = np.flip(grid_score[int(np.shape(grid_score)[0]/2):],axis=0)
# grid_score[:,:int(np.shape(grid_score)[1]/2)] = np.flip(grid_score[:,int(np.shape(grid_score)[1]/2):],axis=1)
# grid_prom[:int(np.shape(grid_prom)[0]/2)] = np.flip(grid_prom[int(np.shape(grid_prom)[0]/2):],axis=0)
# grid_prom[:,:int(np.shape(grid_prom)[1]/2)] = np.flip(grid_prom[:,int(np.shape(grid_prom)[1]/2):],axis=1)


save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"data-np")
if not os.path.exists(save_location):
    os.makedirs(save_location)
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"data-np", "more-data")
if not os.path.exists(save_location):
    os.makedirs(save_location)

np.save(save_location+"/period_map", grid)
np.save(save_location+"/period_std_score", grid_score)
np.save(save_location+"/period_prominence_score", grid_prom)

print("Counter", counter)

