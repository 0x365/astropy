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
from scipy.signal import find_peaks, peak_prominences

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

num_num = 100


grid_fft = np.zeros((2*num_num,2*num_num,101))
grid_fft[grid_fft == 0] = np.nan


for j in tqdm(range(-num_num, num_num)):
    try:    
        data = np.load("data-np/set_"+str(j+0.5)+".npy", allow_pickle=True)
    except:
        continue


    for i in range(len(data)):
        if len(data[i]) > 2:
            counter += 1
        vals = 1/np.array(data[i],dtype=float)

        # # plt.plot()
        # if len(vals) == 50000:

        vals = vals - np.mean(vals)
        pad_vals = [*vals, *np.zeros(50000-len(vals))]
        # print(len(pad_vals))
        # pad_vals = np.pad(vals, (0, 50000), 'constant')
        FFT = np.fft.fft(vals)
        # indx = np.argmax(abs(FFT))
        x = np.fft.fftfreq(len(FFT), 0.0075/len(FFT))
        # print(len(x))
        # indxes = abs(x) < 50000
        # indxes = np.array(np.zeros_like(x),dtype=bool)
        # indxes = 
        # print(x)
        # # indxes = 
        # print(sum(indxes))
        grid_fft[i,j+num_num,:] = abs(FFT)[:101]



# Mirror Array
# grid_fft[:int(np.shape(grid_fft)[0]/2)] = np.flip(grid_fft[int(np.shape(grid_fft)[0]/2):],axis=0)
# grid_fft[:,:int(np.shape(grid_fft)[1]/2)] = np.flip(grid_fft[:,int(np.shape(grid_fft)[1]/2):],axis=1)


save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"data-np")
if not os.path.exists(save_location):
    os.makedirs(save_location)
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"data-np", "more-data")
if not os.path.exists(save_location):
    os.makedirs(save_location)


np.save(save_location+"/period_fft_big", grid_fft)

