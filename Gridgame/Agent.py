import random
from math import e

class Agent:
	depth = 10
	def Agent():
		return 


class MaxAgent(Agent):
	def __init__(self, depth = 10, discount = 1):
		self.depth = depth
		self.discount = discount

	def value(self, gameState):
		#Tie Game
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

		
	def evaluationFunction(self, gameState):
		return 0


