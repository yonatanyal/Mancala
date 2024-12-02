from Environment import Environment
from State import State


class Agent:
    def __init__(self, player:int, env: Environment) -> None:
            self.player = player
            self.env = env


    def get_action(self, state: State) -> tuple[int] | None:
            if state.extra_turn:
                return (-1, -1)
            