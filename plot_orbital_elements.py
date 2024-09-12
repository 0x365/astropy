import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
import itertools

from common import *

data_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(data_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
if not os.path.exists(save_location):
    os.mkdir(save_location)
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures", "orbital-elements")
if not os.path.exists(save_location):
    os.mkdir(save_location)

combinati = itertools.combinations(["argp","ecc","inc","raan","anom","mot"],2)

for comb in tqdm(list(combinati)):

    data = np.load(data_location+"/contact_num_"+comb[0]+"_"+comb[1]+".npy")
    # data = np.load("contact_num.npy")
    json_data = load_json(data_location+"/details_"+comb[0]+"_"+comb[1]+".json")

    # print(comb)
    # print(np.shape(data))
    # print(np.mean(data))

    data = np.squeeze(data)

    extent = [np.nanmin(json_data[comb[0]]), np.nanmax(json_data[comb[0]]),np.nanmax(json_data[comb[1]]),np.nanmin(json_data[comb[1]])]


    plt.figure(figsize=(10,10), layout="constrained")
    plt.imshow(np.swapaxes(data,0,1), extent=extent, aspect="auto")
    plt.xlabel(comb[0])
    plt.ylabel(comb[1])
    plt.gca().invert_yaxis()
    plt.savefig(save_location+"/"+comb[0]+"_"+comb[1]+".png")