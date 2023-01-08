from numpy.random import normal, uniform 
import numpy as np
from utils import *


class MultilayerPerceptron:
    def __init__(self, neurons:int, hidden_layers:int):
        """Initialise network, neurons is number of hidden neuorns on laysers,
        hidden_layers is number of hidden layers"""
        self.neurons = neurons
        self.hidden_layers = hidden_layers
        self.matrices = [None]*(self.hidden_layers+1) #store all matrices
        self.f_hidden = tanh #hidden activation function
        self.df_hidden = tanh_derivative
        self.f_out = linear #output activation function
        self.df_out = linear_derivative

        self.matrices[0] = self.make_matrix(neurons+1, 3) #input matrix

        for i in range(1, hidden_layers+1):
            n, m = neurons, neurons
            if i == 1:
                m += 1
            if i == hidden_layers:
                n = 1
            self.matrices[i] = self.make_matrix(n, m)
            
    def make_matrix(self, rows, cols) -> np.array:
        """returns a random uniform matrix having values from [-1, 1]"""
        mat = uniform(-1, 1, size=(rows, cols))
        return mat

    def compute_output(self, x, add_bias=True) -> np.array:
        """computes output from the network
        if x has already bias, set add bias
        to False, othervise it will be added"""

        if add_bias:
            x = np.concatenate((x, [1]))
        nets, h = [], [x] #here we store nets and outputs after activations funcions to be used in backpropagation

        for i, m in enumerate(self.matrices):
            net = m@(h[-1]) #compute net from output from previous layer

            if i == self.hidden_layers: #last layer output
                y = self.f_out(net)
            else:
                y = self.f_hidden(net) #hidden layer output

            nets.append(net)
            h.append(y)

        return nets, h

    def compute_error(self, output, target) -> np.array:
        """computes sqaure error between predicted output and expected target"""
        return (output-target)**2

    def train(self, inputs, outputs, num_epoch:int=100, alpha:float=.1) -> list[float]:
        """Train the network, returns error history"""
        errors = []
        n = len(outputs)

        for _ in range(num_epoch):
            E = 0 #error for this epoch
            perm = np.random.permutation(n) #random order of indices

            for i in perm:
                x = inputs[i] #input
                d = outputs[i] #target
                x_new = np.concatenate((x, [1])) #add bias
                net, h = self.compute_output(x_new, add_bias=False) #compute output

                y = h[-1] #output
                e = self.compute_error(y, d) #error
                E += e[0] #add to epoch error, index 0 so that it is float not array

                #BACKPROPAGATION
                #delta_out
                delta = np.asarray(d-y)
                self.matrices[-1] += alpha*np.outer(delta,h[-2]) #adjust last matrix

                M = self.hidden_layers #number of hidden layers

                for i in reversed(range(M)): #we adjust matrices from the last one
                    #delta_hid
                    delta = np.dot(self.matrices[i+1].T,delta)*self.df_hidden(net[i])

                    #W_hid
                    outer = np.outer(delta, h[i])
                    self.matrices[i] += alpha*outer

                    #after this delta_hid and W_hid become delta_out and W_out for the previous layer
             
            errors.append(E)
        return errors

    def evaluate(self, file_name: str) -> float or np.array:
        """Computes mean square error for data stored in 'file_name' file"""
        inputs, outputs = read_data(file_name) #split data to input and output

        n = len(outputs) #number of data
        err = 0
        for i in range(n):
            x = inputs[i]
            d = outputs[i]
            net, h = self.compute_output(x)
            y = h[-1]
            e = self.compute_error(y, d)
            err += e
        return err/n #average error

    def save_weights(self, file_name:str) -> None:
        """Saves all matrices into 'file_name' file"""

        with open(file_name, 'wb') as file:
            for matrix in self.matrices:
                np.save(file, matrix)

    def load_weights(self, file_name:str) -> None:
        """Loads matrices from 'file_name' file,
        raises AttrubuteError, if shape of matrices don\'t match"""
        mats = []
        with open(file_name, 'rb') as file:
            for i in range(len(self.matrices)):
                mat = np.load(file)
                if mat.shape != self.matrices[i].shape:
                    raise AttributeError("Matrices must be of the same shape as in the model")
                mats.append(mat)
        self.matrices = mats
    
if __name__ == "__main__":
    #Tu som si len testoval veci, tato cast nie je dolezita
    FILE_NAME = "mlp_train.txt"
    inputs, outputs = read_data(FILE_NAME)
    train_in, test_in, train_out, test_out = split_data(inputs, outputs, .8)
    alphas = list(np.arange(0.0001, 0.01, 0.0001))

    mlp = MultilayerPerceptron(40, 4)
    mlp.train(train_in, train_out, num_epoch=650, alpha=0.0071)

    e1 = 0
    n = len(train_out)
    for i, x in enumerate(train_in):
        d = train_out[i]
        net, h = mlp.compute_output(x)
        y = h[-1]
        e1 += mlp.compute_error(y, d)
    e1/=n
    e2 = 0
    m = len(test_out)
    for i, x in enumerate(test_in):
        d = test_out[i]
        net, h = mlp.compute_output(x)
        y = h[-1]
        e2 += mlp.compute_error(y, d)
    e2/=m
    print("total error", .3*e1+.7*e2)
    mlp.save_weights("pretrained.npy")



    





