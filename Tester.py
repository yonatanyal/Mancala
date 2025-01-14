import torch
from Agent import Agent
from Random_Agent import Random_Agent
from DQN import DQN
from DQN_Agent import DQN_Agent
from State import State
from Constants import *
from Environment import Environment


class Tester: 
    def __init__(self, env: Environment, player1: Agent, player2: Agent) -> None:
        self.env: Environment = env
        self.player1: Agent = player1
        self.player2: Agent = player2
        

    def test(self, games: int = 100) -> tuple[int,int,int]:
        player = self.player1
        player1_wins = 0
        player2_wins = 0
        ties = 0

        for game in range(games):
            play = True
            while play:
                action = player(self.env.state)
                self.env.move(self.env.state, action)
                player = self.switch_players(player)
                if self.env.is_end_of_game(self.env.state):
                    res = self.env.state.end_of_game
                    if res == 1:
                        player1_wins += 1
                    elif res == 2:
                        player2_wins += 1
                    else:
                        ties += 1
                    self.env.state = State()
                    player = self.player1
                    play = False

        self.env.restart()
        return player1_wins, player2_wins, ties        


    def switch_players(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1


if __name__ == '__main__':
    env = Environment(State())
    player1 = DQN_Agent(1, env, parameters_path='Data/DQN_Model11.pth', test=True)
    # player1 = Random_Agent(1, env)
    player2 = Random_Agent(2, env)
    tester = Tester(env,player1, player2)
    print(tester.test())
    