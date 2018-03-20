

from Agent import MaxAgent
from gridGame import gridGame
class Game: 

	def __init__(self):
		self.gameState = gridGame(		[[0, 1000, 0, 0, 0, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
										 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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


game = Game()
game.agentPlay()