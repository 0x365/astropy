import torch
from torch import nn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

from model import MyModel

dataset = np.load("data-np/-0.9_0.6.npy")
dataset = np.array(dataset, dtype=float)
dataset = dataset[:3000]
dataset_saver = dataset.copy()

scaler = StandardScaler()
dataset[:2000,1:] = scaler.fit_transform(dataset[:2000,1:])
dataset[2000:,1:] = scaler.transform(dataset[2000:,1:])

dataset_new = []
dataset_res = []
for i in range(len(dataset)):
    for j in range(i,len(dataset)):
        if i != j:
            dataset_new.append([*dataset[i,1:], dataset[j,0]-dataset[i,0]])
            dataset_res.append(dataset[j,1:])

dataset_new = np.array(dataset_new)
dataset_res = np.array(dataset_res)


# Load the entire model (architecture + state)
model = torch.load('test.pth')

# Set the model to evaluation mode before inference
model.eval()

device = 'cuda' if torch.cuda.is_available() else 'cpu'


all_pred = []
with torch.inference_mode():
    for i in range(len(dataset_saver)):
        data0 = dataset_new[0]
        data0[-1] = i
        example_input = torch.tensor(data0, dtype=torch.float32)
        example_input = example_input.to(device)
        prediction = model(example_input)
        predicted_values = prediction.cpu().numpy()
        all_pred.append(predicted_values)

all_pred = np.array(all_pred)
all_pred = scaler.inverse_transform(all_pred)


print(np.shape(all_pred))
stopper = -1

plt.figure(figsize=(10,10))

plt.plot(dataset_saver[1:,1], dataset_saver[1:,2], c="black")
plt.plot(dataset_saver[1:,3], dataset_saver[1:,4], c="black")
plt.plot(dataset_saver[1:,5], dataset_saver[1:,6], c="black")

plt.plot(all_pred[:stopper,0], all_pred[:stopper,1], c="red")
plt.plot(all_pred[:stopper,2], all_pred[:stopper,3], c="red")
plt.plot(all_pred[:stopper,4], all_pred[:stopper,5], c="red")


for i in range(5):
    print("Pred:", all_pred[i,:6])
    print("Real:", dataset_saver[1+i,1:7])
    print()

plt.gca().axis('equal')

plt.savefig("test.png",dpi=500)