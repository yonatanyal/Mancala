from DQN import DQN
from DQN_Agent import DQN_Agent
from Random_Agent import Random_Agent
from Environment import Environment
from ReplayBuffer import ReplayBuffer
from State import State
import torch 
from Constants import *
import matplotlib.pyplot as plt
import numpy as np
import wandb


def main ():
    #init wandb
    wandb.init(
        project="Mancala", 
        config = {
            "layer1" : layer1, 
            "layer2" : layer2, 
            "gamma" : GAMMA ,
            "epochs" : epochs ,
            "C" : C, 
            "batch_size" : BATCH_SIZE, 
            "learning _rate" : LR
        }
    )

    #init parameters
    env = Environment()
    player1 = DQN_Agent(1, env , parameters_path="Data/checkpoint4",train=True)
    player2 = Random_Agent(2, env)
    replay = ReplayBuffer()
    Q = player1.DQN
    Q_hat :DQN = Q.copy()
    Q_hat.train = False
    optim = torch.optim.Adam(Q.parameters(), lr=LR)

    avg_diff = 0
    wins = 0
    losses = []
    avg_diffs = []
    wins_per_100 = []
       
    for epoch in range(epochs):
        state = State()
        while not env.end_of_game(state):
            action = player1.get_action(state, epoch=epoch)
            after_state, reward = env.move(state, action)
            if env.end_of_game(after_state):
                replay.push(state, action, reward, after_state, env.end_of_game(next_state))
                avg_diff += after_state.diff()
                if after_state.diff() > 0:
                    wins+=1
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
    
        if epoch % 100 == 0:
            avg_diff /= 100
            losses.append(loss.item())
            wins_per_100.append(wins)
            avg_diffs.append(avg_diff)
            print(f'epoch: {epoch}, loss: {loss.item():.2f}, wins per 100: {wins}, avg piece diff: {avg_diff}')

            avg_diff = 0
            wins = 0

        if epoch % 50000 == 0:
            player1.save_param(f'Data/checkpoint')


    player1.save_param(file)
    torch.save(losses, 'Data/losses_Training1.pth')
    torch.save(wins_per_100, 'Data/wins_Training1.pth')
    torch.save(avg_diffs, 'Data/avg_diffs_Training1.pth')

    # epochs_np = np.array(list(range(0, epochs-100, 100)))
    # losses_np = np.array(losses)
    # wins_per_100_np = np.array(wins_per_100)
    # avg_diffs_np = np.array(avg_diffs)

    # plt.plot(epochs_np, losses_np)
    # plt.title('losses')
    # plt.show()

    # plt.plot(epochs_np, wins_per_100_np)
    # plt.title('wins_per_100')
    # plt.show()


    # plt.plot(epochs_np, avg_diffs_np)
    # plt.title('average difference')
    # plt.show()


if __name__ == '__main__':
    main()

