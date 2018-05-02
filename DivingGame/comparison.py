#!/usr/bin/env python

from Agent import MaxAgent
from rolloutvisual import visualize

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
    return idxs


def helpLarger(rewards, mini):
    return max([x for x,y in [_ for _ in enumerate(rewards)][mini:]], key = lambda x: rewards[x])










def explainKgreatestPlus1(states, scores, info): #finds the indices of the largest K rewards and unions the set of indices + 1, and also start and end states
    rewards = scoresToRewards(scores)
    idxs = idxklargest(rewards, 3)
    idxs = plus1(idxs)
    if 0 not in idxs:
        idxs.append(0)
    if len(states) - 1 not in idxs:
        idxs.append(len(states) - 1)
    idxs = sorted(idxs)
    print("KgreatestPlus1", idxs)
    visualize([states[i] for i in idxs], info)
    

def explainKgreatest(states, scores, info): #finds the indices of the largest K rewards, and also start and end states
    rewards = scoresToRewards(scores)
    idxs = idxklargest(rewards, 3)
    if 0 not in idxs:
        idxs.append(0)
    if len(states) - 1 not in idxs:
        idxs.append(len(states) - 1)
    idxs = sorted(idxs)
    print("Kgreatest", idxs)
    visualize([states[i] for i in idxs], info)



def explainIncreasinglyLargePlus1(states, scores, info):
    rewards = scoresToRewards(scores)
    minI = 0
    idxs = []
    while minI < len(rewards):
        idxs.append(minI)
        minI = helpLarger(rewards, minI) + 1
        if minI == len(rewards) - 1:
            idxs.append(minI)
            break
    idxs = plus1(idxs)
    idxs = sorted(idxs)
    if idxs[:-1] == len(states):
        idxs = idxs[::-1]
    print("forwardLargestPlus1", idxs)
    visualize([states[i] for i in idxs], info)


def explainIncreasinglyLarge(states, scores, info):
    rewards = scoresToRewards(scores)
    minI = 0
    idxs = []
    while minI < len(rewards):
        idxs.append(minI)
        minI = helpLarger(rewards, minI) + 1
        if minI == len(rewards) - 1:
            idxs.append(minI)
            break
    print("forwardLargest", idxs)
    visualize([states[i] for i in idxs], info)

def skip2(states, scores, info): #Show every other state
    idxs = [i for i in range(len(states))][::2]
    print("skip2",idxs)
    visualize([states[i] for i in idxs], info)

