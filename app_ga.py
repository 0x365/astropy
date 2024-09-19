import os
import datetime
from tqdm import tqdm
import itertools
import matplotlib.pyplot as plt

# Orbital Maths
from skyfield.api import load, utc
from sgp4.api import Satrec, WGS72
from skyfield.elementslib import osculating_elements_of

# GA
from pymoo.optimize import minimize
from pymoo.core.problem import ElementwiseProblem, Problem
from pymoo.core.mixed import MixedVariableGA
from pymoo.core.variable import Real
from pymoo.optimize import minimize
from pymoo.core.evaluator import Evaluator
from pymoo.core.population import Population

import ctypes
from array import array

from common import *
from ga_fitness import fitness

open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)



pop_size = 200
num_generations = 20
num_start_days = 10

run_mode = "completed" # "time"

os.system("go build -buildmode=c-shared -o ./go_fit.so .")


def flatten_plus_one(real_sat_grid):
    big_grid = np.zeros((len(real_sat_grid)+1, len(real_sat_grid)+1, len(time)))
    big_grid[big_grid == 0] = -1
    big_grid[1:,1:] = real_sat_grid

    flat_grid = []
    for i in range(np.shape(big_grid)[0]):
        for j in range(np.shape(big_grid)[1]):
            flat_grid.extend(big_grid[i,j])

    return flat_grid

class MyProblem(Problem):
    def __init__(self, possible, real_sat_grid, time, mode, **kwargs):
        vars = {
            "argp_i": Real(bounds=(-180, 180)),
            "ecc_i": Real(bounds=(0, 0.14)),
            "inc_i": Real(bounds=(-90, 90)),
            "raan_i": Real(bounds=(-180, 180)),
            "anom_i": Real(bounds=(-180, 180)),
            "mot_i": Real(bounds=(4000, 6500)),
        }
        super().__init__(vars=vars, n_obj=1, **kwargs)
        combs_arr = array('d', (possible).flatten().tolist())
        combs_raw = (ctypes.c_double * len(combs_arr)).from_buffer(combs_arr)
        self.possible = combs_raw
        self.real_sat_grid_flat = np.array(flatten_plus_one(real_sat_grid), dtype=float)
        # self.real_sat_grid = real_sat_grid
        self.depth = np.shape(real_sat_grid)[2]
        self.time = time
        self.mode = mode


    def _evaluate(self, x, out, *args, **kwargs):
        f1 = []
        for val in tqdm(x, desc="Consensus on population"):
            argp_i = val["argp_i"]
            ecc_i = val["ecc_i"]
            inc_i = val["inc_i"]
            raan_i = val["raan_i"]
            anom_i = val["anom_i"]
            mot_i = val["mot_i"]
            # print(val)
            satellite2 = Satrec()
            satellite2.sgp4init(
                WGS72,                      # gravity model
                'i',                        # 'a' = old AFSPC mode, 'i' = improved mode
                25544,                      # satnum: Satellite number
                epoch.days,                 # epoch: days since 1949 December 31 00:00 UT
                3.8792e-05,                 # bstar: drag coefficient (1/earth radii)
                0.0,                        # ndot: ballistic coefficient (radians/minute^2)
                0.0,                        # nddot: mean motion 2nd derivative (radians/minute^3)
                ecc_i,                      # ecco: eccentricity
                np.deg2rad(argp_i),         # argpo: argument of perigee (radians)
                np.deg2rad(inc_i),          # inclo: inclination (radians)
                np.deg2rad(anom_i),         # mo: mean anomaly (radians)
                np.deg2rad(mot_i)/(24*60),  # no_kozai: mean motion (radians/minute)
                np.deg2rad(raan_i),         # nodeo: R.A. of ascending node (radians)
            )
            sim_sat = EarthSatellite.from_satrec(satellite2, ts)
            completed, timer = fitness(sim_sat, satellites, self.possible, self.real_sat_grid_flat.copy(), self.depth, self.time)
            if self.mode == "completed":
                f1.append(-completed)
            elif self.mode == "time":
                f1.append(timer)
            else:
                raise Exception("Mode not correctly defined")
        # f1 = np.squeeze(f1)
        # print(f1)
        out["F"] = f1



for start_day_added in range(num_start_days):
    ts = load.timescale()

    start_date = datetime.datetime(2024,9,11+start_day_added, tzinfo=utc)
    end_date = start_date + relativedelta(days=1)
    time_range = date_range(start_date, end_date, 30, 'seconds')
    time = ts.from_datetimes(time_range)
    epoch = (start_date - datetime.datetime(1949,12,31,0,0, tzinfo=utc))




    satellites = get_icsmd_satellites(open_location+"/active.tle", "icsmd_sats.txt")

    # REMOVE
    # satellites = satellites[:len(satellites)//3]



    ########## Get all valid combinations

    # valid_combs = []
    # valid_combs_time = []
    # for i, x in enumerate(tqdm(satellites, desc="Building possible real satellite combinations")):
    #     for j, y in enumerate(satellites):
    #         if j > i:
    #             barycentric = (x.at(time) - y.at(time)).distance().km
    #             ans = np.where(barycentric <= 500)[0]
    #             if len(ans) > 0:
    #                 valid_combs.append([i, j])
    #                 valid_combs_time.append(ans)

    # valid_combs = np.array(valid_combs)       

    # def checker(temp):
    #     for i, x in enumerate(temp):
    #         for j, y in enumerate(temp):
    #             if j > i:
    #                 if not y in valid_combs[valid_combs[:,0] == x, 1]:
    #                     return False
    #     return True

    # possible = filter(checker, itertools.combinations(np.arange(0,np.amax(valid_combs)), 3))
    # possible = np.array(list(possible))
    possible = np.array(list(itertools.combinations(np.arange(0,len(satellites)+1), 4)))



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


    problem = MyProblem(possible, real_sat_grid, time, run_mode)





    # Generate initial guess from a different satellite
    barycentric = satellites[1].at(ts.from_datetime(start_date))
    orb = osculating_elements_of(barycentric)
    X = {
        'argp_i': orb.argument_of_periapsis.degrees,
        'ecc_i': orb.eccentricity, 
        'inc_i': orb.inclination.degrees, 
        'raan_i': orb.longitude_of_ascending_node.degrees, 
        'anom_i': orb.mean_anomaly.degrees, 
        'mot_i': orb.mean_motion_per_day.degrees
    }
    # X = {
    #     'argp_i': 0,
    #     'ecc_i': 0, 
    #     'inc_i': 0, 
    #     'raan_i': 0, 
    #     'anom_i': 0, 
    #     'mot_i': 0
    # }


    # pop = Population.new("X", [X])
    # Evaluator().eval(problem, pop)









    algorithm = MixedVariableGA(
        pop_size=int(pop_size))#, sampling=pop)

    res = minimize(problem,
                algorithm,
                ("n_gen", int(num_generations)),
                seed=1,
                verbose=True,
                save_history=True)

    print()
    print("------ RESULTS ------")
    print("Maximum consensus:", round(-res.F[0]*100,2), "%")
    print("Orbital Elements:",res.X)

    print()

    out_data = []
    for i in range(len(res.history)):
        out_data.append({
            "gen": i,
            "x": res.history[i].pop.get("X").tolist(),
            "f": res.history[i].pop.get("F")[:,0].tolist()
        })

    save_json("data-ga/long_"+str(start_day_added)+"_"+run_mode+".json", out_data)