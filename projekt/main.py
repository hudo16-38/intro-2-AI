import numpy as np
from multilayer_perceptron import MultilayerPerceptron
from utils import *

def make_network(file_name:str="mlp_train.txt") -> MultilayerPerceptron:
    inputs, outputs = read_data(file_name)
    mlp = MultilayerPerceptron(40, 4)
    mlp.train(inputs, outputs, num_epoch=450, alpha=0.0081)
    return mlp

def load_pretrained(file_name:str) -> MultilayerPerceptron:
    mlp = MultilayerPerceptron(40, 4)
    mlp.load_weights(file_name)
    return mlp


if __name__ == "__main__":
    TRAIN_FILE = "mlp_train.txt"
    TEST_FILE = None #put name of the test file here
    LOAD_PRETRAINED = False
    assert(TEST_FILE is not None, "You forgot to specify the test file")

    network = make_network(TRAIN_FILE)
    train_error = network.evaluate(TRAIN_FILE)

    test_error = network.evaluate(TEST_FILE)
    total_error = 0.3*train_error + 0.7*test_error
    print(f"{total_error=}")

    if LOAD_PRETRAINED:
        network = load_pretrained("pretrained.npy")
        train_error = network.evaluate(TRAIN_FILE)
    
        test_error = network.evaluate(TEST_FILE)
        total_error = 0.3*train_error + 0.7*test_error
        print("Pretrained error:", total_error)
        
        
