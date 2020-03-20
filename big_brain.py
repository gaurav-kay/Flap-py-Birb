import numpy as np


class Network:

    def __init__(self, layer_sizes):
        weight_shapes = [(a, b) for a, b in zip(layer_sizes[1:], layer_sizes[:-1])]
        self.weights = [np.random.standard_normal(s) for s in weight_shapes]
        self.biases = [np.zeros((s, 1)) for s in layer_sizes[1:]]

    def forward(self, a):
        for w, b in zip(self.weights, self.biases):
            a = self.sigmoid(np.matmul(w, a) + b)
        return a

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
