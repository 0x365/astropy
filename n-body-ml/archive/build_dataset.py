import numpy as np
from tqdm import tqdm

total_num = 5

valid_rows = []
for i in tqdm(range(-total_num, total_num)):
    for j in range(-total_num, total_num):
        v1 = 1.5 * i / total_num
        v2 = 1.5 * j / total_num
        try:
            data_in = np.load("data-np/"+str(v1)+"_"+str(v2)+".npy")
        except:
            continue
        
        for k in range(data_in.shape[0] - 500):  # Only iterate where the 500th row exists
            row_1 = data_in[i]
            row_500th_after = data_in[i + 500]
            valid_rows.append([row_1, row_500th_after])

print(np.shape(valid_rows))



np.save("test-data/500s_dataset", np.array(valid_rows))