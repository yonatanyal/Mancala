from DQN import DQN
from DQN_Agent import DQN_Agent
from Random_Agent import Random_Agent
from Environment import Environment
from ReplayBuffer import ReplayBuffer
from State import State
from Tester import Tester
import torch 
from Constants import *
import wandb
import os


def main ():
    ''' Preparing Data '''
    # init model
    env = Environment()
    player1 = DQN_Agent(1, env , train=True)
    player2 = Random_Agent(2, env)
    buffer = ReplayBuffer()
    Q_hat :DQN = player1.DQN.copy()
    Q_hat.train = False
    optim = torch.optim.Adam(player1.DQN.parameters(), lr=LR)

    # init metrics
    avg_diff, wins, defeats = 0, 0 ,0
    start_epoch = 0

    Q = player1.DQN
    
    ''' Training '''
    for epoch in range(start_epoch, epochs):
        # Sample Environment
        state = State()
        while not env.is_end_of_game(state):
            action = player1.get_action(state, epoch=epoch)
            print(state.board)
            print(action)
            after_state, reward = env.move(state, action)
            if env.is_end_of_game(after_state):
                buffer.push(state, action, reward, after_state, env.is_end_of_game(after_state))
                state = after_state
                break
            
            after_action = player2.get_action(state=after_state)
            print(after_state.board)
            print(after_action)
            next_state, next_reward = env.move(after_state, after_action)
            reward += next_reward
            print(reward)
            print('-----------------------------')
            buffer.push(state, action, reward, next_state, env.is_end_of_game(next_state))
            state = next_state

        # update metrics
        diff = state.diff()
        avg_diff += diff
        if diff > 0:
            wins += 1
        elif diff < 0:
            defeats += 1   

        # Checking if the buffer's length is greater than the minimum
        if len(buffer) < 5000:
            continue

        # Training
        states, actions, rewards, next_states, dones = buffer.sample(BATCH_SIZE)
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
    
        if (epoch + 1) % 10 == 0:
            # print metrics
            avg_diff /= 10
            print(f'epoch: {epoch}, loss: {loss.item():.2f}, wins per 10 games: {wins}, avg piece difference: {avg_diff}')

            avg_diff = 0
            wins = 0
            defeats = 0


    player1.save_param("Data/debug_Training")


if __name__ == '__main__':
    main()

