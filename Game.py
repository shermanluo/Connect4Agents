

from Agent import MinimaxAgent, MinimaxAgentDiscount, RandomAgent, HelperMinimaxAgentDiscount, HeatAgentDiscount, HeatAgentDiscountHelper
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
				action = agent2.getAction(self.gameState, 2)
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


	def assistedPlay(self, agentEnemy, agentHelp):
		player = 1
		count = 0
		while True:
			print('CURRENTBOARD')
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
				recommended = agentHelp.getAction(self.gameState, 2)
				print("RECOMMENDED:", recommended)
				action = int(input())				
				self.gameState = self.gameState.getSuccessor(2, action)
				player = 1
			else:
				action = agentEnemy.getAction(self.gameState, 1)
				self.gameState = self.gameState.getSuccessor(1, action)
				player = 2


game = Game()
#game.humanPlay(MinimaxAgent(7)) #Play against a optimal agent
#game.humanPlay(MinimaxAgentDiscount(5)) #Play against a optimal agent that tries to win quickly
#game.play(MinimaxAgentDiscount(5), MinimaxAgentDiscount(6)) #P1 tries to win as quickly as possible, P2 tries to delay loss for as long as possible
#game.play(MinimaxAgent(6), MinimaxAgentDiscount(6)) #P1 tries to win, P2 tries to delay as long as possible assuming P1 tries to win as quickly as possible
#game.assistedPlay(MinimaxAgent(5), HelperMinimaxAgentDiscount(6)) #HELPER AGENT HELPS U PLAY. HELPER AGENT IS SLIGHTLY MORE OPTIMAL THAN ADVERSIAL (MORE DEPTH)
#game.humanPlay(HeatAgentDiscount(7, 0.8, 0.8))
game.assistedPlay(HeatAgentDiscount(7, 1.5, 0.7), HeatAgentDiscountHelper(7, 2, 0.7))
#game.play(HeatAgentDiscount(7, 1, 0.7), HeatAgentDiscount(7, 1, 0.7))
#game.play(HeatAgentDiscount(4, 2, 0.7), HeatAgentDiscount(8, 2, 0.7))