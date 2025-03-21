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
# collisions_np2 = np.zeros((200,200), dtype="str")
# collisions_np2[collisions_np == 0] = "non-collisional"
# collisions_np2[collisions_np == 1] = "collisional"

i_range = range(178,200)

for ii in tqdm(i_range):

    names = []
    v1 = []
    v2 = []
    period = []
    stability = []
    collisions = []
    to_file = []

    for jj in range(200):

        names.append(str(ii)+"_"+str(jj))
        v1.append(counters[ii])
        v2.append(counters[jj])
        period.append(period_np[ii,jj])
        stability.append(stability_np[ii,jj])
        collisions.append(collisions_np[ii,jj])

        
        orbit_data = np.load(data_location+str(ii)+"_"+str(jj)+".npz")

        comb = []
        
        # comb.append([orbit_data["t"]])
        # extra.append([orbit_data["t"]])
        for i in orbit_data["y"]:
            if len(i) != 50000:
                comb.append([[*i, *[np.nan]*(50000-len(i))]])
            else:
                comb.append([i])

        
        to_file.append(comb)

    to_file = np.array(to_file, dtype="float32")

    print(np.shape(to_file))

    dataset = datasets.Dataset.from_dict({
        "id": names,
        "v1": v1,
        "v2": v2,
        "period": period,
        "stability": stability,
        "collisional": collisions,
        "r1x": to_file[:,0,:,:],
        "r1y": to_file[:,1,:,:],
        "r2x": to_file[:,2,:,:],
        "r2y": to_file[:,3,:,:],
        "r3x": to_file[:,4,:,:],
        "r3y": to_file[:,5,:,:],
        "v1x": to_file[:,6,:,:],
        "v1y": to_file[:,7,:,:],
        "v2x": to_file[:,8,:,:],
        "v2y": to_file[:,9,:,:],
        "v3x": to_file[:,10,:,:],
        "v3y": to_file[:,11,:,:]
        }, 
        features=datasets.Features({
            "id": datasets.Value("string"),
            "v1": datasets.Value("float32"),
            "v2": datasets.Value("float32"),
            "period": datasets.Value("float32"),
            "stability": datasets.Value("float32"),
            "collisional": datasets.Value("bool"),
            "r1x": datasets.Array2D(shape=(1,50000), dtype='float32'),
            "r1y": datasets.Array2D(shape=(1,50000), dtype='float32'),
            "r2x": datasets.Array2D(shape=(1,50000), dtype='float32'),
            "r2y": datasets.Array2D(shape=(1,50000), dtype='float32'),
            "r3x": datasets.Array2D(shape=(1,50000), dtype='float32'),
            "r3y": datasets.Array2D(shape=(1,50000), dtype='float32'),
            "v1x": datasets.Array2D(shape=(1,50000), dtype='float32'),
            "v1y": datasets.Array2D(shape=(1,50000), dtype='float32'),
            "v2x": datasets.Array2D(shape=(1,50000), dtype='float32'),
            "v2y": datasets.Array2D(shape=(1,50000), dtype='float32'),
            "v3x": datasets.Array2D(shape=(1,50000), dtype='float32'),
            "v3y": datasets.Array2D(shape=(1,50000), dtype='float32')
        }))

    print(dataset)
    # print((np.array(dataset[0]["r1x"])))

    dataset.push_to_hub("0x365/stable-orbits", private=True, split=f"part_{ii:05d}")
