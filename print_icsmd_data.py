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

satellites = get_satellites("active.tle", refine_by_name="icsmd_sats.txt")
# satellites = get_random_satellites(open_location+"/active.tle")

ts = load.timescale()
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


all_params = np.array(all_params, dtype=float)

# for i in range(len(all_params)):
#     if all_params[i,0] > 180:
#         all_params[i,0] = 360 - all_params[i,0]
# print(all_params[:,0])
all_params[all_params[:,0] > 180,0] = all_params[all_params[:,0] > 180,0] - 360
# all_all_params[all_all_params[:,0] > 180,0] = all_all_params[all_all_params[:,0] > 180,0] -360
# print(all_params[:,0])
all_params[:,1] = (all_params[:,1]) # Log Eccentricity
# all_all_params[:,1] = (all_all_params[:,1]) # Log Eccentricity
all_params[all_params[:,2] < 90,2] = 180 - all_params[all_params[:,2] < 90,2]
all_params[:,2] = all_params[:,2] - 90
# all_params[all_params[:,2] >= 90,2] = all_params[all_params[:,2] >= 90,2] - 90
# all_params[all_params[:,2] < 90,2] = 180 - all_params[all_params[:,2] < 90,2]
# all_all_params[all_all_params[:,2] > 90,2] = all_all_params[all_all_params[:,2] > 90,2] - 180
# print(all_params[:,2])
all_params[all_params[:,3] > 180,3] = all_params[all_params[:,3] > 180,3] - 360
# all_all_params[all_all_params[:,3] > 180,3] = all_all_params[all_all_params[:,3] > 180,3] -360

all_params[all_params[:,4] > 180,4] = all_params[all_params[:,4] > 180,4] - 360
# all_all_params[all_all_params[:,4] > 180,4] = all_all_params[all_all_params[:,4] > 180,4] -360

all_params[:,5] = all_params[:,5]/360

# all_params = np.around(all_params, 4)

print(np.shape(all_params))

import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

# Creating a sample dataset
data = {
    "Class": ["ICSMD Satellites"]*np.shape(all_params)[0],
    'ARGP': all_params[:,0],
    'ECC': all_params[:,1],
    'INC': all_params[:,2],
    'RAAN': all_params[:,3],
    'ANOM': all_params[:,4],
    'MOT': all_params[:,5],
}

data_result = {
    "Class": "Simulated Satellite",
    'ARGP': [-125.239492],
    'ECC': [0.00555023937],
    'INC': [-82.6515415],
    'RAAN': [-31.2498591],
    'ANOM': [-59.4895235],
    'MOT': [15.1931995],
}

# Converting the dataset into a pandas DataFrame
df = pd.DataFrame(data)
df_result = pd.DataFrame(data_result)

# Create a figure
fig, ax = plt.subplots(figsize=(10, 6))

temp = all_params.copy()

ranger = [
    np.linspace(-180,180, 10),
    np.around(np.linspace(np.amin(all_params[:,1]),np.amax(np.append(all_params[:,1], data_result["ECC"])), 10),5),
    np.linspace(-90,90, 10),
    np.linspace(-180,180, 10),
    np.linspace(-180,180, 10),
    np.around(np.linspace(np.amin(all_params[:,5]),np.amax(all_params[:,5]), 10),5),
]

# Normalize each feature independently between 0 and 1 for plotting
df_normalized = df.copy()
df_normalized_result = df_result.copy()
for i, column in enumerate(df.columns[1:]):
    df_normalized[column] = (df[column] - np.amin(ranger[i])) / (np.amax(ranger[i]) - np.amin(ranger[i]))
    df_normalized_result[column] = (df_result[column] - np.amin(ranger[i])) / (np.amax(ranger[i]) - np.amin(ranger[i]))

# print(df_normalized)

# Plot each row as a line on the plot
for i, row in df_normalized.iterrows():
    ax.plot(df.columns[1:], row[1:], color="orange", alpha=0.3)
    # print(row[1:])
for i, row in df_normalized_result.iterrows():
    ax.plot(df_result.columns[1:], row[1:], color="blue", alpha=1)


# Customizing the plot with different y-ticks for each feature

for i, column in enumerate(df.columns[1:]):
    # Calculate the position of the x-ticks
    x_position = i
    # Set the original feature values as y-ticks
    # ax.text(x_position, -0.1, f"{column}", ha='center', fontsize=12)  # Label the axis
    ax.set_yticks([])  # Remove default y-ticks
    
    # Create a new axis at the same position for the y-ticks of the feature
    ax_temp = ax.twinx()
    ax_temp.set_xlim([0,5])
    ax.set_ylim(0,1)
    ax_temp.set_ylim(0, 1)  # Normalize range (0 to 1)
    ax_temp.set_yticks(np.linspace(0, 1, 10))#len(df[column].unique())))  # Normalize y-ticks
    ax_temp.set_yticklabels(ranger[i])
    # ax_temp.set_yticklabels(df[column].unique())  # Set y-tick labels to actual feature values
    ax_temp.spines['top'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax_temp.spines['bottom'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    # Overlay axes so they share the same x-axis but have different y-ticks
    ax_temp.spines['left'].set_position(('axes', x_position / (len(df.columns)-2)))
    ax_temp.spines['left'].set_visible(True)
    ax_temp.spines['right'].set_visible(False)
    ax_temp.yaxis.set_ticks_position('left')


# Add the legend and title
ax.legend(loc='upper right')
plt.title('')

plt.savefig("parallel_coordinate_plot_results.png")


# print(np.shape(all_params))
# print(np.mean(all_params,axis=0))
