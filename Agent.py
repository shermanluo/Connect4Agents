class Agent:
	depth = 10
	def Agent():
		return 

class MinimaxAgent(Agent):
	def value(self, gameState, player, depth):
		#Tie Game
		if gameState.isWin() and gameState.isLose():
			return (0, None)
		if depth == -1:
			return (self.evaluationFunction(gameState), None)
		if gameState.isWin():
			return (1000, None)
		if gameState.isLose():
			return (-1000, None)
		if player == 1:
			return self.maxValue(gameState, 1, depth - 1)
		else:
			return self.minValue(gameState, 2, depth - 1)

	def maxValue(self, gameState, player, depth):
		v = (-100000000, None)
		for action in gameState.getLegalActions(player):
			nxt = gameState.getSuccessor(player, action)
			val = self.value(nxt, 2, depth)[0]
			if val > v[0]:
				v = (val, action)
			if v[0] > 0:
				return v
		return v
	def minValue(self, gameState, player, depth):
		v = (100000000, None)
		for action in gameState.getLegalActions(player):
			nxt = gameState.getSuccessor(player, action)
			val = self.value(nxt, 1, depth)[0]
			if val < v[0]:
				v = (val, action)
			if v[0] < 0:
				return v
		return v

	def getAction(self, gameState, player):
		t = self.value(gameState, player, self.depth)
		print(player, t[0])
		return t[1]
		
	def evaluationFunction(self, gameState):
		return 0 
