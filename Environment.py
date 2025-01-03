import numpy as np
from State import State
from Constants import *


class Environment:
    def __init__(self, state: State = State()) -> None:
        self.state = state


    def legal(self, state: State, action: tuple) -> bool:
        if not action:
            return False
        if action == (1, 6) or action == (0, 0): # action is one of the bases
            return False
        if action[0] != state.player - 1: # action is in the wrong player's row
            return False
        if state.board[action] == 0: # action is an empty pit
            return False
        
        return True
    

    def legal_actions(self, state: State) -> list:
        row = state.player - 1
        return [(row, col) for col in range(COLS) if self.legal(state, (row, col))]


    def move(self, state: State, action: tuple) -> tuple[State, int]:
        state.extra_turn = False
        state.curr_extra_turn = False
        if action == (-1, -1):
            state.curr_extra_turn = True
            self.switch_players(state)
            return state, 0
        
        row, col = action
        player = state.player
        stones = state.board[action]; stones_left = stones
        state.board[action] = 0
        step = -1 if player == 1 else 1
        prev_p1_score, prev_p2_score = state.board[0][0], state.board[1][6]
        reward = 0

        while stones_left > 0:
            for pit_col in range(col + step, col + (stones + 1) * step, step):
                curr_pit = (row, pit_col)

                if (player == 1 and curr_pit != (1,6)) or (player == 2 and curr_pit != (0,0)):
                    state.board[curr_pit] += 1
                    stones_left -= 1


                if curr_pit == (0,0) or curr_pit == (1,6):
                    col = pit_col + step
                    break
                
            step *= -1
            row += step
            stones = stones_left
        
        # Checking for extra turn
        if (player == 1 and curr_pit == (0,0)) or (player == 2 and curr_pit == (1,6)): 
            state.extra_turn = True
            reward += 1 if player == 1 else -1 # Reward player
        
        # Checking if the last stone landed on an empty pit
        elif player == 1 and state.board[curr_pit] == 1 and curr_pit[0] == 0 and state.board[1][curr_pit[1] - 1] != 0:
            added = state.board[1][curr_pit[1] - 1] + 1
            state.board[0][0] += added
            state.board[1][curr_pit[1] - 1] = 0
            state.board[curr_pit] = 0
            
        elif player == 2 and state.board[curr_pit] == 1 and curr_pit[0] == 1 and state.board[0][curr_pit[1] + 1] != 0:
            added = state.board[0][curr_pit[1] + 1] + 1
            state.board[1][6] += added
            state.board[0][curr_pit[1] + 1] = 0
            state.board[curr_pit] = 0

        # Rewarding player
        curr_p1_score, curr_p2_score = state.board[0][0], state.board[1][6]
        reward += curr_p1_score - prev_p1_score if player == 1 else curr_p2_score - prev_p2_score
        
        if self.end_of_game(state):
            diff = state.diff()
            reward += 10*diff
        self.switch_players(state)

        # Returning reward and next state
        return state, reward


    def switch_players(self, state: State) -> None:
        if state.player == 1:
            state.player = 2
            return
        
        state.player = 1
        

    def is_end_of_game(self, state: State) -> bool:
        return state.end_of_game != 0


    def end_of_game(self, state: State) -> int:
        board = state.board
        row1_sum = np.sum(board[0]) - board[0, 0]
        row2_sum = np.sum(board[1]) - board[1, 6]
        player1_score = board[0][0]
        player2_score = board[1][6]

        # Checking if the game has ended
        if row1_sum != 0 and row2_sum != 0:
            return 0
        
        # Updating score and board
        player1_score += row2_sum   
        player2_score += row1_sum  
        state.board = np.zeros((ROWS,COLS), dtype=int)
        state.board[0][0] = player1_score
        state.board[1][6] = player2_score

        # Chcking the game result
        if state.diff() > 0:
            state.end_of_game = 1
        
        elif state.diff() < 0:
            state.end_of_game = 2
        
        else:
            state.end_of_game = -1

        return 1