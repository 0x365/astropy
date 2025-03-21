import numpy as np
import torch
from torch import nn
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from model import MyModel

dataset = np.load("data-np/-0.9_0.6.npy")
dataset = np.array(dataset, dtype=float)
dataset = dataset[:2000]

scaler = StandardScaler()
# dataset[:,0] = np.linspace(-1,1,3000)[:1000]
# dataset[:,0] = scaler.fit_transform(dataset[:,0])
dataset[:,1:] = scaler.fit_transform(dataset[:,1:])


print(dataset)
# dataset[1:] = dataset[1:]/np.amax(dataset[1:])

dataset_new = []
dataset_res = []
for i in range(len(dataset)):
    for j in range(i,len(dataset)):
        if i != j:
            dataset_new.append([*dataset[i,1:], dataset[j,0]-dataset[i,0]])
            dataset_res.append(dataset[j,1:])

dataset_new = np.array(dataset_new)
dataset_res = np.array(dataset_res)

data_x = torch.tensor(dataset_new.tolist(), dtype=torch.float32)
data_y = torch.tensor(dataset_res.tolist(), dtype=torch.float32)
# sklearn.MinMaxScalar

x_train, x_valid, y_train, y_valid = train_test_split(data_x, data_y, test_size=0.2, shuffle=True)

print('x_train:', x_train.shape)
print('y_train:', y_train.shape)
print('x_valid:', x_valid.shape)
print('y_valid:', y_valid.shape)

device = 'cuda' if torch.cuda.is_available() else 'cpu'


model = MyModel().to(device)


learning_rate = 0.001

loss_fn = nn.MSELoss()

optimizer =  torch.optim.Adam(params=model.parameters(), lr=learning_rate)


# Number of epochs
epochs = 1000

# Send data to the device
x_train, x_valid = x_train.to(device), x_valid.to(device)
y_train, y_valid = y_train.to(device), y_valid.to(device)

# Empty loss lists to track values
epoch_count, train_loss_values, valid_loss_values = [], [], []

def accuracy_fn(y_true, y_pred):
    # Calculate the mean squared error between predictions and true values
    mse = torch.mean((y_true - y_pred) ** 2).item()
    return mse

# Loop through the data
last_loss = np.inf
for epoch in range(epochs):

    # Put the model in training mode
    model.train()

    y_pred = model(x_train) # forward pass to get predictions; squeeze the logits into the same shape as the labels
    # print(y_logits)
    # y_pred = (y_logits) # convert logits into prediction probabilities

    loss = loss_fn(y_pred, y_train) # compute the loss   
    acc = accuracy_fn(y_train, y_pred)

    optimizer.zero_grad() # reset the gradients so they don't accumulate each iteration
    loss.backward() # backward pass: backpropagate the prediction loss
    optimizer.step() # gradient descent: adjust the parameters by the gradients collected in the backward pass
    
    # Put the model in evaluation mode
    model.eval() 

    with torch.inference_mode():
        valid_pred = model(x_valid) 

        valid_loss = loss_fn(valid_pred, y_valid)
        valid_acc = accuracy_fn(y_valid, valid_pred)    
    
    # Print progress a total of 20 times
    if epoch % int(epochs / 50) == 0 and epoch != 0:
        print(f'Epoch: {epoch:4.0f} | Train Loss: {loss:.5f}, MSE: {acc:.2f}% | Validation Loss: {valid_loss:.5f}, MSE: {valid_acc:.2f}%')

        epoch_count.append(epoch)
        train_loss_values.append(loss.detach().numpy())
        valid_loss_values.append(valid_loss.detach().numpy())

        if valid_loss < last_loss:
            torch.save(model, 'test.pth')
            last_loss = valid_loss

        plt.plot(train_loss_values)
        plt.plot(valid_loss_values)
        plt.savefig("loss.png")
        plt.clf()

if valid_loss < last_loss:
    torch.save(model, 'test.pth')
    last_loss = valid_loss