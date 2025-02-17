from DQN import DQN
from DQN_Agent import DQN_Agent
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
    # init models
    env = Environment()
    player1 = DQN_Agent(1, env , train=True)
    buffer1 = ReplayBuffer()
    Q_hat1 :DQN = player1.DQN.copy()
    Q_hat1.train = False
    optim1 = torch.optim.Adam(player1.DQN.parameters(), lr=LR)


    player2 = DQN_Agent(2, env, train=True)
    buffer2 = ReplayBuffer()
    Q_hat2 :DQN = player2.DQN.copy()
    Q_hat2.train = False
    optim2 = torch.optim.Adam(player2.DQN.parameters(), lr=LR)
    loss = torch.tensor([0])

    # init metrics
    losses, avg_diffs, wins_per_10 = [], [], [], []
    avg_diff, wins, defeats = 0, 0 ,0
    start_epoch = 0

    

    # init Testing
    tester =  Tester(env, player1, player2)
    best_model_state_dict1 = player1.DQN.state_dict()
    best_win_p1 = 0

    best_model_state_dict2 = player2.DQN.state_dict()
    best_win_p2 = 0
    
    # Load player 1 checkpoint 
    resume_wandb = False
    run_id = 201
    checkpoint_path1 = f'Data/Player1/checkpoint{run_id}.pth'
    buffer_path1 = f'Data/buffers/Player1/buffer_run{run_id}.pth'
    file = f"Data/Player1/DQN_Model{run_id}.pth"
    if os.path.exists(checkpoint_path1):
        checkpoint = torch.load(checkpoint_path1)
        start_epoch = checkpoint['epoch'] + 1
        player1.DQN.load_state_dict(checkpoint['model_state_dict'])
        Q_hat1.load_state_dict(checkpoint['model_state_dict'])
        best_model_state_dict1 = checkpoint['best_model_state_dict']
        optim1.load_state_dict(checkpoint['optimizer_state_dict'])
        best_win_p1 = checkpoint['best_model_win_percentage']
        losses1 = checkpoint['loss']
        avg_diffs1 = checkpoint['avg_diff']
        wins_per_10_1 = checkpoint['wins']
        buffer1 = torch.load(buffer_path1)

    # Load player2 checkpoint
    checkpoint_path2 = f'Data/Player2/checkpoint{run_id}.pth'
    buffer_path2 = f'Data/buffers/Player2/buffer_run{run_id}.pth'
    file = f"Data/Player2/DQN_Model{run_id}.pth"
    if os.path.exists(checkpoint_path2):
        checkpoint = torch.load(checkpoint_path2)
        player2.DQN.load_state_dict(checkpoint['model_state_dict'])
        Q_hat2.load_state_dict(checkpoint['model_state_dict'])
        best_model_state_dict2 = checkpoint['best_model_state_dict']
        optim2.load_state_dict(checkpoint['optimizer_state_dict'])
        best_win_p2 = checkpoint['best_model_win_percentage']
        losses2 = checkpoint['loss']
        avg_diffs2 = checkpoint['avg_diff']
        wins_per_10_2 = checkpoint['wins']
        buffer2 = torch.load(buffer_path2)

    # init wandb
    wandb.init(
        project="Mancala",
        resume=resume_wandb,
        id=f'Mancala {run_id}',
        config={
            "name": f'Mancala {run_id}',
            "checkpoint1": checkpoint_path1,
            "checkpoint2": checkpoint_path2,
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
        state = State()
        while not env.is_end_of_game(state):
            #region ############### Sample Environment
            action = player1.get_action(state, epoch=epoch)
            after_state, reward = env.move(state.copy(), action)
            if env.is_end_of_game(after_state):
                buffer.push(state, action, reward, after_state, env.is_end_of_game(after_state))
                state = after_state
                break
            
            after_action = player2.get_action(state=after_state)
            next_state, next_reward = env.move(after_state.copy(), after_action)
            reward += next_reward
            done = env.is_end_of_game(next_state)
            buffer.push(state, action, reward, next_state, done)
            state = next_state

            # Checking if the buffer's length is greater than the minimum
            if len(buffer) < 5000:
                continue
            #endregion

            #region ############### Back propagation 
            states, actions, rewards, next_states, dones = buffer.sample(BATCH_SIZE)
            Q_values = Q(states, actions)
            next_actions = player1.get_actions(next_states, dones)
            with torch.no_grad():
                Q_hat_Values = Q_hat(next_states, next_actions)
            
            loss = Q.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()
            #endregion

        if epoch % C == 0:
            Q_hat.load_state_dict(Q.state_dict())

        # update metrics
        diff = state.diff()
        avg_diff += diff
        if diff > 0:
            wins += 1
        elif diff < 0:
            defeats += 1   
    
        if (epoch + 1) % 10 == 0:
            # print metrics
            avg_diff /= 10
            print(f'epoch: {epoch}, loss: {loss.item():.2f}, wins per 10 games: {wins}, avg piece difference: {avg_diff}')

            # append metrics
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

