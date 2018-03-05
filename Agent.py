import random

class Agent:
	depth = 10
	def Agent():
		return 

discount = 0.9

class MinimaxAgent(Agent):
	def __init__(self, depth = 10):
		self.depth = depth

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
		return t[1]
		
	def evaluationFunction(self, gameState):
		return 0 



class MinimaxAgentDiscount(Agent):
	def __init__(self, depth = 10):
		self.depth = depth

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
			val = self.value(nxt, 2, depth)[0] * discount
			if val > v[0]:
				v = (val, action)
		return v
	def minValue(self, gameState, player, depth):
		v = (100000000, None)
		for action in gameState.getLegalActions(player):
			nxt = gameState.getSuccessor(player, action) 
			val = self.value(nxt, 1, depth)[0] * discount
			if val < v[0]:
				v = (val, action)
		return v

	def getAction(self, gameState, player):
		t = self.value(gameState, player, self.depth)
		return t[1]
		
	def evaluationFunction(self, gameState):
		return 0

class HelperMinimaxAgentDiscount(Agent):
	def __init__(self, depth = 10):
		self.depth = depth

	def value(self, gameState, player, depth):
		#Tie Game
		if gameState.isWin() and gameState.isLose():
			return (0, None, gameState)
		if depth == -1:
			return (self.evaluationFunction(gameState), None, gameState)
		if gameState.isWin():
			return (1000, None, gameState)
		if gameState.isLose():
			return (-1000, None, gameState)
		if player == 1:
			return self.maxValue(gameState, 1, depth - 1)
		else:
			return self.minValue(gameState, 2, depth - 1)

	def maxValue(self, gameState, player, depth):
		v = (-100000000, None)
		for action in gameState.getLegalActions(player):
			nxt = gameState.getSuccessor(player, action)
			value = self.value(nxt, 2, depth)
			if depth == self.depth - 1:
				print("MOVE: ", action, " PROBABLY LEADS TO:")
				if value[0] < 0:
					print("DANGER OF LOSING")
				if value[0] > 0:
					print("GUARANTEED WIN")
				value[2].printBoard()
				print()

			val = value[0] * discount
			if val > v[0]:
				v = (val, action, value[2])
		return v
	def minValue(self, gameState, player, depth):
		v = (100000000, None, None)
		for action in gameState.getLegalActions(player):
			nxt = gameState.getSuccessor(player, action) 
			value = self.value(nxt, 1, depth)
			if depth == self.depth - 1:
				print("MOVE: ", action, " PROBABLY LEADS TO:")
				if value[0] > 0:
					print("DANGER OF LOSING")
				if value[0] < 0:
					print("GUARANTEED WIN")
				value[2].printBoard()
				print()

			val = value[0] * discount
			if val < v[0]:
				v = (val, action, value[2])
		return v

	def getAction(self, gameState, player):
		t = self.value(gameState, player, self.depth)
		return t[1]
		
	def evaluationFunction(self, gameState):
		return 0





class HeatAgentDiscount(Agent):
	def __init__(self, depth = 10, alpha = 1, discount = 1):
		self.depth = depth
		self.alpha = alpha
		self.discount = discount

	def value(self, gameState, player, depth):
		#Tie Game
		if gameState.isWin() and gameState.isLose():
			return (0, None)
		if depth == -1:
			return (self.evaluationFunction(gameState), None)
		if gameState.isWin():
			return (5, None)
		if gameState.isLose():
			return (-5, None)
		if player == 1:
			return self.maxValue(gameState, 1, depth - 1)
		else:
			return self.minValue(gameState, 2, depth - 1)

	def maxValue(self, gameState, player, depth):
		totalValue = 0
		d = {}
		for action in gameState.getLegalActions(player):
			nxt = gameState.getSuccessor(player, action)
			val = self.value(nxt, 2, depth)[0] * self.discount
			totalValue += pow(2, self.alpha * val)
			d[action] = val
		r = random.uniform(0, 1)
		running = 0
		for key in d:
			running += pow(2, self.alpha * d[key]) / totalValue
			if r <= running:
				return (d[key], key)

	def minValue(self, gameState, player, depth):
		totalValue = 0
		d = {}
		for action in gameState.getLegalActions(player):
			nxt = gameState.getSuccessor(player, action) 
			val = self.value(nxt, 1, depth)[0] * self.discount
			totalValue += pow(2, self.alpha * val * -1)
			d[action] = val
		r = random.uniform(0, 1)
		running = 0
		for key in d:
			running += pow(2, self.alpha * d[key] * -1) / totalValue
			if r <= running:
				return (d[key], key)

	def getAction(self, gameState, player):
		t = self.value(gameState, player, self.depth)
		return t[1]
		
	def evaluationFunction(self, gameState):
		return 0

class HeatAgentDiscountHelper(Agent):
	def __init__(self, depth = 10, alpha = 1, discount = 1):
		self.depth = depth
		self.alpha = alpha
		self.discount = discount

	def value(self, gameState, player, depth):
		#Tie Game
		if gameState.isWin() and gameState.isLose():
			return (0, None, gameState)
		if depth == -1:
			return (self.evaluationFunction(gameState), None, gameState)
		if gameState.isWin():
			return (5, None, gameState)
		if gameState.isLose():
			return (-5, None, gameState)
		if player == 1:
			return self.maxValue(gameState, 1, depth - 1)
		else:
			return self.minValue(gameState, 2, depth - 1)

	def maxValue(self, gameState, player, depth):
		totalValue = 0
		d = {}
		g = {}
		for action in gameState.getLegalActions(player):
			nxt = gameState.getSuccessor(player, action)
			value = self.value(nxt, 2, depth)
			val = value[0] * self.discount
			if depth == self.depth - 1:
				print("MOVE: ", action, " PROBABLY LEADS TO:")
				value[2].printBoard()
				print()

			totalValue += pow(2, self.alpha * val)
			d[action] = val
			g[action] = value[2]
		if depth == self.depth - 1:
			x = max(d, key = lambda x: d[x])
			return (d[x], x, value[2])
		r = random.uniform(0, 1)
		running = 0
		for key in d:
			running += pow(2, self.alpha * d[key]) / totalValue
			if r <= running:
				return (d[key], key, g[key])

	def minValue(self, gameState, player, depth):
		totalValue = 0
		d = {}
		g = {}
		for action in gameState.getLegalActions(player):
			nxt = gameState.getSuccessor(player, action) 
			value = self.value(nxt, 2, depth)
			val = value[0] * self.discount
			if depth == self.depth - 1:
				print("MOVE: ", action, " PROBABLY LEADS TO:")
				value[2].printBoard()
				print()
			totalValue += pow(2, self.alpha * val * -1)
			d[action] = val
			g[action] = value[2]
		if depth == self.depth - 1:
			x = min(d, key = lambda x: d[x])
			return (d[x], x, value[2])
		r = random.uniform(0, 1)
		running = 0
		for key in d:
			running += pow(2, self.alpha * d[key] * -1) / totalValue
			if r <= running:
				return (d[key], key, g[key])

	def getAction(self, gameState, player):
		t = self.value(gameState, player, self.depth)
		return t[1]
		
	def evaluationFunction(self, gameState):
		return 0

class RandomAgent(Agent):
	def getAction(self, gameState, player):
		return random.choice(list(gameState.getLegalActions(player)))
