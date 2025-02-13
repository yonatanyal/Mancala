import pygame
from Graphics import Graphics
from State import State
from Environment import Environment
from Human_Agent import Human_Agent
from Random_Agent import Random_Agent
from Advanced_Random_Agent import Advanced_Random_Agent
from DQN_Agent import DQN_Agent
from Agent import Agent
import sys
from Constants import *


pygame.init()
graphics = Graphics()
clock = pygame.time.Clock()
env = Environment(State())

player1 = Human_Agent(1, env, graphics)
player2 = Human_Agent(2, env, graphics)

def main_menu():
    global player1, player2
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        pick = graphics.main_menu(events)
        match pick:
            case 1:
                player1  = Human_Agent(1, env, graphics)
            case 2:
                player1  = Random_Agent(1, env)
            case 3:
                player1  = DQN_Agent(1, env, parameters_path=best_model_path_P1)
            case 4:
                player1  = Advanced_Random_Agent(1, env)
            case 5:
                player2  = Human_Agent(2, env, graphics)
            case 6:
                player2  = Random_Agent(2, env)
            case 7:
                player2  = DQN_Agent(2, env, parameters_path=best_model_path_P2)
            case 8:
                player2  = Advanced_Random_Agent(2, env)
            case 9:
                play()

        pygame.display.update()
        # pygame.display.flip()
        clock.tick(FPS)


def play(): 
    env.restart()
    run = True
    player = player1

    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        action = player(env.state, events)
        if action:
            env.move(env.state, action)
            player = switch_players(player)
            if env.is_end_of_game(env.state):
                end_menu(env.state.end_of_game)
                return

        graphics(env.state)   
        pygame.display.update()
        # pygame.display.flip()
        clock.tick(FPS)


def end_menu(result):
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        
        pick = graphics.end_menu(result, events)
        if pick:
            return

        pygame.display.update()
        # pygame.display.flip()
        clock.tick(FPS)


def switch_players(player: Agent):
    if player == player1:
        return player2
    else:
        return player1


if __name__ == '__main__':
    main_menu()