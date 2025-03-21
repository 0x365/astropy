import csv
import numpy as np

# from scipy.fft import fft, fftfreq
import math
import numpy as np

from tqdm import tqdm
import itertools

import os


def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = [row for row in read_obj]
    f.close()
    return output

total_num = 200
max_val = 2.0

combos = list(itertools.product([0, *range(-total_num, total_num+1)], repeat=2))
for ii in tqdm(combos):
    i = ii[0]
    j = ii[1]
    # if i <= 0 and j <= 0:
    if not os.path.exists("data-np/"+str(i)+"_"+str(j)+".npy"):
        try:
            v1 = max_val * i / total_num
            v2 = max_val * j / total_num
            if round(v1) == v1:
                v1 = round(v1)
            if round(v2) == v2:
                v2 = round(v2)
            # print(v1)
            if os.path.exists("data/"+str(v1)+"_"+str(v2)+".csv"):
                data = np.array(csv_input("data/"+str(v1)+"_"+str(v2)+".csv"),dtype=float)
                np.save("data-np/"+str(i)+"_"+str(j), data)
                # del data
        except:
            # print(v1,v2, i,j)
            pass

