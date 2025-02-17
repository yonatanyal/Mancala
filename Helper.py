from Constants import *
import math

def epsilon_greedy(epoch = 0, start = epsilon_start, final = epsilon_final, decay = epsilon_decay):
        #######exp#######
        res = final + (start - final) * math.exp(-1 * epoch/decay)
        return res

        ######linear#######
        # res = start - (start / decay) * epoch
        # return res if res > final else final