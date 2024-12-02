import pygame
from Agent import Agent
from typing import Any
from Environment import Environment
from Graphics import Graphics
from State import State


# class Human_Agent:
#     def __init__(self, player: int, env: Environment, graphics: Graphics):
#         self.player = player
#         self.env = env
#         self.graphics = graphics

#     def get_action(self, events) -> tuple[int]:
#         if self.env.state.extra_turn:
#                  return (-1, -1)

#         for event in events:
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 pos = event.pos
#                 action = self.graphics.calc_row_col(pos)
#                 if self.env.legal(action):
#                     return action

    
#     def __call__(self, events) -> tuple[int]:
#         return self.get_action(events)
    

class Human_Agent(Agent):
    def __init__(self, player: int, env: Environment, graphics: Graphics):
        super().__init__(player, env)
        self.graphics = graphics


    def get_action(self, state: State, events) -> tuple[int]:
        action = super().get_action(state)
        if action: 
            return action

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                action = self.graphics.calc_row_col(pos)
                if self.env.legal(self.env.state, action):
                    return action

    
    def __call__(self, state: State, events) -> tuple[int]:
        return self.get_action(state, events)