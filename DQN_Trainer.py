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
    losses, avg_diffs, wins_per_10, defeats_per_10 = [], [], [], []
    avg_diff, wins, defeats = 0, 0 ,0
    start_epoch = 0

    # init Testing
    tester =  Tester(env, player1, player2)
    best_model_state_dict = player1.DQN.state_dict()
    best_win_p = 0
    
    # Load checkpoint
    resume_wandb = False
    run_id = 10
    checkpoint_path = f'Data/checkpoint{run_id}.pth'
    buffer_path = f'Data/buffer_run{run_id}.pth'
    file = f"Data\DQN_Model{run_id}.pth"
    if os.path.exists(checkpoint_path):
        resume_wandb = True
        checkpoint = torch.load(checkpoint_path)
        start_epoch = checkpoint['epoch'] + 1
        player1.DQN.load_state_dict(checkpoint['model_state_dict'])
        Q_hat.load_state_dict(checkpoint['model_state_dict'])
        best_model_state_dict = checkpoint['best_model_state_dict']
        optim.load_state_dict(checkpoint['optimizer_state_dict'])
        best_win_p = checkpoint['best_model_win_percentage']
        losses = checkpoint['loss']
        avg_diffs = checkpoint['avg_diff']
        wins_per_10 = checkpoint['wins']
        defeats_per_10 = checkpoint['defeats']
        buffer = torch.load(buffer_path)

    Q = player1.DQN

    # init wandb
    wandb.init(
        project="Mancala",
        resume=resume_wandb,
        id=f'Mancala {run_id}',
        config={
            "name": f'Mancala {run_id}',
            "checkpoint": checkpoint_path,
            "learning_rate": LR,
            "epochs": epochs,
            "start_epoch": start_epoch,
            "decay": epsilon_decay,
            "gamma": GAMMA,
            "batch_size": BATCH_SIZE, 
            "C": C,
            "Model": str(player1.DQN),
            "device": str(device)
        })
    
    ''' Training '''
    for epoch in range(start_epoch, epochs):
        # Sample Environment
        state = State()
        while not env.is_end_of_game(state):
            action = player1.get_action(state, epoch=epoch)
            after_state, reward = env.move(state, action)
            if env.is_end_of_game(after_state):
                buffer.push(state, action, reward, after_state, env.is_end_of_game(after_state))
                state = after_state
                break
            
            after_action = player2.get_action(state=after_state)
            next_state, next_reward = env.move(after_state, after_action)
            reward += next_reward
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

            # append params
            avg_diffs.append(avg_diff)
            wins_per_10.append(wins)
            defeats_per_10.append(losses)

            # log metrics to wandb
            wandb.log({
                "Wins Per 10 Games": wins,
                "Defeats Per 10 Games": defeats,
                "Loss": loss,
                "Average Piece Difference Per 10 Games" : avg_diff
            })

            avg_diff = 0
            wins = 0
            defeats = 0

        # Test the current model and save the one with the highest win %
        if epoch % 100 == 0:
            player1.test_mode()
            win_p = tester.test()[0]
            if win_p > best_win_p:
                best_model_state_dict = player1.DQN.state_dict()
            player1.train_mode()


        # create checkpoint
        if epoch % 10000 == 0:
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': player1.DQN.state_dict(),
                'best_model_state_dict': best_model_state_dict,
                'optimizer_state_dict': optim.state_dict(),
                'best_model_win_percentage' : best_win_p,
                'loss': losses,
                'avg_diff': avg_diffs,
                'wins': wins_per_10,
                'defeats': defeats_per_10
            }
            torch.save(checkpoint, checkpoint_path)
            torch.save(buffer, buffer_path)

    player1.save_param(file)

    wandb.finish()


if __name__ == '__main__':
    main()

