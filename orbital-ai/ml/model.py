import torch
from torch import nn

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(13, 64)
        self.linear2 = nn.Linear(64, 128)
        self.linear3 = nn.Linear(128, 128)
        self.linear4 = nn.Linear(128, 128)
        self.linear5 = nn.Linear(128, 96)
        self.linear6 = nn.Linear(96, 32)
        self.linear7 = nn.Linear(32, 12)
        
        # Activation functions
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()
        self.logsigmoid = nn.LogSigmoid()

    def forward(self, x):
        # Apply linear layers with activations
        x = self.tanh(self.linear1(x))            # Tanh after first linear layer
        x = self.logsigmoid(self.linear2(x))      # LogSigmoid after second layer
        x = self.relu(self.linear3(x))            # ReLU after third layer
        x = self.relu(self.linear4(x))            # ReLU after fourth layer
        x = self.tanh(self.linear5(x))            # Tanh after fifth layer
        x = self.logsigmoid(self.linear6(x))      # LogSigmoid after sixth layer
        x = self.linear7(x)                       # No activation in the last layer
        
        return x