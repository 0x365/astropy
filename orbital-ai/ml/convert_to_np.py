import csv
import numpy as np

# from scipy.fft import fft, fftfreq
import math
import numpy as np

from tqdm import tqdm

def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)
    f.close()
    return output

total_num = 5

for i in range(-total_num, total_num):
    for j in range(-total_num, total_num):
        v1 = 1.5 * i / total_num
        v2 = 1.5 * j / total_num
        try:
            data = csv_input("data/"+str(v1)+"_"+str(v2)+".csv")
            data = np.array(data)
            np.save("data-np/"+str(v1)+"_"+str(v2), data)
            del data
        except:
            pass
