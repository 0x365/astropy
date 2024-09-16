import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import itertools 
import datetime

from dateutil.relativedelta import relativedelta
from skyfield.api import load, EarthSatellite, utc
from skyfield.iokit import parse_tle_file
from skyfield.elementslib import osculating_elements_of
from sgp4.api import Satrec, WGS72

from common import *
from ga_fitness import *

########### Setup data paths


open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)


######### Get date and times for analysis

ts = load.timescale()

start_date = datetime.datetime(2024,9,11, tzinfo=utc)
end_date = start_date + relativedelta(days=1)
time_range = date_range(start_date, end_date, 30, 'seconds')
time = ts.from_datetimes(time_range)
epoch = (start_date - datetime.datetime(1949,12,31,0,0, tzinfo=utc))


########### Get orbital elements of all sats


with load.open(save_location+"/active.tle") as f:
    satellites = list(parse_tle_file(f, ts))

print('Loaded', len(satellites), 'satellites')

all_starts = []
all_params = []
for sat in satellites:
    barycentric = sat.at(ts.from_datetime(start_date))

    orbit_elements = osculating_elements_of(barycentric)

    temp = []
    temp.append(orbit_elements.argument_of_periapsis.degrees)
    temp.append(orbit_elements.eccentricity)
    temp.append(orbit_elements.inclination.degrees)
    temp.append(orbit_elements.longitude_of_ascending_node.degrees)
    temp.append(orbit_elements.mean_anomaly.degrees)
    temp.append(orbit_elements.mean_motion_per_day.degrees)
    all_params.append(temp)

all_params = np.array(all_params)

all_params_mean = np.nanmean(all_params,axis=0)
all_params_std = np.nanstd(all_params,axis=0)
all_params_min = all_params_mean - 3*all_params_std
all_params_max = all_params_mean + 3*all_params_std


############## Get icmsd satellites


satellites = get_icsmd_satellites(open_location+"/active.tle", "icsmd_sats.txt")
# satellites = get_random_satellites(open_location+"/active.tle")


######## Determine satellites that could be useful in 4 participant consensus

valid_combs = []
valid_combs_time = []
for i, x in enumerate(tqdm(satellites)):
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

possible = filter(checker, itertools.combinations(np.arange(0,np.amax(valid_combs)), 3))
possible = np.array(list(possible))
# satellites = np.array(satellites)[np.array(np.unique(possible),dtype=int)]

############# Real satellite grid

big_comb = np.array(satellites)

real_sat_grid = np.zeros((len(big_comb), len(big_comb), len(time)))
real_sat_grid[real_sat_grid == 0] = np.nan

for i in tqdm(range(len(big_comb)), desc="Generate real satellite's interactions"):
    for j in range(len(big_comb)):
        if i != j:
            x = np.where((big_comb[i].at(time) - big_comb[j].at(time)).distance().km <= 500)[0]
            real_sat_grid[i,j,:len(x)] = x
            real_sat_grid[j,i,:len(x)] = x

#############


combinati = itertools.combinations(["argp","ecc","inc","raan","anom","mot"],2)

quality = 10

for comb in tqdm(list(combinati)):
    if "argp" in comb:
        argp = np.linspace(-180, 180, quality)
    else:
        argp = [all_params_mean[0]]
    if "ecc" in comb:
        ecc = np.linspace(0, all_params_max[1], quality)
    else:
        ecc = [all_params_mean[1]]
    if "inc" in comb:
        inc = np.linspace(-90, 90, quality)
    else:
        inc = [all_params_mean[2]]
    if "raan" in comb:
        raan = np.linspace(-180, 180, quality)
    else:
        raan = [all_params_mean[3]]
    if "anom" in comb:
        anom = np.linspace(-180, 180, quality)
    else:
        anom = [all_params_mean[4]]
    if "mot" in comb:
        mot = np.linspace(4000, 6500, quality)
    else:
        mot = [all_params_mean[5]]


    all_elements = [argp, ecc, inc, raan, anom, mot]

    # out_data = np.zeros((len(argp),len(ecc),len(inc),len(raan),len(anom),len(mot)))
    # out_data2 = np.zeros((len(argp),len(ecc),len(inc),len(raan),len(anom),len(mot)))
    out_data3 = np.zeros((len(argp),len(ecc),len(inc),len(raan),len(anom),len(mot)))

    save_json(save_location+"/details_"+comb[0]+"_"+comb[1]+".json", {
        "argp": np.array(argp).tolist(),
        "ecc": np.array(ecc).tolist(),
        "inc": np.array(inc).tolist(),
        "raan": np.array(raan).tolist(),
        "anom": np.array(anom).tolist(),
        "mot": np.array(mot).tolist(),
    })

    for i1, argp_i in enumerate(tqdm(argp)):
        for i2, ecc_i in enumerate((ecc)):
            for i3, inc_i in enumerate(inc):
                for i4, raan_i in enumerate(raan):
                    for i5, anom_i in enumerate(anom):
                        for i6, mot_i in enumerate(mot):

                            ######## Generate simulated sallite
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
                            sat = EarthSatellite.from_satrec(satellite2, ts)                            
                            sim_sats = [sat]

                            completed, _ = fitness_multi_sat(sim_sats, satellites, possible.copy(), real_sat_grid, time)
                            out_data3[i1,i2,i3,i4,i5,i6] = -completed

                            # ######### Compare simulated satellite against all real satellites in subset
                            # contact_time = 0
                            # contact_num = 0

                            # for sat_real in satellites:
                            #     barycentric = (sat.at(time) - sat_real.at(time)).distance().km
                            #     sizer = np.shape(np.where(barycentric <= 500)[0])[0]
                            #     contact_time += sizer
                            #     if sizer > 0:
                            #         contact_num += 1

                            # out_data[i1,i2,i3,i4,i5,i6] = contact_time
                            # out_data2[i1,i2,i3,i4,i5,i6] = contact_num
                            

        # np.save(save_location+"/contact_time_"+comb[0]+"_"+comb[1], out_data)
        # np.save(save_location+"/contact_num_"+comb[0]+"_"+comb[1], out_data2)
        np.save(save_location+"/contact_consensus_"+comb[0]+"_"+comb[1], out_data3)
    

    # np.save(save_location+"/contact_time_"+comb[0]+"_"+comb[1], out_data)
    # np.save(save_location+"/contact_num_"+comb[0]+"_"+comb[1], out_data2)
    np.save(save_location+"/contact_consensus_"+comb[0]+"_"+comb[1], out_data3)













