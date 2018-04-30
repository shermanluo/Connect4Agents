#!/usr/bin/env python

from Agent import MaxAgent

# def find_max_diff_vals_idx(optimal_rollout, human_rollout, optimal_scores, human_scores, min_t, min_y, value_fn):
    


# def print_max_diff_vals(optimal_rollout, human_rollout, value_fn, \
#                         optimal_scores, human_scores):

def scoresToRewards(scores):
    rewards = []
    i = iter(scores)
    assert len(scores) > 1
    elem = next(i)
    while(True):
        try:
            nxt = next(i)
        except:
            break
        rewards.append(nxt - elem)
        elem = nxt
    assert(len(scores) == len(rewards) + 1)
    return rewards

def idxklargest(rewards, k):
    rewards = rewards[:]
    copy1 = rewards[:]
    copy = rewards[:]
    largest = []
    answer = []
    assert len(rewards) >= k
    for i in range(k):
        big = max(rewards)
        rewards.remove(big)
        largest.append(big)
    largest = [x for x in largest if x > 0]
    for large in largest:
        locations = [i for i, j in enumerate(copy) if j == large]
        for loc in locations:
            if loc not in answer:
                answer.append(loc)
                break
    return answer

def plus1(idxs):
    copy = idxs[:]
    for i in copy:
        if i + 1 not in idxs:
            idxs.append(i + 1)
    return sorted(idxs)

def explain(states, scores):
    rewards = scoresToRewards(scores)
    print("scores", scores)
    print("rewards", rewards)
    idxs = idxklargest(rewards, 3)
    print(idxs)
    idxs = plus1(idxs)
    print(idxs)
    for i in idxs:
        states[i].printBoard()
        print()

