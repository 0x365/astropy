import numpy as np
import os
import ctypes
from array import array
from pytictoc import TicToc

import datetime
from tqdm import tqdm
import itertools
import matplotlib.pyplot as plt

# Orbital Maths
from skyfield.api import load, utc
from sgp4.api import Satrec, WGS72
from skyfield.elementslib import osculating_elements_of

from common import *

os.system("go build -buildmode=c-shared -o ./go_fit.so .")

def fitness_no_sim(satellites, possible, real_sat_grid):

    Ticcer = TicToc()
    # Ticcer.tic()
    library = ctypes.cdll.LoadLibrary("./go_fit.so")
    conn1 = library.consensus_completeness_per
    conn1.restype = ctypes.c_int64

    conn1.argtypes = [
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_int64,
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_int64,
        ctypes.c_int64
    ]
    
    # Ticcer.tic()
    sizer = len(real_sat_grid)
    grid_raw = real_sat_grid.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    # print("To ctype conversion")
    # Ticcer.toc()

    num_sats = int(len(satellites))

    possible_1 = array('d', (possible).flatten().tolist())
    possible_raw = (ctypes.c_double * len(possible_1)).from_buffer(possible_1)

    # Ticcer.tic()
    c = conn1(possible_raw, len(possible_raw), grid_raw, sizer, num_sats)

    return c



open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)

for xxx in range(10):
    ts = load.timescale()

    start_date = datetime.datetime(2024,9,11, tzinfo=utc)
    end_date = start_date + relativedelta(days=1+xxx)
    time_range = date_range(start_date, end_date, 30, 'seconds')
    time = ts.from_datetimes(time_range)
    epoch = (start_date - datetime.datetime(1949,12,31,0,0, tzinfo=utc))





    satellites = get_icsmd_satellites(open_location+"/active.tle", "icsmd_sats.txt")

    # REMOVE
    # satellites = satellites[:len(satellites)//3]



    ########## Get all valid combinations

    valid_combs = []
    valid_combs_time = []
    for i, x in enumerate(tqdm(satellites, desc="Building possible real satellite combinations")):
        for j, y in enumerate(satellites):
            if j > i:
                barycentric = (x.at(time) - y.at(time)).distance().km
                ans = np.where(barycentric <= 500)[0]
                if len(ans) > 0:
                    valid_combs.append([i, j])
                    valid_combs_time.append(ans)

    valid_combs = np.array(valid_combs)       

    def checker(temp):
        for i, x in enumerate(temp):
            for j, y in enumerate(temp):
                if j > i:
                    if not y in valid_combs[valid_combs[:,0] == x, 1]:
                        return False
        return True

    # possible = filter(checker, itertools.combinations(np.arange(0,np.amax(valid_combs)), 4))
    # possible = np.array(list(possible))
    possible = np.array(list(itertools.combinations(np.arange(0,np.amax(valid_combs)), 4)))


    ######### Create real sat grid

    big_comb = np.array(satellites)

    real_sat_grid = np.zeros((len(big_comb), len(big_comb), len(time)))
    real_sat_grid[real_sat_grid == 0] = -1

    for i in tqdm(range(len(big_comb)), desc="Generate real satellite's interactions"):
        for j in range(len(big_comb)):
            if i != j:
                x = np.where((big_comb[i].at(time) - big_comb[j].at(time)).distance().km <= 500)[0]
                real_sat_grid[i,j,:len(x)] = x
                real_sat_grid[j,i,:len(x)] = x

    def flattener(real_sat_grid):

        flat_grid = []
        for i in range(np.shape(real_sat_grid)[0]):
            for j in range(np.shape(real_sat_grid)[1]):
                flat_grid.extend(real_sat_grid[i,j])

        return flat_grid




    flat_sat_grid = np.array(flattener(real_sat_grid), dtype=float)

    print("Number of days:", 1+xxx)

    completed = fitness_no_sim(satellites, possible, flat_sat_grid)

    print(completed/(len(possible)*4))










###### For no simulated satellites
# [1 day = 0,                       0 out of 79 sats]
# [2 day = 4.346530662320136e-05,   12 out of 79 sats]
# [3 day = 0.0006176279860490387,   49 out of 79 sats]
# [4 day = 0.009457209457209457,    66 out of 79 sats]
# [5 day = 0.03995811206337522,     68 out of 79 sats]
# [6 day = 0.09982123140017878,     69 out of 79 sats]
# [7 day = 0.1948612790718054,      70 out of 79 sats]
# [8 day = 0.30194945405471724,     71 out of 79 sats]
# [9 day = 0.3801400354031933,      72 out of 79 sats]
# [10 day = 0.45094957673905045,    72 out of 79 sats]



