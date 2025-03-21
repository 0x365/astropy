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
from tqdm import tqdm

def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)
    f.close()
    return output


for j in tqdm(range(-250,250)):
    try:
        data = csv_input("data/out_file_name"+str(j)+".csv")
        data = np.array(data, dtype=object)
        np.save("data-np/set_"+str(j), data)
        del data
    except:
        pass
    try:
        data = csv_input("data/out_file_name"+str(j+0.5)+".csv")
        data = np.array(data, dtype=object)
        np.save("data-np/set_"+str(j+0.5), data)
        del data
    except:
        pass