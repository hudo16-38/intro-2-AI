import random
from games import TicTacToe, Gomoku
from copy import deepcopy

################################### PLAYERS ###################################

class Player:
    def choose_move(self, game, state):
        raise NotImplementedError



class AskingPlayer(Player):
    def choose_move(self, game, state):
        # Asks user (human) which move to take. Useful for debug.
        actions = game.actions(state)
        print("Choose one of the following positions: {}".format(actions))
        game.display_state(state, True)
        return int(input('> '))



class RandomPlayer(Player):
    def choose_move(self, game, state):
        # Picks random move from list of possible ones.
        return random.choice(game.actions(state))



class MyPlayer(Player):
    def choose_move(self, game, state):
        ### YOUR CODE GOES HERE ###
        ### Examples:
        # my_player = game.player_at_turn(state)
        # opponent = game.other_player(my_player)
        # board = game.board_in_state(state)
        # if board[0][1] == my_player: ...
        # possible_actions = game.actions(state)
        # some_action = possible_actions[0]
        # new_state = game.state_after_move(current_state, some_action)
        # if game.is_terminal(some_state): ...
        # utility = game.utility(some_state, my_player)

        my_player = game.player_at_turn(state)
        opponent = game.other_player(my_player)
        actions = game.actions(state)
        cpy_state = deepcopy(state)
        cpy_state["player_on_turn"] = opponent

        draw_moves, neutral_moves = [], []


        for action in actions:

            new_state = game.state_after_move(state, action)
            new_state2 = game.state_after_move(cpy_state, action)

            if game.is_terminal(new_state):
                utility = game.utility(new_state, my_player)

                if utility == 1:
                    return action

                if utility == 0:
                    draw_moves.append(action)
            
            else:
                neutral_moves.append(action)

            if game.is_terminal(new_state2):
                if game.utility(new_state2, opponent) == 1:
                    return action


        if neutral_moves:
            return random.choice(neutral_moves)
        return random.choice(draw_moves)


        



################################ MAIN PROGRAM #################################

if __name__ == '__main__':
    ## Print all moves of the game? Useful for debugging, annoying if it`s already working.
    show_moves = False

    ## Play computer against human:
    ## a) with random player
    #TicTacToe().play([RandomPlayer(), AskingPlayer()], show_moves=show_moves)
    ## b) simple TicTacToe with MyPlayer
    TicTacToe().play([MyPlayer(), AskingPlayer()], show_moves=show_moves)
    ## c) difficult Gomoku with MyPlayer
    # Gomoku().play([MyPlayer(), AskingPlayer()], show_moves=show_moves)

    ## Test MyPlayer
    ## a) play single game of TicTacToe
    #TicTacToe().play([MyPlayer(), RandomPlayer()], show_moves=show_moves)
    ## b) play single game of Gomoku
    #Gomoku().play([MyPlayer(), RandomPlayer()], show_moves=show_moves)
    ## c) play N games
    #TicTacToe().play_n_games([MyPlayer(), RandomPlayer()], n=10)
    ##Gomoku().play_n_games([MyPlayer(), RandomPlayer()], n=10)
