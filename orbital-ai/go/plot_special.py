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

i = 10
for j in range(150):
    data = np.load("data-np/set_"+str(j)+".npy", allow_pickle=True)
    vals = np.array(data[i],dtype=float)[500:]
    # print(vals)
    plt.plot(vals)
plt.savefig("test.png")
plt.clf()