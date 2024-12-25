from Constants import *
import math

def epsilon_greedy(epoch = 0, start = epsilon_start, final = epsilon_final, decay = epsilon_decay):
        res = final + (start - final) * math.exp(-1 * epoch/decay)
        return res