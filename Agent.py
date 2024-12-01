from Environment import Environment


class Agent:
    def __init__(self, player:int, env: Environment) -> None:
            self.player = player
            self.env = env


    def get_action(self) -> tuple[int] | None:
            if self.env.state.extra_turn:
                return (-1, -1)
            