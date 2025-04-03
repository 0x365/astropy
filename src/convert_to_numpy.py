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





x_start_num = 0
x_end_num = 50
y_start_num = -50
y_end_num = 0

total_num = 200

multiplier = 2

sizer_x = abs(x_start_num-x_end_num)+1
sizer_y = abs(y_start_num-y_end_num)+1

grid = np.array(np.zeros((sizer_x,sizer_y,2500,8)))
grid[grid == 0] = np.nan

for i, xi in tqdm(enumerate(np.linspace(x_start_num,x_end_num,sizer_x)), total=sizer_x, desc="Generating grid"):
    for j, yi in enumerate(np.linspace(y_start_num,y_end_num,sizer_y)):
            x = round(multiplier*xi/total_num,2)
            y = round(multiplier*yi/total_num,2)
            if int(x) == x:
                x = int(x)
            if int(y) == y:
                y = int(y)
            try:
                dataset = np.array(csv_input("data/"+str(x)+"_"+str(y)+".csv"))
                grid[i,j] = dataset
            except:
                print(x,y, "missing")
                pass
    # if i%5 == 0 and i != 0:
    #     np.save("big_grid.npy", grid)
            
xv0 = str(round(multiplier*x_start_num/total_num,1))
xv1 = str(round(multiplier*x_end_num/total_num,1))
yv0 = str(round(multiplier*y_start_num/total_num,1))
yv1 = str(round(multiplier*y_end_num/total_num,1))
np.save("np/big_grid_"+xv0+"_"+xv1+"_"+yv0+"_"+yv1+".npy", grid)