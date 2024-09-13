# WIP - Currently only takes into account sim sat as primary


import numpy as np


# Function to check consensus based on communication rounds and a grid of satellites
def consensus(comm, small_grid):
    # Time array for end of previous round for each communication
    t_local = np.zeros(np.shape(small_grid)[0])

    # Iterate through communication rounds and process satellite pairs for each round
    for _, conn_round in enumerate(comm):
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
def fitness(sim_sat, satellites, possible, real_sat_grid, time):
    
    possible += 1

    big_grid = np.zeros((len(satellites)+1, len(satellites)+1, len(time)))
    big_grid[big_grid == 0] = np.nan
    big_grid[1:,1:] = real_sat_grid

    for i in range(len(satellites)):
        x = np.where((sim_sat.at(time) - satellites[i].at(time)).distance().km <= 500)[0]
        big_grid[i+1,0,:len(x)] = x
        big_grid[0,i+1,:len(x)] = x

    c = 0
    time_li = []
    for small_comb in possible:
        small_grid = big_grid[[0,*small_comb]][:,[0,*small_comb]]
        comm =  [
            [[0,1],[0,2],[0,3]],
            [[1,0],[1,2],[1,3], [2,0],[2,1],[2,3], [3,0],[3,1],[3,2]],
            [[0,1],[0,2],[0,3], [1,0],[1,2],[1,3], [2,0],[2,1],[2,3], [3,0],[3,1],[3,2]],
            [[1,0],[2,0],[3,0]]
        ]
        completed, times = consensus(comm, small_grid)
        if completed:
            c += 1
            time_li.append(times)
    if c == 0:
        time_li.append(0)
    return c/len(possible), np.mean(time_li)