import sys
import numpy as np
import random

from utils import *


class SingleLayerPerceptron:

    def __init__(self, input_dim, output_dim):
        # Initialize perceptron and data.
        # List self.data = [(input1, target1), (input2, target2), ...]
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.initialize_weights()

    def compute_accuracy(self, inputs, targets):
        # Computes *classification* accuracy - percentage of correctly categorized inputs
        return np.mean([d.argmax() == self.compute_output(self.add_bias(x)).argmax() for (x, d) in zip(inputs.T, targets.T)])


    def add_bias(self, x):
        # Add bias to input vector x.
        return np.concatenate((x, [1]))

    def initialize_weights(self):
        # Sets all weights to (Gaussian) random values
        ### YOUR CODE GOES HERE: replace "0, 0" with correct size of weights matrix (no. of rows and columns) ###
        self.W = np.random.randn(self.output_dim, self.input_dim + 1)

    def sigmoid(self, x):
        return 1/(1 + np.exp(-x))

    def compute_output(self, x):
        # Computes output (vector y) of the neural network for given input vector x (including bias).
        ### YOUR CODE GOES HERE ###
        return self.sigmoid(self.W @ x) 

    def compute_error(self, d, y):
        # Computes square error of output y against desired output d.
        ### YOUR CODE GOES HERE ###
        return np.linalg.norm(d-y)



    def train(self, inputs, targets, num_epochs, alpha=0.1):
        # Trains the neural network, iterating num_epochs times.
        # After each epoch, per-epoch regression error (E) and classification
        # accuracy are appended into history, that is return for further plotting.
        count = inputs.shape[1] # number of input-target pairs
        err_history = []
        accuracy_history = []
        

        for ep in range(num_epochs):
            E = 0
            for i in np.random.permutation(count):
                x = self.add_bias(inputs[:, i])
                d = targets[:, i]
                ### YOUR CODE GOES HERE ###
                y = self.compute_output(x)
                e = self.compute_error(d, y)
                E += e
                delta = (d-y)*(y*(1-y))
                self.W += alpha*np.outer(delta, x)

            err_history.append(E)
            acc = self.compute_accuracy(inputs, targets)
            accuracy_history.append(acc)
            if (ep+1) % 10 == 0: print('Epoch {:3d}, E = {:6.3f}, accuracy = {:4.1%}'.format(ep+1, E, acc))
        return (err_history, accuracy_history)


if __name__ == "__main__":
    ## Load data and initialize
    #file_path = 'odd_even.in' # Easier: distinguish between odd and even numbers
    file_path = 'numbers.in' # Harder: recognize digits
    to_plot = False

    inputs, targets = prepare_data(file_path)
    input_dim = inputs.shape[0]
    output_dim = targets.shape[0]

    model = SingleLayerPerceptron(input_dim, output_dim)

    ## Train the neural network
    training_hisotry = model.train(inputs, targets, num_epochs=200, alpha=0.05) # feel free to add epochs

    ## Print results or weights
    if to_plot:
        plot_original_inputs(model=model)
        plot_noisy_inputs(model=model, count=18)
        plot_errors(training_hisotry)
