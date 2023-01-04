import numpy as np
from multilayer_perceptron import MultilayerPerceptron
from utils import *

def make_network(file_name:str="mlp_train.txt"):
    inputs, outputs = read_data(file_name)
    mlp = MultilayerPerceptron(8, 1)
    mlp.train(inputs, outputs)
    return mlp


def evaluate(file_name:str) -> float:
    global network
    inputs, outputs = read_data(file_name)
    error = 0
    
    n = len(outputs)
    for i in range(n):
        x = inputs[:, i]
        d = outputs[i]

        y = network.compute_output(x)
        e = network.compute_error(y, d)
        error += e

    return error/n

if __name__ == "__main__":
    network = make_network()