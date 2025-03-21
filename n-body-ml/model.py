import torch
from torch import nn

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(12, 64)
        self.linear2 = nn.Linear(64, 128)
        self.linear3 = nn.Linear(128, 128)
        self.linear4 = nn.Linear(128, 128)
        self.linear41 = nn.Linear(128, 128)
        self.linear42 = nn.Linear(128, 128)
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
        x = self.linear41(x)
        x = self.linear42(x)
        x = self.tanh(self.linear5(x))            # Tanh after fifth layer
        x = self.logsigmoid(self.linear6(x))      # LogSigmoid after sixth layer
        x = self.linear7(x)                       # No activation in the last layer
        
        return x
        

class LSTMModel(nn.Module):
    def __init__(self):
        super(LSTMModel, self).__init__()
        
        # Define the hidden size for the LSTM
        self.hidden_size = 10
        
        # Linear layers
        self.linear1 = nn.Linear(12, 32)
        self.linear2 = nn.Linear(32, 64)
        
        # Double stacked LSTM layer (num_layers=2)
        self.lstm = nn.LSTM(input_size=64, hidden_size=self.hidden_size, num_layers=2, batch_first=True)
        
        # Additional linear layers after LSTM
        self.linear3 = nn.Linear(self.hidden_size, 64)
        self.linear4 = nn.Linear(64, 12)
        
        # Activation functions
        self.tanh = nn.Tanh()
        self.logsigmoid = nn.LogSigmoid()
        self.relu = nn.ReLU()

    def forward(self, x):
        # Pass through first linear layer with Tanh activation
        x = self.tanh(self.linear1(x))
        
        # Pass through second linear layer with LogSigmoid activation
        x = self.logsigmoid(self.linear2(x))
        
        # Prepare input for LSTM (batch size should be 1 if input is a single example)
        x = x.unsqueeze(0).contiguous()  # Add a batch dimension if needed, e.g., (1, sequence_length, features)
        
        # Initialize hidden and cell states for the LSTM (zeros)
        # Adjust for double-stacked LSTM: num_layers=2
        h_0 = torch.zeros(2, x.size(0), self.hidden_size).to(x.device)  # (num_layers, batch_size, hidden_size)
        c_0 = torch.zeros(2, x.size(0), self.hidden_size).to(x.device)
        
        # Pass through LSTM layer
        lstm_out, _ = self.lstm(x, (h_0, c_0))
        
        # Take the last output of the LSTM (since batch_first=True)
        lstm_out = lstm_out[:, -1, :]
        
        # Pass through third linear layer with ReLU activation
        x = self.relu(self.linear3(lstm_out))
        
        # Pass through fourth linear layer
        x = self.linear4(x)  # No activation at the final layer
        
        return x