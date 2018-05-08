#!/usr/bin/env python


from m2 import getRollout
import pickle
import math
from rolloutvisual import visualize
from fatal_flaw import printActions
from Agent import MaxAgent
import pdb

f = open('store.pckl', 'rb')
rR, rS, hR, hS, rA, hA = pickle.load(f)

def smExplain(states, actions):
    data = []
    for i in range(len(states) - 1):
        print(i)
        state = states[i]
        takenAction = actions[i]
        takenActionValue = None
        values = []
        possibleActions = state.getLegalActions()
        idxTaken = [x for x, y in enumerate(possibleActions) if y == takenAction][0]
        for action in possibleActions:
            print(action)
            if not (action[2] == "exit" and takenAction == "exit"):
                nxt = state.getSuccessor(action)[0]
                __, __, scores, __ = getRollout(nxt, 50000)
                value = scores[-1]
                values.append(value)
        data.append((idxTaken, values))
    f = open('data.pckl', 'wb')
    pickle.dump(data, f)
    f.close()
    print(data)

def smExplainGreedy(states, actions):
    data = []
    kagent = MaxAgent(depth=3)
    value_fn = lambda s: kagent.value(s)[0]
    for i in range(len(states) - 1):
        state = states[i]
        takenAction = actions[i]
        takenActionValue = None
        values = []
        possibleActions = state.getLegalActions()
        idxTaken = [x for x, y in enumerate(possibleActions) if y == takenAction][0]
        for action in possibleActions:
            if not (action[2] == "exit" and takenAction == "exit"):
                nxt = state.getSuccessor(action)
                values.append(value_fn(nxt[0]) + nxt[1])
        data.append((idxTaken, values))
    f = open('data.pckl', 'wb')
    pickle.dump(data, f)
    f.close()
    #print(data)

# def smExplain(states, actions):
#   results = []
#   for i in range(len(states) - 1):
#       print(i)
#       state = states[i]
#       takenAction = actions[i]
#       takenActionValue = None
#       total = 0
#       actionValues = []


#       possibleActions = state.getLegalActions()
#       #pdb.set_trace()
#       idxTaken = [x for x, y in enumerate(possibleActions) if y == takenAction][0]

        
#       nxt_states = [state.getSuccessor(i) for i in possibleActions]
#       pool = Parallel(n_jobs=len(nxt_states))
#       results = pool(delayed(m2.getRollout)(nxt[0], 50) for nxt in nxt_states)




#       values = [scores[-1] for _,_,scores,_ in results]

#       results.append((idxTaken, values))


#   print(results)
#smExplain(rR, rA)



NUM_TRIES = 4
THRESHOLD = 0.95
def calculateProbability(start, end, pathProbs):
    prob = 1
    for i in range(start, end - 1):
        prob *= pathProbs[i]
    return 1 - pow(1 - prob, NUM_TRIES)

def findStates():
    f = open('data.pckl', 'rb')
    data = pickle.load(f)
    results = []
    for idx, vector in data:
        value = pow(2, 0.04 * vector[idx])
        results.append(value / sum([pow(2, 0.04 * x) for x in vector]))
    idx = [x for x in range(len(data) + 1)]
    print("action probabilities", [format(i, ".2f") for i in results])
    start = 0
    end = 1
    idxs = [0]
    #pdb.set_trace()
    while end <= len(results):
        prob = calculateProbability(start, end, results)
        while prob >= THRESHOLD:
            if end == len(results):
                idxs.append(end)
                return idxs
            end += 1
            prob = calculateProbability(start, end, results)
        idxs.append(end - 1)
        start = end - 1
    idxs.append(end)
    return idxs


idxs = findStates()
print("State Indices", idxs)
visualize([rR[i] for i in idxs], printActions(rR[0], rA))
    

