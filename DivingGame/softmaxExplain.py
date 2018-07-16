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

def smExplain(states, actions): #Qvalues
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

def smExplainGreedy(states, actions): #K=3 evaluations of actions
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
    f = open('kdata.pckl', 'wb')
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
smExplainGreedy(rR, rA)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


NUM_TRIES = 4
THRESHOLD = 0.95

kagent = MaxAgent(depth=3)
value_fn = lambda s: kagent.value(s)[0]
#THIS FUNCTION RETURNS THE PROBABILITY OF TAKING A PATH. CURRENTLY A HYBRID BETWEEN K3 and Q
#THIS FUNCTION IS USED TO CALCULATE THE PROBABILITY OF ONE OF THE ALTERNATE PATHS
def pathProb(path):
    prob = 1
    for i in range(len(path)):
        state = path[i]
        if not state.getLegalActions():
            return prob
        total = 0
        ktotal = 0
        for action in state.getLegalActions():
            nxt = state.getSuccessor(action)
            __, __, scores, __ = getRollout(nxt[0], 50000)
            score = scores[:-1]
            kscore = value_fn(nxt[0]) + nxt[1]
            total += pow(math.e, 0.04 * score)
            ktotal += pow(math.e, 0.1 * kscore)
            if nxt == path[i + 1]:
                takenScore = pow(math.e, 0.04 * score)
                ktakenScore = pow(math.e, 0.1 * kscore)
        prob *= 0.33 * takenScore / total + 0.67 * ktakenScore / ktotal 
        
#calculate the probability of inferring between start and end
def calculateProbability(start, end, pathProbs): #pathprobs is an array of the probabilities of each action. start and end are indices
    allPaths = findPaths(rR[start], rR[end], end - start)
    allPaths = [x for x in allPaths if x != rR[start:end + 1]] #trim off the actual path explored
    P = 1
    for i in range(start, end - 1):
        P *= pathProbs[i]
    Q = 0
    for path in allPaths:
        Q += pathProb(path)
    total = 0
    for i in range(0, NUM_TRIES):
        total += pow(1 - P - Q, i) * P
    return total

#Finds all paths from start to end with a certain length
def findPaths(start, end, length):
    def findPathsUtil(path, depth):
        if depth == 0 and path[-1] == end:
            return [path]
        if depth == 0 and path[-1] != end:
            return []
        node = path[-1]
        ret = []
        for action in node.getLegalActions():
            nxt = node.getSuccessor(action)[0]
            found = findPathsUtil(path + [nxt], depth - 1)
            ret += found
        return ret  
    return findPathsUtil([start], length)


#Master function that finds the indices of the states to be shown.
def findStates():
    f = open('data.pckl', 'rb')
    data = pickle.load(f)
    f = open('kdata.pckl', 'rb')
    kdata = pickle.load(f)
    results = [] #results is a list of the probabilities of each action in the rollout
    for idx, vector in data:
        qvalue = pow(math.e, 0.04 * vector[idx])
        results.append(0.33 * (qvalue / sum([pow(math.e, 0.04 * x) for x in vector])))

    kresults = []
    for idx, vector in kdata:
        kvalue = pow(math.e, 0.1 * vector[idx])
        kresults.append(0.67 * (kvalue / sum([pow(math.e, 0.1 * x) for x in vector])))
    for i in range(len(results)):
        results[i] += kresults[i]
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
    

