

from Agent import MaxAgent, QSolveAgent
from gridGame import gridGame
import itertools
def euclidDist(A, B):
    return pow(pow(A[0] - B[0], 2) + pow(A[1] - B[1], 2), 0.5)
class Game: 

    def __init__(self):
        self.gameState = gridGame(4,        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 12, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 20, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 10, 0, 0, 0, 0, 6, 0, 0],
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
        return agent.Qvalues

    def exploreTree(self):
        Qvalues = self.agentSolve()
        stack = []   #stack keeps track of previous states
        start = self.gameState
        curr = self.gameState
        while True:
            print()
            curr.printBoard()
            if start == curr: 
                print("Start of game, don't type -1")
            if (curr.holding):
                print("Holding: ", curr.holding)
                print("Choose where to place it. To return to previous state, type -1.")
            else:
                print('Go pick up a piece!')
                print("Type the index of your action. To return to previous state, type -1.")
            actions = curr.getLegalActions()
            for i, action in enumerate(actions):
                print(i, action, "| Distance: ~", format(euclidDist(action, curr.playerLoc), '.2f'), "| QValue: ~", format(Qvalues[(curr, action)], '.2f'))
            if not actions:
                print("game is done!")

            request = input()
            if request == -2:
                return
            if int(request) == -1:
                curr = stack.pop()
                continue
            stack.append(curr)
            curr = curr.getSuccessor(actions[int(request)])[0]






game = Game()
game.exploreTree()