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

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)




ts = load.timescale()

with load.open(save_location+"/active.tle") as f:
    satellites = list(parse_tle_file(f, ts))

print('Loaded', len(satellites), 'satellites')

all_starts = []
all_params = []
for sat in satellites:
    barycentric = sat.at(ts.utc(2024, 1, 1, 0, 0, 0))
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

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(all_starts[:,0],all_starts[:,1],all_starts[:,2])
ax.set_xlim([-50000, 50000])
ax.set_ylim([-50000, 50000])
ax.set_zlim(-50000, 50000)
plt.savefig("test.png")

fig = plt.figure()
all_params_plot = (all_params-np.nanmean(all_params,axis=0))/(3*np.nanstd(all_params,axis=0))
plt.violinplot(all_params_plot, [0,1,2,3,4,5], showmeans=False, showextrema=False, showmedians=False)
plt.ylim([-1,1])
plt.savefig("test2.png")

csv_output(save_location+"/start_params_real.csv", all_starts)






import datetime
from dateutil.relativedelta import relativedelta
from skyfield.api import utc

def date_range(start_date, end_date, increment, period):
    result = []
    nxt = start_date
    delta = relativedelta(**{period:increment})
    while nxt <= end_date:
        result.append(nxt)
        nxt += delta
    return result


start_date = datetime.datetime(2024,1,1, tzinfo=utc)
# print(start_date)
end_date = start_date + relativedelta(days=1)
time_range = date_range(start_date, end_date, 30, 'seconds')
time = ts.from_datetimes(time_range)

all_satellites = satellites.copy()
satellites = satellites[:20]


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
# print(np.shape(valid_combs))
# print(valid_combs)


def checker(temp):
    for i, x in enumerate(temp):
        for j, y in enumerate(temp):
            if j > i:
                if not y in valid_combs[valid_combs[:,0] == x, 1]:
                    return False
    return True


possible = filter(checker, itertools.combinations(np.arange(0,np.amax(valid_combs)), 3))
possible = np.array(list(possible))
# print(np.shape(possible))
# print(possible)
# print(all_satellites)
satellites = np.array(all_satellites)[np.array(np.unique(possible),dtype=int)]

epoch = (start_date - datetime.datetime(1949,12,31,0,0, tzinfo=utc))

all_params_mean = np.nanmean(all_params,axis=0)
all_params_std = np.nanstd(all_params,axis=0)
all_params_min = all_params_mean - 3*all_params_std
all_params_max = all_params_mean + 3*all_params_std


argp = [all_params_mean[0]]
argp = np.linspace(all_params_min[0], all_params_max[0], 30)
ecc = [all_params_mean[1]]
ecc = np.linspace(0, all_params_max[1], 30)
inc = [all_params_mean[2]]
inc = np.linspace(all_params_min[2], all_params_max[2], 30)
raan = [all_params_mean[3]]
raan = np.linspace(all_params_min[3], all_params_max[3], 30)
anom = [all_params_mean[4]]
# anom = np.linspace(all_params_min[4], all_params_max[4], 30)
mot = [all_params_mean[5]]
# mot = np.linspace(all_params_min[5], all_params_max[5], 50)

all_elements = [argp, ecc, inc, raan, anom, mot]

out_data = np.zeros((len(argp),len(ecc),len(inc),len(raan),len(anom),len(mot)))
out_data2 = np.zeros((len(argp),len(ecc),len(inc),len(raan),len(anom),len(mot)))

for i1, argp_i in enumerate(tqdm(argp)):
    for i2, ecc_i in enumerate((ecc)):
        for i3, inc_i in enumerate(inc):
            for i4, raan_i in enumerate(raan):
                for i5, anom_i in enumerate(anom):
                    for i6, mot_i in enumerate(mot):
                        # print(mot_i)
                        satellite2 = Satrec()
                        satellite2.sgp4init(
                            WGS72,                # gravity model
                            'i',                  # 'a' = old AFSPC mode, 'i' = improved mode
                            25544,                # satnum: Satellite number
                            epoch.days,                # epoch: days since 1949 December 31 00:00 UT
                            3.8792e-05,           # bstar: drag coefficient (1/earth radii)
                            0.0,                  # ndot: ballistic coefficient (radians/minute^2)
                            0.0,                  # nddot: mean motion 2nd derivative (radians/minute^3)
                            ecc_i,            # ecco: eccentricity
                            np.deg2rad(argp_i),   # argpo: argument of perigee (radians)
                            np.deg2rad(inc_i),   # inclo: inclination (radians)
                            np.deg2rad(anom_i),   # mo: mean anomaly (radians)
                            np.deg2rad(mot_i)/(24*60),  # no_kozai: mean motion (radians/minute)
                            np.deg2rad(raan_i),    # nodeo: R.A. of ascending node (radians)
                        )
                        sat = EarthSatellite.from_satrec(satellite2, ts)
                        # print(sat.at(time).position.km)
                        contact_time = 0
                        contact_num = 0
                        for sat_real in satellites:
                            barycentric = (sat.at(time) - sat_real.at(time)).distance().km
                            contact_time += np.shape(np.where(barycentric <= 500)[0])[0]
                            contact_num += 1

                        out_data[i1,i2,i3,i4,i5,i6] = contact_time
                        out_data2[i1,i2,i3,i4,i5,i6] = contact_num


# print(out_data)
# print("SUM", np.sum(out_data))


save_json(save_location+"/details.json", {
    "argp": np.array(argp).tolist(),
    "ecc": np.array(ecc).tolist(),
    "inc": np.array(inc).tolist(),
    "raan": np.array(raan).tolist(),
    "anom": np.array(anom).tolist(),
    "mot": np.array(mot).tolist(),
})
np.save(save_location+"/contact_time", out_data)
np.save(save_location+"/contact_num", out_data2)
