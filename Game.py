

from Agent import MinimaxAgent 
from gameState import connectThreeGS
class Game: 

	def __init__(self):
		self.gameState = connectThreeGS([[],[],[],[]])


	def play(self, agent1, agent2):
		player = 1
		count = 0
		while True:
			self.gameState.printBoard()
			print()
			if self.gameState.isWin() and self.gameState.isLose():
				print("Tie!")
				return 3
			if self.gameState.isWin():
				print("Player 1 Wins!")
				return 1
			if self.gameState.isLose():
				print("Player 2 Wins!")
				return 2

			if player == 1:
				action = agent1.getAction(self.gameState, 1)
				self.gameState = self.gameState.getSuccessor(1, action)
				player = 2
			else:
				action = agent1.getAction(self.gameState, 2)
				self.gameState = self.gameState.getSuccessor(2, action)
				player = 1

	def humanPlay(self, agent1):
		player = 1
		count = 0
		while True:
			self.gameState.printBoard()
			print()
			if self.gameState.isWin() and self.gameState.isLose():
				print("Tie!")
				return 3
			if self.gameState.isWin():
				print("Player 1 Wins!")
				return 1
			if self.gameState.isLose():
				print("Player 2 Wins!")
				return 2

			if player == 2:
				action = int(input())				
				self.gameState = self.gameState.getSuccessor(2, action)
				player = 1
			else:
				action = agent1.getAction(self.gameState, 1)
				self.gameState = self.gameState.getSuccessor(1, action)
				player = 2


game = Game()
game.humanPlay(MinimaxAgent())
#game.play(MinimaxAgent(), MinimaxAgent())
