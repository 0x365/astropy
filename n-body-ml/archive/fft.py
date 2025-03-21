import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from fastdtw import fastdtw
import random
from sklearn.cluster import DBSCAN

total_num = 5
c = 0

fig, axs = plt.subplots(3,1, figsize=(5,10))

def normalise(x):
    return (x-np.amin(x))/(np.amax(x)-np.amin(x))

data = []
for i in tqdm(range(-total_num, total_num)):
    for j in range(-total_num, total_num):
        v1 = 1.5 * i / total_num
        v2 = 1.5 * j / total_num
        try:
            dataset = np.array(np.load("data-np/"+str(v1)+"_"+str(v2)+".npy"), dtype=float)
        except:
            continue
        if c < 1100:
            dataset_x = (np.sqrt(np.sum(np.square(dataset[:,1:2]),axis=1)))
            axs[0].plot(np.log10(dataset_x))

            fft_output = np.fft.fft(dataset_x-np.mean(dataset_x))
            magnitude_spectrum = np.abs(fft_output)

            # Since FFT is symmetric, we only plot the first half
            n = len(magnitude_spectrum) // 2
            frequencies = np.fft.fftfreq(len(dataset_x), 1/10000)[1:n]
            half_spectrum = magnitude_spectrum[1:n]
            axs[1].plot(frequencies, normalise(np.log10(half_spectrum)))

            windows = np.lib.stride_tricks.sliding_window_view(np.log10(half_spectrum), window_shape=100)
            axs[2].plot(normalise(np.std(windows,axis=1)))
            data.append(normalise(np.std(windows,axis=1)))
            c += 1
        else:
            break

plt.savefig("test.png")
plt.clf()


clustering = DBSCAN(eps=3, min_samples=2).fit(np.array(data))
print(clustering)