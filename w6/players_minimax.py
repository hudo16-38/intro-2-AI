import sys
import random
from games import TicTacToe, Gomoku
from copy import deepcopy

infinity = 0
try:
    infinity = sys.maxint
except:
    infinity = sys.maxsize



################################### PLAYERS ###################################

class Player:
    def choose_move(self, game, state):
        raise NotImplementedError



class AskingPlayer(Player):
    def choose_move(self, game, state):
        # Asks user (human) which move to take. Useful for debug.
        actions = game.actions(state)
        action = None
        while True:
            print("Choose one of the following positions: {}".format(actions))
            game.display_state(state, True)
            inp = input('> ')
            try:
                action = int(inp)
            except ValueError:
                pass
            if action in actions:
                return action
            print('"{}" is not valid action!'.format(inp))



class RandomPlayer(Player):
    def choose_move(self, game, state):
        # Picks random move from list of possible ones.
        return random.choice(game.actions(state))



class MinimaxPlayer(Player):
    def choose_move(self, game, state):
        ### Task 1 ###
        my_player = game.player_at_turn(state) # get 'X' or 'O'



        def max_value(state):
            ### YOUR CODE GOES HERE ###
            if game.is_terminal(state):
                return game.utility(state, my_player), None

            v = -infinity
            best_action = None
            for action in game.actions(state):
                new_state = game.state_after_move(state, action)
                v_new, act = min_value(new_state)
                if best_action is None or v_new > v:
                    best_action = action
                    v = v_new
            return (v, best_action)


        def min_value(state):
            if game.is_terminal(state):
                return game.utility(state, my_player), None
            
            v = infinity
            best_action = None
            for action in game.actions(state):
                new_state = game.state_after_move(state, action)
                v_new, act = max_value(new_state)
                if best_action is None or v_new < v:
                    best_action = action
                    v = v_new
            return (v, best_action)

        utility,action = max_value(state)
        return action



class AlphaBetaPlayer(Player):
    def choose_move(self, game, state):
        my_player = game.player_at_turn(state) # get 'X' or 'O'



        def max_value(state, alpha, beta):
            ### YOUR CODE GOES HERE ###
            if game.is_terminal(state):
                return game.utility(state, my_player), None

            v = -infinity
            best_action = None
            for action in game.actions(state):
                new_state = game.state_after_move(state, action)
                v_new, act = min_value(new_state, alpha, beta)
                if best_action is None or v_new > v:
                    best_action = action
                    v = v_new

                if v>=beta:
                    return (v, best_action)
                alpha = max(alpha, v)
            return (v, best_action)


        def min_value(state, alpha, beta):
            if game.is_terminal(state):
                return game.utility(state, my_player), None
            
            v = infinity
            best_action = None
            for action in game.actions(state):
                new_state = game.state_after_move(state, action)
                v_new, act = max_value(new_state, alpha, beta)
                if best_action is None or v_new < v:
                    best_action = action
                    v = v_new

                if v<=alpha:
                    return (v, best_action)
                beta = min(beta, v)
            return (v, best_action)

        utility,action = max_value(state, -infinity, infinity)
        return action



class AlphaBetaEvalPlayer(Player):
    def reflex_search(self, game, state):
        my_player = game.player_at_turn(state)
        opponent = game.other_player(my_player)
        actions = game.actions(state)
        cpy_state = deepcopy(state)
        cpy_state["player_on_turn"] = opponent

        #draw_moves, neutral_moves = [], []


        for action in actions:

            new_state = game.state_after_move(state, action)
            new_state2 = game.state_after_move(cpy_state, action)

            if game.is_terminal(new_state):
                utility = game.utility(new_state, my_player)

                if utility == 1:
                    return infinity, action

            if game.is_terminal(new_state2):
                if game.utility(new_state2, opponent) == 1:
                    return infinity, action

        return random.choice(range(1, 7)), random.choice(actions)

    def choose_move(self, game, state):
        ### Task 3  ###
        ### YOUR CODE GOES HERE ###
        my_player = game.player_at_turn(state)

        def max_value(state, alpha, beta, depth, max_depth=2):
            if game.is_terminal(state):
                return game.utility(state, my_player), None

            if depth == max_depth:
                return self.reflex_search(game, state)

            v = -infinity
            best_action = None
            for action in game.actions(state):
                new_state = game.state_after_move(state, action)
                v_new, act = min_value(new_state, alpha, beta, depth=depth+1, max_depth=max_depth)
                if best_action is None or v_new > v:
                    best_action = action
                    v = v_new

                if v>=beta:
                    return (v, best_action)
                alpha = max(alpha, v)
            return (v, best_action)


        def min_value(state, alpha, beta, depth, max_depth=2):
            if game.is_terminal(state):
                return game.utility(state, my_player), None

            if depth == max_depth:
                return self.reflex_search(game, state)
            
            v = infinity
            best_action = None
            for action in game.actions(state):
                new_state = game.state_after_move(state, action)
                v_new, act = max_value(new_state, alpha, beta, depth=depth+1, max_depth=max_depth)
                if best_action is None or v_new < v:
                    best_action = action
                    v = v_new

                if v<=alpha:
                    return (v, best_action)
                beta = min(beta, v)
            return (v, best_action)

        utility,action = max_value(state, -infinity, infinity, 0)
        return action



################################ MAIN PROGRAM #################################

if __name__ == '__main__':
    ## Print all moves of the game? Useful for debugging, annoying if it`s already working.
    show_moves = False


    ## Task 1
    #print('MiniMax plays as O and goes second - O must win or draw:')
    #TicTacToe().play([RandomPlayer(), MinimaxPlayer()], show_moves)

    #print('\n\nMiniMax plays as X and goes first - X must win or draw:')  # might take some extra time (max. cca 20s)
    #TicTacToe().play([MinimaxPlayer(), RandomPlayer()], show_moves)

    #print('\n\nMiniMax vs. MiniMax - should be draw:')
    #for _ in range(10):
    #   TicTacToe().play([MinimaxPlayer(), MinimaxPlayer()], show_moves)  # might take some extra time (max. cca 20s)


    # ## Task 2
    #print('\n\nAlpha-Beta plays as X and goes first - X must win or draw:')
    #TicTacToe().play([AlphaBetaPlayer(), RandomPlayer()], show_moves)

    #print('\n\nAlpha-Beta vs. MiniMax - should be draw:')
    #TicTacToe().play([AlphaBetaPlayer(), MinimaxPlayer()], show_moves)


    # ## Task 3
    #print('\n\nAlpha-Beta Eval vs. itself - should be a well-played game.')
    #Gomoku().play([AlphaBetaEvalPlayer(), AlphaBetaEvalPlayer()], show_moves=True)


    # ## Play computer against human:
    # ## a) human cannot win, draw is possible (assuming algorithm is correct)
    # TicTacToe().play([AskingPlayer(), MinimaxPlayer()])   # Task 1
    # TicTacToe().play([MinimaxPlayer(), AskingPlayer()])   # Task 1
    TicTacToe(4, 4, 3).play([AskingPlayer(), AlphaBetaPlayer()]) # Task 2
    # TicTacToe().play([AlphaBetaPlayer(), AskingPlayer()]) # Task 2
    # ## b) computer will win, human will loose, draw is not possible
    #TicTacToe(4,4,3).play([AlphaBetaPlayer(), AskingPlayer()]) # Task 2
    # ## c) human, have fun! (recommended depth limit=2~3)  
    # Gomoku().play([AskingPlayer(), AlphaBetaEvalPlayer()]) # Task 3
