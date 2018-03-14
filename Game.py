

from Agent import MinimaxAgent, MinimaxAgentDiscount, RandomAgent, HelperMinimaxAgentDiscount, HeatAgentDiscount, HeatAgentDiscountHelper,HeatAgentDiscountHelperIntermediate
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
	def flip(self, player):
		if player == 1:
			return 2
		if player == 2:
			return 1

	def humanPlay(self, agent1, humanPlayerNum):
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

			if player == humanPlayerNum:
				action = int(input())				
				self.gameState = self.gameState.getSuccessor(player, action)
				player = self.flip(player)
			else:
				action = agent1.getAction(self.gameState, player)
				self.gameState = self.gameState.getSuccessor(player, action)
				player = self.flip(player)


	def assistedPlay(self, agentEnemy, agentHelp, humanPlayerNum):
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

			if player == humanPlayerNum:
				recommended = agentHelp.getAction(self.gameState, player)
				print("RECOMMENDED:", recommended)
				action = int(input())				
				self.gameState = self.gameState.getSuccessor(player, action)
				player = self.flip(player)
			else:
				action = agentEnemy.getAction(self.gameState, player)
				self.gameState = self.gameState.getSuccessor(player, action)
				player = self.flip(player)

def testPredictions(agent, gameState, player):
	gameState.printBoard()
	recommended = agent.getAction(gameState, player)
	print("RECOMMENDED: ", recommended)


game = Game()
#game.humanPlay(MinimaxAgent(20), 1) #Play against a optimal agent
#game.humanPlay(MinimaxAgentDiscount(20), 1) #Play against a optimal agent that tries to win quickly
#game.play(MinimaxAgentDiscount(5), MinimaxAgentDiscount(6)) #P1 tries to win as quickly as possible, P2 tries to delay loss for as long as possible
#game.play(MinimaxAgent(6), MinimaxAgentDiscount(6)) #P1 tries to win, P2 tries to delay as long as possible assuming P1 tries to win as quickly as possible
#game.assistedPlay(MinimaxAgent(5), HelperMinimaxAgentDiscount(6)) #HELPER AGENT HELPS U PLAY. HELPER AGENT IS SLIGHTLY MORE OPTIMAL THAN ADVERSIAL (MORE DEPTH)
#game.humanPlay(HeatAgentDiscountHelper(9, 1, .9), 1)
#game.humanPlay(HeatAgentDiscount(9, 1, .9), 1)
#game.assistedPlay(HeatAgentDiscount(5, 1.5, 0.99), HeatAgentDiscountHelper(5, 2, 0.99), 1)
#game.play(HeatAgentDiscount(7, 1, 0.7), HeatAgentDiscount(7, 1, 0.7))

#testGS = connectThreeGS([[],[],[1],[]])
#testPredictions(HeatAgentDiscountHelper(10, 2, 0.8), testGS, 2)
#testPredictions(HelperMinimaxAgentDiscount(10, 0.9), testGS, 2)

testGS = connectThreeGS([[2],[1],[2],[1, 1, 2]])
testPredictions(HeatAgentDiscountHelperIntermediate(4, 1.5, 0.99), testGS, 1)