import random
from typing import Any
import torch
import torch.nn as nn
import numpy as np
from DQN import DQN
from Agent import Agent
from Environment import Environment
from State import State
from Constants import *
from Helper import epsilon_greedy
import time


MSELoss = nn.MSELoss()


class DQN_Agent(Agent):
    def __init__(self, player: int, env: Environment, parameters_path = None, train = False, test = False) -> None:
        super().__init__(player, env)
        self.DQN = DQN()
        if parameters_path:
            self.DQN.load_params(parameters_path)
        self.train = train
        self.test = test


    def get_action (self, state: State, epoch = 0) -> tuple[int]:
        action = super().get_action(state)
        if action: 
            return action
        
        if not (self.train or self.test):
            time.sleep(0.6)

        epsilon = epsilon_greedy(epoch)
        rnd = random.random()
        actions = self.env.legal_actions(state)
        if self.train and rnd < epsilon:
            return random.choice(actions)
        
        state_tensor = state.to_tensor()
        action_np = np.array(actions, dtype=np.float32)
        action_tensor = torch.from_numpy(action_np)
        expand_state_tensor = state_tensor.unsqueeze(0).repeat((len(action_tensor),1))
        # state_action = torch.cat((expand_state_tensor, action_tensor ), dim=1)
        with torch.no_grad():
            Q_values = self.DQN(expand_state_tensor, action_tensor)
        max_action = torch.argmax(Q_values)
        return actions[max_action]


    def get_actions(self, states: torch.Tensor, dones: torch.Tensor) -> torch.Tensor:
        actions = []
        for i, state in enumerate(states):
            if dones[i].item():
                actions.append((1, 1))
            else:
                actions.append(self.get_action((State.tensor_to_state(state, self.player)))) 
        return torch.tensor(actions)
    

    def save_param (self, path) -> None:
        self.DQN.save_params(path)


    def load_params (self, path) -> None:
        self.DQN.load_params(path)


    def __call__(self, state: State, events = None) -> tuple[int]:
        return self.get_action(state)