from Random_Agent import Random_Agent
from Environment import Environment
from Constants import *
import random
import time
from State import State


class Advanced_Random_Agent(Random_Agent):
        def __init__(self, player: int, env: Environment, test = False) -> None:
            super().__init__(player, env, test)
            

        def get_action(self, state: State) -> tuple[int]:
            action = super().get_action(state)

            # extra turn
            if action == (-1, -1):
                return action
            
            row = self.player - 1
            target = 0 if row == 0 else 6
            b = state.board
            extra_turns = [action for action in self.env.legal_actions(state) if b[action] % 13 == abs(action[1] - target)]

            target = self.env.empty_pits(state)
            on_empty_pit = [action for action in self.env.legal_actions(state) if b[action] == 13]
            if target:
                for t in target:
                    d = abs(action[1] - t[1])
                    on_empty_pit += [action for action in self.env.legal_actions(state) if b[action] == d or b[action] == 13 - d]
            
            special_actions = extra_turns + on_empty_pit
            if special_actions:
                action = random.choice(special_actions)
            
            return action


        def __call__(self,state: State,  events = None) -> tuple[int]:
            return self.get_action(state)