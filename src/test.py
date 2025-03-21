from scipy.spatial.distance import directed_hausdorff
from scipy.spatial import procrustes
import numpy as np
import cv2
import csv
from tqdm import tqdm
import matplotlib.pyplot as plt

def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)   
    f.close()
    return output


def hu_moments_similarity(line1, line2):
    # Convert to contour format
    contour1 = line1.reshape((-1, 1, 2))
    contour2 = line2.reshape((-1, 1, 2))

    # Compute Hu Moments
    hu1 = cv2.HuMoments(cv2.moments(contour1)).flatten()
    hu2 = cv2.HuMoments(cv2.moments(contour2)).flatten()

    # Compute Euclidean distance between moments
    return np.linalg.norm(hu1 - hu2)

sizer = 201

grid = np.zeros((sizer,sizer,3000,8))


for i, xi in tqdm(enumerate(np.linspace(-2,2,sizer)), total=sizer, desc="Generating grid"):
    for j, yi in enumerate(np.linspace(-2,2,sizer)):
        x = round(xi,2)
        y = round(yi,2)
        if int(x) == x:
            x = int(x)
        if int(y) == y:
            y = int(y)
        try:
            dataset = np.array(csv_input("data/"+str(x)+"_"+str(y)+".csv"))
            grid[i,j] = dataset
        except:
            pass
            

np.save("big_grid.npy", grid)

plt.imshow(np.log10(np.nanmean(grid, axis=(2,3))))
plt.colorbar()
plt.savefig("test.png")




# print(np.shape(line1))
# similarity = hu_moments_similarity(line1, line2)
# print(f"Hu Moments Similarity: {similarity}")