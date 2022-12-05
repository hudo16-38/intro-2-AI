from generate_data import Data
from numpy import array
import numpy as np

def S(x_data, y_data):

    n = len(x_data)

    x = array(x_data)
    y = array(y_data)
    
    ones = np.ones(n)
    
    second_sum = (x*(y@ones))@ones


    return x@y - second_sum/n
    


def linear_regression(data):

    x, y = [], []
    
    for xi, yi in data:
        x.append(xi); y.append(yi)

    x = array(x)
    y = array(y)
    n = len(x)
    x_squared = x**2

    ones = np.ones(n)

    second_sum = (x*(y@ones))@ones
    denominator = n*(x_squared@ones) - (x@ones)**2

    a = (n*x@y - second_sum)/denominator
    b = (y@ones - a*(x@ones))/n

    return a, b


def quadratic_regression(data):
    x, y = [], []
    
    for xi, yi in data:
        x.append(xi); y.append(yi)

    
    x = array(x)
    y = array(y)
    n = len(x)

    x_squared = x**2
    ones = np.ones(n)


    a = (S(x_squared, y)*S(x, x) - S(x, y)*S(x, x_squared))/(S(x, x)*S(x_squared, x_squared) - S(x, x_squared)**2) 
    b = (S(x, y)*S(x_squared, x_squared) - S(x_squared, y)*S(x, x_squared)) / (S(x,x)*S(x_squared, x_squared) - S(x, x_squared)**2)
    c = (y@ones - b*(x@ones) - a*(x_squared@ones))/n

    return a, b, c


if __name__ == "__main__":

    # generate linear data, calculate both linear and quadratic fit, plot along with regression error and test data
    lin = Data('linear')
    line_a, line_b = linear_regression(lin.points)
    parabola_a, parabola_b, parabola_c = quadratic_regression(lin.points)
    lin.plot_result(line_a, line_b, parabola_a, parabola_b, parabola_c)

    # generate quadratic data, calculate both linear and quadratic fit, plot along with regression error and test data
    quad = Data('quadratic')
    line_a, line_b = linear_regression(quad.points)
    parabola_a, parabola_b, parabola_c = quadratic_regression(quad.points)
    quad.plot_result(line_a, line_b, parabola_a, parabola_b, parabola_c)

    
