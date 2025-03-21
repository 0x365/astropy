import numpy as np
from tqdm import tqdm
import csv
import datasets
import glob


data_location = "data_big/raw_orbits/"


counters = np.linspace(-1,1, 200)



period_np = np.load("data_big/periods.npy")

stability_np = np.load("data_big/orbit_deviation_std.npy")

collisions_np = np.array(np.load("data_big/collisions.npy"), dtype="bool")

names = []
v1 = []
v2 = []
period = []
stability = []
collisions = []
to_file = []

for ii in tqdm(range(200)):

    for jj in range(200):

        names.append(str(ii)+"_"+str(jj))
        v1.append(counters[ii])
        v2.append(counters[jj])
        period.append(period_np[ii,jj])
        stability.append(stability_np[ii,jj])
        collisions.append(collisions_np[ii,jj])

dataset = datasets.Dataset.from_dict({
        "id": names,
        "v1": v1,
        "v2": v2,
        "period": period,
        "stability": stability,
        "collisional": collisions
    }, 
    features=datasets.Features({
        "id": datasets.Value("string"),
        "v1": datasets.Value("float32"),
        "v2": datasets.Value("float32"),
        "period": datasets.Value("float32"),
        "stability": datasets.Value("float32"),
        "collisional": datasets.Value("bool")
    }))

print(dataset)
# print((np.array(dataset[0]["r1x"])))

dataset.push_to_hub("0x365/stable-orbits-map", private=True)