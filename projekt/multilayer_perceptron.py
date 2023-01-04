from numpy.random import normal 
import numpy as np
from utils import *


class MultilayerPerceptron:

    def __init__(self, neurons:int, hidden_layers:int):
        self.neurons = neurons
        self.hidden_layers = hidden_layers
        self.matrices = [None]*(self.hidden_layers+1)
        self.f = None

        self.matrices[0] = self.make_matrix(neurons+1, 3) #input matrix

        for i in range(1, hidden_layers+1):
            n, m = neurons, neurons
            if i == 1:
                m+=1
            if i == hidden_layers:
                n = 1

            self.matrices[i] = self.make_matrix(n, m)
            

    def make_matrix(self, rows, cols):
        return normal(size=(rows, cols), scale=1/3)

    def compute_output(self, x, add_bias=True):
        if self.f is None:
            raise ValueError("Network hasn\'n been trained yet")

        if add_bias:
            x = np.concatenate((x, [1]))
        nets, y = [], []

        for i, m in enumerate(self.matrices):
            net = m@x

            if i == self.hidden_layers:
                h = linear(net)
            else:
                h = self.f(net)

            nets.append(net)
            y.append(h)

        return nets, y

    def compute_error(self, output, target):
        return (input-target)**2

    def train(self, inputs, outputs):
        pass

    def evaluate(self, file_name: str) -> float:
        inputs, outputs = read_data(file_name)

        n = len(outputs)
        err = 0
        for i in range(n):
            x = inputs[:, i]
            d = outputs[i]
            y = self.compute_output(x)
            e = self.compute_error(y, d)
            err += e
        return err/n



if __name__ == "__main__":
    mlp = MultilayerPerceptron(8, 1)
    #res = mlp.compute_output(np.array([1, 1]))

    print(normal(size=(2,3)))

