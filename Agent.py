from Environment import Environment
from State import State
import time


class Agent:
    def __init__(self, player:int, env: Environment, test = False) -> None:
            self.player = player
            self.env = env
            self.test = test


    def get_action(self, state: State, train = False) -> tuple[int] | None:
            if not (train or self.test):
                  time.sleep(0.6)
                  
            if state.extra_turn:
                return (-1, -1)
            