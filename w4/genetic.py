from audioop import reverse
from pickle import NONE
import numpy as np
import random
from numpy.random import normal

def alternative_generator(prob):
    val = random.random()

    return int(val <= prob)

from problems import *

class GenAlgProblem:

    def __init__(self, population_size=12, n_crossover=3, mutation_prob=0.05):
        # Initialize the population - create population of 'size' individuals,
        # each individual is a bit string of length 'word_len'.
        self.population_size = population_size
        self.n_crossover = 3
        self.mutation_prob = 0.05
        self.population = [self.generate_individual() for _ in range(self.population_size)]

    def generate_individual(self):
        # Generate random individual.
        # To be implemented in subclasses
        raise NotImplementedError

    def show_individual(self, x):
        # Show the given individual x, either to console or graphically.
        # To be implemented in subclasses
        raise NotImplementedError

    def show_population(self, title='Population:', limit=None, **kwargs):
        # Show whole population.
        # To be implemented in subclasses
        raise NotImplementedError


    def fitness(self, x):
        # Returns fitness of a given individual.
        # To be implemented in subclasses
        raise NotImplementedError

    def crossover(self, x, y, k):
        # Take two parents (x and y) and make two children by applying k-point
        # crossover. Positions for crossover are chosen randomly.
        ### YOUR CODE GOES HERE ###
        n = len(x)
        x_new, y_new = list(x), list(y)

        points_to_cross = set()
        possible_cross = range(1, n-1)

        while len(points_to_cross) < k:
            points_to_cross.add( np.random.choice(possible_cross) )

        points_to_cross = sorted(points_to_cross)

        #zamienam na striedacku
        previous = 0
        for i, cross in enumerate(points_to_cross):
            
            if i%2 == 0:
                x_new[previous:cross], y_new[previous:cross] = x[previous:cross], y[previous:cross]
            else:
                x_new[previous:cross], y_new[previous:cross] = y[previous:cross], x[previous:cross]

            previous = cross

        if k%2 == 1:
            x_new[cross:], y_new[cross:] = y[cross:], x[cross:]

        return (x_new, y_new)

    def boolean_mutation(self, x, prob):
        # Elements of x are 0 or 1. Mutate (i.e. change) each element of x with given probability.
        ### YOUR CODE GOES HERE ###
        for i in range(len(x)):
            if alternative_generator(prob):
                x[i] = int(not x[i])
        return x

    def number_mutation(self, x, prob):
        # Elements of x are real numbers [0.0 .. 1.0]. Mutate (i.e. add/subtract random number)
        # each number in x with given probability.
        ### YOUR CODE GOES HERE ###
        for i in range(len(x)):
            if alternative_generator(prob):
                value = normal(0, 1/6)
                x[i] += value
        return x

    def mutation(self, x, prob):
        # To be specified in subclasses, uses boolean_mutation or number_mutation functions
        raise NotImplementedError

    def solve(self, max_generations, goal_fitness=1):
        # Implementation of genetic algorithm. Produce generations until some
        # individual`s fitness reaches goal_fitness, or you exceed total number
        # of max_generations generations. Return best found individual.
        ### YOUR CODE GOES HERE ###
        n = len(self.population)


        for _ in range(max_generations):
            self.population.sort(reverse=True, key=self.fitness)

            if self.fitness(self.population[0]) >= goal_fitness:
                return self.population[0]

            best_ones = list(self.population[:n//2])
            random.shuffle(best_ones)

            #parim po 2 susednych 
            for x in range(0, n//2, 2):
                y = x + 1

                new_x, new_y = self.crossover(best_ones[x], best_ones[y], k=self.n_crossover)
                new_x = self.mutation(new_x, self.mutation_prob)
                new_y = self.mutation(new_y, self.mutation_prob)
                best_ones.append(new_x)
                best_ones.append(new_y)

            self.population = best_ones

        return sorted(self.population, reverse=True, key=self.fitness)[0] #the best individual found

            




if __name__ == "__main__":
    ## Choose problem
    #ga = OnesString()
    #ga = Smiley()
    ga = Painting('painting.jpg', population_size=32, mutation_prob=0.25)
    #ga.show_population('Initial population', limit=None)

    ## You can play with parameters
    # ga.n_crossover = 5
    # ga.mutation_prob = 0.1

    ## Solve to find optimal individual
    best = ga.solve(100) # you can also play with max. generations
    ga.show_population('Final population', limit=None)
    ga.show_individual(best, 'Best individual')


    ## Test your crossover function
    #ga = OnesString()
    #children = ga.crossover([0]*32, [1]*32, k=3)
    #print('{}\n{}'.format(*children))
