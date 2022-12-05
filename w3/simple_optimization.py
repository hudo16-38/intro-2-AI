import math
import random
import os
import atexit
from time import sleep
import numpy as np
import matplotlib
matplotlib.use('TkAgg') # fixme if plotting doesn`t work (try 'Qt5Agg' or 'Qt4Agg')
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


def finish():
    plt.show(block=True) # Woraround to prevent plots from closing

atexit.register(finish)


class OptimizeMax(ABC):

    def hillclimb(self, max_steps=100, plot=True):

        current_state = self.random_state()

        for _ in range(max_steps):

            best_neighbor = None
            
            for x in self.neighbors(current_state):

                if best_neighbor is None or self.fitness(x) > self.fitness(best_neighbor):
                    best_neighbor = x
            
            if plot:
                self.plot(current_state, self.fitness(current_state), title='Hill climb')

            if self.fitness(current_state) > self.fitness(best_neighbor):
                return current_state

            current_state = best_neighbor

        return current_state



    @abstractmethod
    def fitness(self, x):
        pass
    
    @abstractmethod
    def neighbors(self, x):
        pass

    @abstractmethod
    def random_state(self):
        pass

    def plot(self, x, fx):
        pass



class MysteryFunction(OptimizeMax):
    # An optimization problem in which we are trying to find value for x such
    # that function sin(x)/x is maximized.

    def __init__(self, span=30, delta=0.1):
        self.cfg = None
        self.hist_x = []
        self.hist_y = []
        self.span = span
        self.delta = delta

    def keypress(self, e):
        if e.key in {'q', 'escape'}: os._exit(0) # unclean exit, but exit() or sys.exit() won't work
        if e.key in {' ', 'enter'}: plt.close() # skip blocking figures

    def plot(self, x, y, title, temperature=None):
        # Initialization of figure
        if title != self.cfg:
            self.cfg = title
            self.hist_x = []
            self.hist_y = []
            plt.figure(num=title).canvas.mpl_connect('key_press_event', self.keypress)
            plt.axis([-self.span, self.span, -0.5, 2.5])
            plt.ion()
        # Plotting
        plt.clf()
        xx = np.linspace(-self.span, self.span, 1000)
        plt.plot(xx, np.sin(xx)/xx + np.cos(xx/10)/3, c='k', lw=0.5)
        self.hist_x += [x]
        self.hist_y += [y]
        colors = np.arange(len(self.hist_x))
        plt.scatter(x, y, s=30, c='r')
        if temperature:
            plt.title('T          = {:.5f}\np(-0.3) = {:.8f} %\n[Press ESC to quit]'
                      .format(temperature, math.exp(-0.3/temperature) * 100), loc='left')
        else:
            plt.title('[Press ESC to quit]', loc='left')
        plt.gcf().canvas.flush_events()
        plt.waitforbuttonpress(timeout=0.001)

    def fitness(self, x):
        if x == 0:
            return 1
        return np.sin(x)/x + np.cos(x/10)/3

    def neighbors(self, x):
        res = []
        if x > -self.span + 3*self.delta: res += [x - i*self.delta for i in range(1, 4)]
        if x <  self.span - 3*self.delta: res += [x + i*self.delta for i in range(1, 4)]
        return res

    def random_state(self):
        return random.random() * self.span * 2 - self.span



class EightQueens(OptimizeMax):
    # An optimization problem in which we are trying to find positions of 8
    # queens on an 8x8 chessboard so that no two queens threaten each other.

    def fitness(self, x):

        """Hodnota fitness(x) predstavuje počet dvojíc dám, ktoré sa
        NEohrozujú. Globálnym maximom je teda 8*7/2 = 28 dvojíc"""

        def is_safe(pair1, pair2):
            x1, y1 = pair1
            x2, y2 = pair2

            #nie su v rovnakom stlpci: x1 != x2
            #ani v riadku: y1 != y2
            #ani na rovnakej diagonale zlava hore - dole vpravo (tam je sucet suradnic rovnaky)
            #ani na opacnej diagonale (tam je zase rozdiel suradnic rovnaky)

            return x1 != x2 and y1 != y2 and (x1+y1) != (x2+y2) and (x1-y1) != (x2-y2)
        
        
        safe_pairs = 0

        for i in range(8):
            queen1 = x[i]
            for j in range(i+1, 8):
                queen2 = x[j]

                safe_pairs += is_safe(queen1, queen2)

        return safe_pairs

    def neighbors(self, x):
        cpy = set(x) #aby som nepoužil nejaké políčko obsadené


        for i in range(8):
            old_pos = x[i]
            pos_x, pos_y = old_pos

            
            for dx in range(8):
                for dy in range(8):

                    new_x, new_y = (pos_x + dx)%8, (pos_y+dy)%8

                    if (new_x, new_y) not in cpy:

                        new_state = x.copy()
                        new_state[i] = (new_x, new_y)
                        yield new_state

            new_state[i] = old_pos
                


    def random_state(self):
        
        queens = set()
        
        while len(queens) < 8:
            x, y = random.randint(0, 7), random.randint(0, 7)

            queens.add((x, y))

        return list(queens)



if __name__ == '__main__':
    #  Task 1
    #for _ in range(10):
    #    problem = MysteryFunction()
    #    max_x = problem.hillclimb()
    #    print("Found maximum of Mystery function with hill climbing at x={}, f={}\n"
    #          .format(max_x, problem.fitness(max_x)))
        #sleep(2)


    #  Task 2
    n_attempts = 10
    for _ in range(n_attempts):
        problem = EightQueens()
        solution = problem.hillclimb(plot=False, max_steps=140)
        print("Found a solution (with fitness of {}) with hill climbing to 8 queens problem:\n{}\n"
              .format(problem.fitness(solution), solution))

    
