from numpy.random import normal 
import numpy as np
from utils import *
from itertools import permutations


class MLP:

    def __init__(self, input_dim:int, output_dim:int, hidden_neurons: int):
        self.input_dim, self.output_dim, self.hidden_neurons = input_dim, output_dim, hidden_neurons 
        self.hidden_neurons = hidden_neurons

        self.input_matrix = normal(size=(self.hidden_neurons, self.input_dim+1))
        self.hidden_matrix = normal(size=(self.output_dim, self.hidden_neurons))

        self.f1 = self.f2 = None #functions to be used

    def compute_output(self, x: np.ndarray):
        if self.f1 is None or self.f2 is None:
            raise Exception("Network hasn\'t been trained yet")

        x = np.concatenate((x, [1]))

        net_hid = self.input_matrix@x

        y1 = self.f1(net_hid)

        net_out = self.hidden_matrix@y1

        y2 = self.f2(net_out)
      
        return net_hid, y1, net_out, y2 #pri backpropagation

    def compute_error(self, output, target):
        return abs(output - target)

    def train(self, inputs, targets, num_of_epochs:int=50, functions=(sigmoid, sigmoid), alpha:float=.1):
        self.f1, self.f2 = functions

        if self.f1 == sigmoid:
            self.df1 = sigmoid_derivative
        elif self.f1 == tanh:
            self.df1 = tanh_derivative
        elif self.f1 == linear:
            self.df1 = linear_derivative
        else:
            self.df1 = relu_derivative

        if self.f2 == sigmoid:
            self.df2 = sigmoid_derivative
        elif self.f2 == tanh:
            self.df2 = tanh_derivative
        elif self.f2 == linear:
            self.df2 = linear_derivative
        else:
            self.df2 = relu_derivative

        n = inputs.shape[0] #num of inputs
        errors = []

        for epoch in range(num_of_epochs):
            E = 0

            perm = np.random.permutation(n)
            for index in perm:
                input = inputs[index]
                d = targets[index]
                net_hid, y_hid, net_out, y = self.compute_output(input) 
                err = self.compute_error(y, d)
                E += err


                #backpropagation
                delta_out = (d-y)*self.df2(net_out) 
                delta_hid = (self.hidden_matrix*delta_out)*self.df1(net_hid) #hidden matrix je druha matica

                self.hidden_matrix += alpha*np.outer(delta_out, y_hid)
                self.input_matrix += alpha*np.outer(delta_hid, np.concatenate((input, [1])))

            errors.append(E)

        return errors


def compute(train_in, train_out, test_in, test_out, functions):
    mlp = MLP(2, 1, 12)
    mlp.train(train_in, train_out, functions=functions)

    train_err = 0
    n = len(train_out)
    for i, x in enumerate(train_in):
        d = train_out[i]
        net_hid, y1, net_ouit, y2 = mlp.compute_output(x)
        train_err += mlp.compute_error(y2, d)
    train_err/=n
    #print(f"{train_err=}")

    test_err = 0
    m = len(test_out)
    for i, x in enumerate(test_in):
        d = test_out[i]
        net_hid, y1, net_ouit, y2 = mlp.compute_output(x)
        test_err += mlp.compute_error(y2, d)
    test_err/=n
    #print(f"{test_err=}")
    return train_err, test_err





if __name__ == "__main__":
    ALL = (sigmoid, relu, tanh, linear)
    FUNCTIONS = permutations(ALL, 2)


    FILE_NAME = "mlp_train.txt"
    P = 0.8

    input, output = read_data(FILE_NAME)
    #print(f"MIN = {min(output)}, MAX = {max(output)}")
    train_in, test_in, train_out, test_out = split_data(input, output, P)
 
    for funs in FUNCTIONS:
        train_err, test_err = compute(train_in, train_out, test_in, test_out, funs)
        total_err = .3*train_err + .7*test_err
        f1, f2 = funs[0].__name__, funs[1].__name__
        print(f"Functions are: {f1} and {f2}")
        print(f"{train_err=}")
        print(f"{test_err=}")
        print(f"{total_err=}")
        print("*"*25)
        print()
    
    

    