import torch


class Network(torch.nn.Module):

    input_neurons = 2
    hidden_neurons = 6
    output_neurons = 1

    def __init__(self):
        super().__init__()

        self.fc1 = torch.nn.Linear(Network.input_neurons, Network.hidden_neurons)
        self.fc2 = torch.nn.Linear(Network.hidden_neurons, Network.output_neurons)

    def forward(self, x):
        x = torch.nn.functional.sigmoid(self.fc1(x))
        x = torch.nn.functional.sigmoid(self.fc2(x))

        return x
