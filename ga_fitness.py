# WIP - Currently only takes into account sim sat as primary


import numpy as np
import os
import ctypes
from array import array
from pytictoc import TicToc

# Function to check consensus based on communication rounds and a grid of satellites
def consensus(comm, small_grid):
    # Time array for end of previous round for each communication
    t_local = np.zeros(np.shape(small_grid)[0])

    # Iterate through communication rounds and process satellite pairs for each round
    for c, conn_round in enumerate(comm):
        t_local_next = t_local.copy()
        for i,j in conn_round:
            x = small_grid[i,j][small_grid[i,j] >= t_local[i]]
            if len(x) > 0:
                y = np.amin(x)
                if y > t_local_next[j]:
                    t_local_next[j] = y
            else:
                return False, -1
        # Update time arrary as round has ended
        t_local = t_local_next.copy()

    return True, np.amax(t_local)



# Function to evaluate the fitness of satellite communication by counting successful connections
def fitness(sim_sat, satellites, possible, real_sat_grid, depth, time):

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
    # print("Load Library")
    # Ticcer.toc()

    # Ticcer.tic()
    for i in range(1,len(satellites)+1):
        x = np.where((sim_sat.at(time) - satellites[i-1].at(time)).distance().km <= 500)[0]
        real_sat_grid[i*depth:(i*depth)+len(x)] = x
        real_sat_grid[(i*(len(satellites)+1))*depth:((i*(len(satellites)+1))*depth)+len(x)] = x
    # print("Get sim sat pos")
    # Ticcer.toc()
    
    # Ticcer.tic()
    sizer = len(real_sat_grid)
    grid_raw = real_sat_grid.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    # print("To ctype conversion")
    # Ticcer.toc()

    num_sats = int(len(satellites))+1

    # Ticcer.tic()
    c = conn1(possible, len(possible), grid_raw, sizer, num_sats)
    # print("Run consensus")
    # Ticcer.toc()

    return c/len(possible), c#, np.mean(time_li)



# # Function to evaluate the fitness of satellite communication by counting successful connections
# def fitness_multi_sat(sim_sats, satellites, possible, real_sat_grid, time, b):
    
#     possible += len(sim_sats)

#     big_grid = np.zeros((len(satellites)+len(sim_sats), len(satellites)+len(sim_sats), len(time)))
#     big_grid[big_grid == 0] = np.nan
#     big_grid[len(sim_sats):,len(sim_sats):] = real_sat_grid

#     # Compare sim sats against each other
#     for j in range(len(sim_sats)):
#         for i in range(len(sim_sats)):
#             if i != j:
#                 x = np.where((sim_sats[j].at(time) - sim_sats[i].at(time)).distance().km <= 500)[0]
#                 if len(x) == 0:
#                     return -1, 0
#                 big_grid[i,j,:len(x)] = x
#                 big_grid[j,i,:len(x)] = x

#     # Compare sim sats against real sats
#     for j in range(len(sim_sats)):
#         for i in range(len(satellites)):
#             x = np.where((sim_sats[j].at(time) - satellites[i].at(time)).distance().km <= 500)[0]
#             if len(x) > b:
#                 b = len(x)
#             big_grid[i+len(sim_sats),0,:len(x)] = x
#             big_grid[0,i+len(sim_sats),:len(x)] = x

#     big_grid = big_grid[:,:,:b+1]    

#     ############# ACCELERATE WITH GOLANG
#     c = 0
#     time_li = []
#     for small_comb in possible:
#         small_grid = big_grid[[*np.arange(len(sim_sats)),*small_comb]][:,[*np.arange(len(sim_sats)),*small_comb]]
#         comm =  [
#             [[0,1],[0,2],[0,3]],
#             [[1,0],[1,2],[1,3], [2,0],[2,1],[2,3], [3,0],[3,1],[3,2]],
#             [[0,1],[0,2],[0,3], [1,0],[1,2],[1,3], [2,0],[2,1],[2,3], [3,0],[3,1],[3,2]],
#             [[1,0],[2,0],[3,0]]
#         ]
#         completed, times = consensus(comm, small_grid)
#         if completed:
#             c += 1
#             time_li.append(times)
#     if c == 0:
#         time_li.append(0)
#     ############# ACCELERATE WITH GOLANG

#     return c/len(possible), np.mean(time_li)