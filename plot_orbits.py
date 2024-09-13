import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import itertools 

from skyfield.api import load, EarthSatellite
from skyfield.iokit import parse_tle_file
from skyfield.elementslib import osculating_elements_of
from sgp4.api import Satrec, WGS72

from common import *

open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
if not os.path.exists(save_location):
    os.makedirs(save_location)





ts = load.timescale()

with load.open(open_location+"/active.tle") as f:
    satellites = list(parse_tle_file(f, ts))

print('Loaded', len(satellites), 'satellites')

all_starts = []
all_params = []
for sat in satellites:
    barycentric = sat.at(ts.utc(2024, 9, 11, 0, 0, 0))
    all_starts.append(np.append(barycentric.position.km, barycentric.velocity.km_per_s))
    orbit_elements = osculating_elements_of(barycentric)

    temp = []
    temp.append(orbit_elements.argument_of_periapsis.degrees)
    temp.append(orbit_elements.eccentricity)
    temp.append(orbit_elements.inclination.degrees)
    temp.append(orbit_elements.longitude_of_ascending_node.degrees)
    temp.append(orbit_elements.mean_anomaly.degrees)
    temp.append(orbit_elements.mean_motion_per_day.degrees)
    all_params.append(temp)

all_starts = np.array(all_starts)
all_params = np.array(all_params)


# print(np.shape())
all_params = all_params[(np.sum(np.isnan(all_starts),axis=1))==0]
all_starts = all_starts[(np.sum(np.isnan(all_starts),axis=1))==0]

# print(all_starts)
# print(all_params)

fig = plt.figure(figsize=(10,10), layout="constrained")
ax = fig.add_subplot(projection='3d')
ax.scatter(all_starts[:,0],all_starts[:,1],all_starts[:,2])
ax.set_xlim([-50000, 50000])
ax.set_ylim([-50000, 50000])
ax.set_zlim(-50000, 50000)
plt.savefig(save_location+"/orbit_map_of_all_sats.png")

fig = plt.figure()
all_params_plot = (all_params-np.nanmean(all_params,axis=0))/(3*np.nanstd(all_params,axis=0))
plt.violinplot(all_params_plot, [0,1,2,3,4,5], showmeans=False, showextrema=False, showmedians=False)
plt.ylim([-1,1])
plt.xticks([0,1,2,3,4,5], ["ARGP", "ECC", "INC", "RAAN", "MA", "MM"])
plt.savefig(save_location+"/orbital_elements_of_all_sats.png")










satellites = get_icsmd_satellites(open_location+"/active.tle", "icsmd_sats.txt")
# satellites = get_random_satellites(open_location+"/active.tle")


all_starts = []
all_params = []
for sat in satellites:
    barycentric = sat.at(ts.utc(2024, 9, 11, 0, 0, 0))
    all_starts.append(np.append(barycentric.position.km, barycentric.velocity.km_per_s))
    orbit_elements = osculating_elements_of(barycentric)

    temp = []
    temp.append(orbit_elements.argument_of_periapsis.degrees)
    temp.append(orbit_elements.eccentricity)
    temp.append(orbit_elements.inclination.degrees)
    temp.append(orbit_elements.longitude_of_ascending_node.degrees)
    temp.append(orbit_elements.mean_anomaly.degrees)
    temp.append(orbit_elements.mean_motion_per_day.degrees)
    all_params.append(temp)

all_starts = np.array(all_starts)
all_params = np.array(all_params)


# print(np.shape())
all_params = all_params[(np.sum(np.isnan(all_starts),axis=1))==0]
all_starts = all_starts[(np.sum(np.isnan(all_starts),axis=1))==0]


fig = plt.figure(figsize=(10,10), layout="constrained")
ax = fig.add_subplot(projection='3d')
ax.scatter(all_starts[:,0],all_starts[:,1],all_starts[:,2])
ax.set_xlim([-50000, 50000])
ax.set_ylim([-50000, 50000])
ax.set_zlim(-50000, 50000)
plt.savefig(save_location+"/subgroup_orbit_map_of_all_sats.png")

fig = plt.figure()
all_params_plot = (all_params-np.nanmean(all_params,axis=0))/(3*np.nanstd(all_params,axis=0))
plt.violinplot(all_params_plot, [0,1,2,3,4,5], showmeans=False, showextrema=False, showmedians=False)
plt.ylim([-1,1])
plt.xticks([0,1,2,3,4,5], ["ARGP", "ECC", "INC", "RAAN", "MA", "MM"])
plt.savefig(save_location+"/subgroup_orbital_elements_of_all_sats.png")