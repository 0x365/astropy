import csv
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)
    f.close()
    return output

ranger = [0, 0.5, 1, 1.5, 2, 2.5]



for j in tqdm(ranger):
    try:
        data = csv_input("data/out_file_name"+str(j)+".csv")
        data = np.array(data, dtype=float)
        np.save("data-np/set_"+str(j), data)
    except:
        pass