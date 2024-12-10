import random
from Agent import Agent
from Environment import Environment
import time
from State import State

# class Random_Agent:
#         def __init__(self, player: int, env: Environment):
#             self.player = player
#             self.env = env
            

#         def get_action(self) -> tuple[int]:
#             if self.env.state.extra_turn:
#                  return (-1, -1)
            
#             col = random.choice(self.env.legal_moves())
#             print(self.player - 1, col)
#             return (self.player - 1, col) 


#         def __call__(self, _) -> tuple[int]:
#             return self.get_action()
        

class Random_Agent(Agent):
        def __init__(self, player: int, env: Environment) -> None:
            super().__init__(player, env)
            

        def get_action(self, state: State) -> tuple[int]:
            action = super().get_action(state) # extra turn
            if action: 
                return action
                        
            action = random.choice(self.env.legal_actions(state))
            return action 


        def __call__(self,state: State,  events = None) -> tuple[int]:
            return self.get_action(state)