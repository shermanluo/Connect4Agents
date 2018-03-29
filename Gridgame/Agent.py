import random
from math import e

class Agent:
    depth = 10
    def Agent():
        return 

class K1GreedyAgent(Agent):
    def __init__(self):
        pass
    def getAction(self, gameState):
        return max([action for action in gameState.getLegalActions()], key = lambda x: gameState.getSuccessor(x)[1])

class MaxAgent(Agent):
    def __init__(self, depth = 10, discount = 1):
        self.depth = depth
        self.discount = discount

    def value(self, gameState):
        if gameState.isOver():
            return (0, [])
        possib = []
        for action in gameState.getLegalActions():
            nxt = gameState.getSuccessor(action)
            temp = self.value(nxt[0])
            value = nxt[1] + temp[0]
            actions = temp[1][:]
            actions.insert(0, action)
            possib.append((value, actions))
        return max(possib, key = lambda x: x[0])

class QSolveAgent(Agent):
    def __init__(self, depth = 10, discount = 1):
        self.Qvalues = {}
        self.scores = {}
        self.rewards = {}
        self.depth = depth
        self.discount = discount

    def value(self, gameState, score=0):
        if gameState.isOver():
            self.scores[gameState] = score
            return (None, 0) 
        values = set()
        for action in gameState.getLegalActions():
            nxt = gameState.getSuccessor(action) #nxt[1] is reward
            temp = self.value(nxt[0], score + nxt[1])
            value = nxt[1] + temp[1]
            self.Qvalues[(gameState, action)] = value
            self.scores[(gameState, action)] = score + nxt[1]
            self.rewards[(gameState, action)] = nxt[1]
            values.add((action, value))
        return max(values, key = lambda x: x[1])
        
    def evaluationFunction(self, gameState):
        return 0


