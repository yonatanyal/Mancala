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


class DQN_Agent(Agent):
    def __init__(self, player: int, env: Environment, parameters_path = None, test = False, train = False) -> None:
        super().__init__(player, env)
        self.DQN = DQN()
        if parameters_path:
            self.DQN.load_params(parameters_path)
        self.test = test
        self.train = train


    def get_action (self, state: State, epoch = 0) -> tuple[int]:
        action = super().get_action(state, self.train)
        if action: 
            return action

        epsilon = epsilon_greedy(epoch)
        rnd = random.random()
        actions = self.env.legal_actions(state)
        if self.train and rnd < epsilon:
            return random.choice(actions)
        
        state_tensor = state.to_tensor()
        action_np = np.array(actions, dtype=np.float32)
        action_tensor = torch.from_numpy(action_np)
        expand_state_tensor = state_tensor.unsqueeze(0).repeat((len(action_tensor),1))

        with torch.no_grad():
            Q_values = self.DQN(expand_state_tensor, action_tensor)
        max_action = torch.argmax(Q_values)
        return actions[max_action]


    def get_actions(self, states: torch.Tensor, dones: torch.Tensor) -> torch.Tensor:
        self.train == False # Excluding epsilon greedy
        actions = []
        for i, state in enumerate(states):
            if dones[i].item():
                actions.append((-1, -1))
            else:
                actions.append(self.get_action((State.tensor_to_state(state, self.player)))) 
        self.train == True

        return torch.tensor(actions)
    

    def test_mode(self):
        self.train = False
        self.test = True

    
    def train_mode(self):
        self.train = True
        self.test = False


    def save_param (self, path) -> None:
        self.DQN.save_params(path)


    def load_params (self, path) -> None:
        self.DQN.load_params(path)


    def __call__(self, state: State, events = None) -> tuple[int]:
        return self.get_action(state)