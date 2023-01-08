import numpy as np
import matplotlib.pyplot as plt
import os


def press_to_quit(e):
    if e.key in {'q', 'escape'}:
        os._exit(0) # unclean exit, but exit() or sys.exit() won't work
    if e.key in {' ', 'enter'}:
        plt.close() # skip blocking figures


def show_history(history, block=True):
    fig = plt.figure(num='Training history')
    fig.canvas.mpl_connect('key_press_event', press_to_quit)

    plt.title('Loss per epoch')
    plt.plot(history.history['loss'], '-b', label='training loss')
    try:
        plt.plot(history.history['val_loss'], '-r', label='validation loss')
    except KeyError:
        pass
    plt.grid(True)
    plt.legend(loc='best')
    plt.xlim(left=-1); plt.ylim(bottom=-0.01)

    plt.tight_layout()
    plt.show(block=block)


def show_data(X, y, predicted=None, s=30, block=True):
    plt.figure(num='Data', figsize=(9,9)).canvas.mpl_connect('key_press_event', press_to_quit)
    
    if predicted is not None:
        predicted = np.asarray(predicted).flatten()
        plt.subplot(2,1,2)
        plt.title('Predicted')
        plt.scatter(X[:, 0], X[:, 1],
                    c=predicted, cmap='coolwarm',
                    s=10 + s * np.maximum(0, predicted))
        
        plt.subplot(2,1,1)
        plt.title('Original')
    y = np.asarray(predicted).flatten()
    plt.scatter(X[:, 0], X[:, 1],
                c=y, cmap='coolwarm',
                s=10 + s * np.maximum(0, y))
    plt.tight_layout()
    
    plt.show(block=block)

##########################################################
#my help functions
def sigmoid(x):
    return (1 + np.exp(-x))**(-1)

def sech(x):
    return 1/np.cosh(x)

def tanh(x):
    return np.tanh(x)

def sigmoid_derivative(x):
    y = sigmoid(x)
    return y*(1-y)

def tanh_derivative(x):
    return 1 - tanh(x)**2

def relu(x):
    return np.array([max(0, i) for i in x])

def relu_derivative(x):
    lst = [0 if i <= 0 else 1 for i in x]
    return np.array(lst)

def linear(x):
    return x + 1

def linear_derivative(x):
    return 1


def split_data(inputs, outputs, prob):
    """This function splits data approximately to the given ratio.
    E.g. if prob is 0.8, data is split in ratio 80:20 (training part:testing part),
    returns 4 arrays: training input, testing input, training output, testing output"""
    n = len(outputs)

    probs = np.random.rand(n) #generate random value for each data from standart uniform distribution
    mask = probs <= prob #if value is <= prob, we put it to testig part

    #split inputs
    train_input = inputs[mask]
    test_input = inputs[~mask]

    #split outputs
    train_output = outputs[mask]
    test_output = outputs[~mask]

    return train_input, test_input, train_output, test_output


def read_data(file_name:str):
    """loads data from 'file_name' file,
    splits them into input and ouput parts and returns them"""
    data = np.loadtxt(file_name)
    inputs = data[:, :2]
    outputs = data[:, -1]

    return inputs, outputs
#######################################################################



