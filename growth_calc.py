import json

#load growth pot probabilities
def load_probs():
    with open('growth_probs.txt', 'r') as f:
        level_probs = json.load(f)

    level_probs = {
        int(k): [(round(v[i] * 0.01, 3) if i < len(v) else 0) for i in range(10)]
        for k, v in level_probs.items()
        }
    return level_probs

#calculates expected pots contribution assuming you get to 'level+result' that is less than target level
def induction_step(level_probs, expected_pots, level, result):
    return level_probs[level][result-1]*(expected_pots[level+result]+1)

#induction_solver calculates the expected pots contribution from all possible growth pot outcomes
def induction_solver(level_probs, expected_pots, level, forward):
    #can only get 10 levels from growth pot
    if forward>10:
        forward = 10

    #expected pots of not getting target directly
    expected = induction_step(level_probs, expected_pots, level, 1)
    for i in range(2,forward+1):
        expected += induction_step(level_probs, expected_pots, level, i)

    #direct is the chance to get to the target level with one potion
    direct = sum(level_probs[level][forward:])
    return expected+direct

#finds the expected number of growth pots using induction solver
def calc_probs(start_level, target_level, level_probs, return_last=True):
    expected_pots = {}
    for i in range(target_level-1, start_level-1, -1):
        if i == target_level-1:
            expected_pots[i] = 1
        else:
            expected_pots[i] = induction_solver(level_probs, expected_pots, i, target_level-1-i)

    expected_pots = {k: round(v, 6) for k, v in expected_pots.items()}
    if return_last:
        return expected_pots[start_level]
    else:
        return expected_pots

#example usage

level_probs = load_probs()
start_level = 169
target_level = 194
print(calc_probs(170, 'a', level_probs))