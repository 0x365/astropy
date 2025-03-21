import matplotlib.pyplot as plt
import numpy as np
import csv
from numpy.linalg import norm

from scipy.integrate import solve_ivp

from propagator import propagated, propagated2, propagated3
from prop import prop
from skimage import metrics
from shapely import LineString, hausdorff_distance, frechet_distance
from scipy.optimize import minimize
from scipy.optimize import curve_fit
import scipy

from pytictoc import TicToc

# step1

p_1_li = []
p_2_li = []
p_3_li = []

# IDEAS
# Use ai to try to decide where 3rd body should be to be stable
# Use ai to work out if the orbit starts repeating itself and is therefore stable


def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)
    f.close()
    return output

Ticcer = TicToc()

# Group 1

# input_data = np.array(csv_input("patterns_arxiv_1303dot0181.csv"))[1:]

# for i in input_data:
#     v_1 = float(i[1])
#     v_2 = float(i[2])
#     file_name = "data_1/"+i[0]
#     m3 = 1
#     time = 100
#     timestep = 1000
#     propagated(v_1, v_2, m3, file_name, time=time, timestep=timestep)


# # Group 2

# input_data = np.array(csv_input("patterns_arxiv_1709dot04775.csv"))[1:]

# for i in input_data:
#     v_1 = float(i[4])
#     v_2 = float(i[5])
#     file_name = "data_2/"+str(i[0])
#     m3 = float(i[3])
#     time = 100
#     timestep = 1000
#     propagated(v_1, v_2, m3, file_name, time=time, timestep=timestep)




# file_name = "data/fig8"
# v_1, v_2 = 0.3471128135672417,0.532726851767674
# # v_1, v_2 = 0.34711,0.532726851767674
# # v_1, v_2 = np.pi/9, 0.532726851767674
# m3 = 1
# loops = 200
# time = loops*np.pi
# timestep = loops*50+1
# propagated(v_1, v_2, m3, file_name, time=time, timestep=timestep)
# propagated3(v_1, v_2, m3, file_name, time=time, timestep=timestep)









def fit_func(v_in):
    v_1, v_2 = v_in

    m1,m2,m3 = 1,1,1

    r1x = -1
    r1y = 0
    r2x = 1
    r2y = 0
    r3x = 0
    r3y = 0
    v1x = v_1
    v1y = v_2
    v2x = v_1
    v2y = v_2
    v3x = -2*v_1/m3
    v3y = -2*v_2/m3
    initial = [m1,m2,m3,r1x,r1y,r2x,r2y,r3x,r3y,v1x,v1y,v2x,v2y,v3x,v3y]

    loops = 30
    per_loop = 100
    time = loops
    timestep = loops*per_loop
    total_steps = loops*per_loop
    file_name = "data/fig8"

    r1, r2, r3 = prop(initial, file_name, time=time, timestep=timestep, do_plot=True)
    
    if len(r1) == 0:
        print(v_in)
        return 100

    # print(np.shape(r1))
    r1_norm = norm([r1[0]-r1[0,0],r1[1]-r1[1,0]],axis=0)
    r2_norm = norm([r2[0]-r2[0,0],r2[1]-r2[1,0]],axis=0)
    r3_norm = norm([r3[0]-r3[0,0],r3[1]-r3[1,0]],axis=0)
    r_mean = np.mean([r1_norm,r2_norm,r3_norm], axis=0)
    

    peaks = scipy.signal.find_peaks(r_mean, distance=per_loop*2)[0]
    # print(peaks)
    found = False
    if len(peaks) >= 2:
        for j in range(1, len(peaks)):
            if peaks[j]-peaks[0] > 1.6*peaks[0] and peaks[j]-peaks[0] < 2.4*peaks[0]:
                found = True
                break
    if not found:
        print(v_in)
        print("No periodicity found")
        return 50
    
    wavelength = peaks[1]-peaks[0]
    loops = int(np.floor(total_steps/wavelength))

    # plt.plot(np.arange(len(r_mean)), r_mean)
    # print(peaks)
    # plt.scatter(peaks,[1.5]*len(peaks))
    
    # plt.legend()
    # plt.savefig("data/tester.png")
    # plt.clf()

    start_set = [r1[:,:wavelength], r2[:,:wavelength], r3[:,:wavelength]]

    r1_change = []
    r2_change = []
    r3_change = []

    r1 = np.swapaxes(r1,0,1)
    r2 = np.swapaxes(r3,0,1)
    r3 = np.swapaxes(r3,0,1)
    start_set = np.swapaxes(start_set,1,2)

    for i in range(loops):
        r1_change.append(hausdorff_distance(LineString(r1[i*wavelength:(i+1)*wavelength]), LineString(start_set[0])))
        r2_change.append(hausdorff_distance(LineString(r2[i*wavelength:(i+1)*wavelength]), LineString(start_set[1])))
        r3_change.append(hausdorff_distance(LineString(r3[i*wavelength:(i+1)*wavelength]), LineString(start_set[2])))

    r1_change = np.array(r1_change)
    r2_change = np.array(r2_change)
    r3_change = np.array(r3_change)

    fitness = np.std(np.mean([r1_change, r2_change, r3_change],axis=0))

    print(v_in, fitness)

    return fitness


# res = minimize(fit_func, x0=[np.pi/8, 0.532726851767674], method="Nelder-Mead")
# print(res)

grid_size = 100
try:
    grid = np.load("grid.npy")
    if np.shape(grid)[0] == grid_size:
        grid_bool = np.logical_not(np.isnan(grid))
    else:
        grid = np.zeros((grid_size,grid_size))
        grid[grid == 0] = np.nan
        grid_bool = np.logical_not(np.isnan(grid))
except:
    grid = np.zeros((grid_size,grid_size))
    grid[grid == 0] = np.nan
    grid_bool = np.logical_not(np.isnan(grid))


counters = np.linspace(-1,1, grid_size)

print(counters)
for ii, i in enumerate(counters):
    if ii == grid_size-1 or np.sum(grid_bool[ii+1]) == 0:
        for jj, j in enumerate(counters):
            if np.sqrt(i**2 + j**2) <= 0.9:
                grid[ii,jj] = fit_func([float(i), float(j)])
            else:
                grid[ii,jj] == np.nan
        np.save("grid", grid)
np.save("grid", grid)



# print(fit_func([np.pi/7, 0.532726851767674]))
# print(fit_func([0.3471128135672417,0.532726851767674]))
# print(fit_func([-0.7373737373737373,-0.010101010101010055]))











# outfit = [[0.3471128135672417,0.532726851767674],
#           [np.pi/9, 0.532726851767674],
#           [np.pi/8, 0.532726851767674]]



# Turn into gif
# tt = 1/np.sqrt(6.67e-11 * 1.99e30 / (1.5e11)**3 ) # seconds
# tt = tt / (60*60 * 24* 365.25) * np.diff(t)[0] # per time step (in years)
# def animate(i):
#     ln1.set_data([sol.y[0][i], sol.y[2][i], sol.y[4][i]], [sol.y[1][i], sol.y[3][i], sol.y[5][i]])
#     text.set_text('Time = {:.1f} Years'.format(i*tt))
# fig, ax = plt.subplots(1,1, figsize=(8,8))
# ax.grid()
# ln1, = plt.plot([], [], 'ro', lw=3, markersize=6)
# text = plt.text(0, 1.75, 'asdasd', fontsize=20, backgroundcolor='white', ha='center')
# ax.set_ylim(-2, 2)
# ax.set_xlim(-2,2)
# ani = animation.FuncAnimation(fig, animate, frames=len(t), interval=50)
# ani.save('plan.gif',writer='pillow',fps=30)