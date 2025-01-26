import torch


#FPS
FPS = 60

#Screen Size
WIDTH, HEIGHT = 1200,650
H_WIDTH, H_HEIGHT = 1200,70
M_WIDTH, M_HEIGHT = 1200,400
SCORES_WIDTH, SCORES_HEIGHT = 1200,90

#Board
ROWS, COLS = 2, 7
SQUARE_WIDTH = 150
SQUARE_HEIGHT = 200

#RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ANTIQUE_WHITE = (250, 235, 215)

#epsilon Greedy
epsilon_start = 1
epsilon_final = 0.01
epsilon_decay = 5000

#DQN Params
input_size = 16 # state: board = 2 * 7 + action 1 * 2
layer1 = 128
layer2 = 64
output_size = 1 # Q(s,a)
GAMMA = 0.99

#DQN Training
epochs = 60000
C = 200
BATCH_SIZE = 64
LR = 0.001

#Device
device = torch.device("cpu")
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

best_model_path_P1 = 'Data/Player1/DQN_Model11.pth'
best_model_path_P2 = 'Data/Player2/DQN_Model2.pth'