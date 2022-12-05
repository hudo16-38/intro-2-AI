#zadanie: CSP Map
#autor: Roman Hudec
#datum: 21.10.2022


import sys
import time
from maps import *

class MapCSP():
    def __init__(self, states, neighbours):
        # List of available colors
        self.color_options = ['red', 'green', 'blue', 'yellow']
        self.states = states
        self.neighbours = neighbours
        self.colors = {s: None for s in self.states}

    def print_map(self):
        # Prints all states and their colors
        for s in sorted(self.states):
            print('{} has color: {}'.format(s, self.get_color(s)))
        print()


    def set_color(self, state, color):
        # Assign color to a state
        self.colors[state] = color

    def del_color(self, state):
        # Remove color from state - reset to None
        self.colors[state] = None

    def get_color(self, state):
        # Get color assigned to a state
        return self.colors[state]

    def has_color(self, state):
        # Returns True if state has already a color
        return self.colors[state] != None

    def same_colors(self, state1, state2):
        # Returns True if state1 and state2 are colored with the same color.
        return self.has_color(state1)  and  self.get_color(state1) == self.get_color(state2)

    def all_colored(self):
        # Returns True if all states of the map are already colored.
        return all([self.has_color(s) for s in self.states])

    def is_correct_coloring(self):
        # Returns True if coloring is all correct, False if not. Prints the result with found error (if any).
        print('Coloring is ', end='')
        for s1 in self.states:
            if self.get_color(s1) not in self.color_options:
                print('INCORRECT - {} has invalid color: {}\n'.format(s1, self.get_color(s1)))
                return False
            for s2 in self.neighbours[s1]:
                if self.same_colors(s1,s2):
                    print('INCORRECT - {} and {} have conflicting color {}\n'.format(s1, s2, self.get_color(s1)))
                    return False
        print('OK\n')
        return True


    def can_set_color(self, state, color):

##        count = 0
##        for n in self.neighbours[state]:
##            if self.get_color(n) != color:
##                count += 1
##
##        return count == len(self.neighbours[state])
        
        for n in self.neighbours[state]:
            if self.get_color(n) == color:
                return False
        return True

    def _heuristic(self, state):
        "Minimum remaining value"

        if self.has_color(state):
            return float("inf") #aby mi zafarbenych hadzalo na koniec tych na vyber
        remaining = set(self.color_options)

        for n in self.neighbours[state]:
            clr = self.get_color(n) 
            if clr is not None: #ak je zafarbeny
                remaining.discard(clr)

        return len(remaining)
                
                
                
            

    def select_next_state(self, use_heuristic=False):
        if use_heuristic:

            states = sorted(self.states, key=self._heuristic) #s najmensou hodnotou remaining value je prvy, sporiadam podla heuristiky
            
            
            candidate = states[0]

            if self._heuristic(candidate) == float("inf"): #vsetci su zafarbeni
                return False
            return candidate

        else:
            for state in self.states:
                if not self.has_color(state):
                    return state
            return False

    def color_map(self):
        if self.all_colored():
            return True

        next_state = self.select_next_state(True)
        if not next_state:
            return False

        for color in self.color_options:
            if self.can_set_color(color=color, state=next_state):
                self.set_color(next_state, color)
                res = self.color_map()
                if res:
                    return True
                self.del_color(next_state)
        
        return False




if __name__ == "__main__":
    maps = [('Australia', AustraliaMap()),
            ('USSR', USSRMap()),
            ('USA', USAMap()),
            ('World', WorldMap()),

            ('Impossible Australia', ImpossibleMap(AustraliaMap())),
            ('Impossible USSR', ImpossibleMap(USSRMap())),
            ('Impossible USA', ImpossibleMap(USAMap())),
            ('Impossible World', ImpossibleMap(WorldMap()))
            ]

    for name, mapa in maps:
        print('==== {} ===='.format(name))
        t = time.time()
        has_result = mapa.color_map()    # Compute the colors for an empty map
        print('Time: {:.3f} ms'.format( (time.time() - t)*1000 ))
        if has_result:
            mapa.is_correct_coloring()  # Print whether coloring is correct
        else:
            print('Coloring does not exist\n')
        mapa.print_map()    # Print whole coloring
