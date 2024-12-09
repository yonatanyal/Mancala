from DQN import DQN
from DQN_Agent import DQN_Agent
from Random_Agent import Random_Agent
from Environment import Environment
from ReplayBuffer import ReplayBuffer
from State import State
import torch 
from Constants import *


def main ():
    env = Environment()
    player1 = DQN_Agent(1, env, parametes_path="Data\DQN_TEST1.pth" ,train=True)
    player2 = Random_Agent(2, env)
    replay = ReplayBuffer()
    Q = player1.DQN
    Q_hat :DQN = Q.copy()
    Q_hat.train = False
    optim = torch.optim.SGD(Q.parameters(), lr=LR)
       
    for epoch in range(epochs):
        print (epoch, end="\r")
        state = State()
        while not env.end_of_game(state):
            action = player1.get_action(state, epoch=epoch)
            after_state, reward = env.move(state, action)
            if env.end_of_game(after_state):
                replay.push(state, action, reward, after_state, env.end_of_game(next_state))
                break
            
            after_action = player2.get_action(state=after_state)
            next_state, reward = env.move(after_state, after_action)
            replay.push(state, action, reward, next_state, env.end_of_game(next_state))
            state = next_state
            
        if len(replay) < BATCH_SIZE:
            continue

        states, actions, rewards, next_states, dones = replay.sample(BATCH_SIZE)
        Q_values = Q(states, actions)
        next_actions = player1.get_actions(next_states, dones)
        with torch.no_grad():
            Q_hat_Values = Q_hat(next_states, next_actions)
        
        loss = Q.loss(Q_values, rewards, Q_hat_Values, dones)
        loss.backward()
        optim.step()
        optim.zero_grad()
        
    if epoch % C == 0:
        Q_hat.load_state_dict(Q.state_dict())

    player1.save_param(path)


if __name__ == '__main__':
    main()