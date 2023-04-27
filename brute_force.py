import json
import numpy as np

#this is here if you want to verify the probabilities given by the induction calculator
#load growth pot probabilities
def load_probs():
    with open('growth_probs.txt', 'r') as f:
        level_probs = json.load(f)

    level_probs = {
        int(k): [(round(v[i] * 0.01, 3) if i < len(v) else 0) for i in range(10)]
        for k, v in level_probs.items()
        }
    return level_probs

#simulate a single growth pot
def simulate_growth(current, target, probs):
    level = current
    pots = 0
    while level < target:
        rng = np.random.random()
        arr = np.cumsum(probs[level])
        mask = arr < rng
        level += np.count_nonzero(mask)+1
        pots += 1
    return pots

#simulate 'iters' number of trials to get from start_level to target_level
def whole_simulation(start_level, target_level, iters, return_last=True):
    simulated = {}
    level_probs = load_probs()
    for i in range(target_level-1, start_level-1, -1):
        for j in range(iters):
            if j == 0:
                simulated[i] = simulate_growth(i, target_level, level_probs)
            else:
                simulated[i] += simulate_growth(i, target_level, level_probs)
    simulated = {k: v / iters for k, v in simulated.items()}
    if return_last:
        return simulated[start_level]
    else:
        return simulated


#example usage

#start_level = 169
#target_level = 194
#iters = 1000
#print(whole_simulation(start_level, target_level, iters))