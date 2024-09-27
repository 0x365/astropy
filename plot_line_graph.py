import os
import numpy as np
import datetime
import matplotlib.pyplot as plt
from tqdm import tqdm
import itertools 
import matplotlib.animation as animation

from skyfield.api import load, EarthSatellite
from skyfield.iokit import parse_tle_file
from skyfield.elementslib import osculating_elements_of
from sgp4.api import Satrec, WGS72

import ctypes
from array import array

from common import *


open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data-animation")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
if not os.path.exists(save_location):
    os.makedirs(save_location)

ccc = 0
plt.figure(figsize=(6.5,4), layout="constrained")
meaner = []
for ii in [0,1,2,3,4,5,6,7,8,9,"special", "special2"]:
    all_plots = []
    try:
        for i in range(10):
            try:
                animation_data = load_json(open_location+"/animation_data_optday_"+str(ii)+"_proccessday_"+str(i)+".json")
            except:
                continue

            plot_data = []
            plot_data2 = []
            time_data = []

            for frame in range(len(animation_data)):

                # print("Frame number:", frame)

                completed_no_sim = np.array(animation_data[frame]["completed_no_sim"])
                completed_with_sim = np.array(animation_data[frame]["completed_with_sim"])  

                time_data.append(animation_data[frame]["time_minutes"]/(24*60))

                ########## Fig 3

                if len(completed_no_sim) > 0:
                    plot_data.append(len(completed_no_sim))
                else:
                    plot_data.append(0)
                if len(completed_with_sim) > 0:
                    adder = len(completed_with_sim)
                    if 0 in completed_with_sim:
                        adder -= 1
                    plot_data2.append(adder)
                else:
                    plot_data2.append(0)
            
            all_plots.append([plot_data, plot_data2])
        all_plots = np.array(all_plots)
        if ii == "special" or ii == "special2":
            if len(all_plots) > 0:
                plt.plot(time_data, np.mean(all_plots[:,1]-all_plots[:,0],axis=0), color=["crimson","gold"][ccc], label="Mean - "+ii, alpha=0.5)
                ccc += 1
        else:
            plt.plot(time_data, np.mean(all_plots[:,1]-all_plots[:,0],axis=0), color="black", alpha=0.1)
            meaner.append(np.mean(all_plots[:,1]-all_plots[:,0],axis=0))
    except:
        pass
plt.plot(time_data, np.mean(meaner,axis=0), color="blue", alpha=0.5, label="Mean of single opt")
plt.legend(loc="lower right")
plt.xlim([0,0.1])
# plt.ylim([0,1])
plt.xlabel("Time (Days)")
plt.ylabel("Number of extra satellites")
plt.title("Mean number of satellites across all days for each optimised value", fontsize=10)

plt.savefig(save_location+"/line_graph.png")
