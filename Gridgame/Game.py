

from Agent import MaxAgent, QSolveAgent
from gridGame import gridGame
import itertools
class Game: 

	def __init__(self):
		self.gameState = gridGame(4,		[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 14, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										 [0, 0, 0, 15, 0, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 0, 0, 10, 20, 0, 0],
										 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 15, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

	def humanPlay(self):
		reward = 0
		while True:
			self.gameState.printBoard()
			print("Reward: ", reward)
			if self.gameState.isOver():
				return
		
			a = int(input())
			b = int(input())				
			nxt = self.gameState.getSuccessor((a, b))
			self.gameState = nxt[0]
			reward += nxt[1]
	def agentPlay(self):
		reward = 0
		agent = MaxAgent()
		actions = agent.value(self.gameState)[1]
		while True:
			self.gameState.printBoard()
			print("Reward: ", reward)
			if self.gameState.isOver():
				return
			action = actions.pop(0)
			nxt = self.gameState.getSuccessor(action)
			self.gameState = nxt[0]
			reward += nxt[1]

	def agentSolve(self):
		agent = QSolveAgent()
		agent.value(self.gameState)
		print(agent.Qvalues)
		print(len(agent.Qvalues))

	# def solve(self):
	# 	pieces = self.gameState.getPiecesandLocations()
	# 	gs = {}
	# 	initialGS1 = gridGame(0, [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], None, (0,0), (0,0))
	# 	initialGS2 = gridGame(0, [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], None, (0,0), (9,0))
	# 	initialGS3 = gridGame(0, [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], None, (0,0), (0,9))
	# 	initialGS4 = gridGame(0, [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 									 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], None, (0,0), (9,9))
	# 	gs[initialGS4] = 0
	# 	gs[initialGS3] = 0
	# 	gs[initialGS2] = 0
	# 	gs[initialGS1] = 0




game = Game()
game.agentSolve()