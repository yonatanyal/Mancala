import pygame
import numpy as np
import torch
from Constants import *


class State:
    def __init__(self, board: np.ndarray = None, player = 1) -> None:
        if board is not None:
            self.board = board
        else:
            self.board = self.init_board()

        self.player = player
        self.extra_turn = False
        self.curr_extra_turn = False
        self.end_of_game = 0


    def init_board (self) -> np.ndarray :
        board = np.full((ROWS,COLS), 4) # all pits have 4 stones in the start of the game
        # both players start with 0 stones in their bases
        board[0][0] = 0 
        board[1][6] = 0 
        return board
    

    def to_tensor(self) -> torch.Tensor:
        return torch.tensor(self.board, dtype=torch.float32).flatten()
    

    @staticmethod
    def tensor_to_state(state_tensor: torch.Tensor, player: int):
        board = state_tensor.reshape([ROWS,COLS]).cpu().numpy()
        return State(board, player)
    

    def copy(self):
        return State(self.board.copy(), self.player)


    def diff(self) -> int:
        return self.board[0][0] - self.board[1][6]
    

if __name__ == '__main__':
    ten = torch.tensor([0,1,2,3,4,5,6,7,8,9,10,11,12,13])
    s = State()
    print(s.board)
