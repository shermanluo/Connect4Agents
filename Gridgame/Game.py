

from Agent import MaxAgent, QSolveAgent
from gridGame import gridGame
import itertools

def euclidDist(A, B):
    return pow(pow(A[0] - B[0], 2) + pow(A[1] - B[1], 2), 0.5)
class Game: 

    def __init__(self):
        self.gameState = gridGame(4,        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 14, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 15, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 20, 0, 0],
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

    def agentSolve(self, return_score=False):
        agent = QSolveAgent()
        agent.value(self.gameState)
        if return_score:
            return agent.Qvalues, agent.scores
        return agent.Qvalues

    def exploreTree(self):
        Qvalues = self.agentSolve()
        stack = []
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

    def jsonSearchTree(self, output_fname="gridgame_qvals.json"):
        # Generate search tree in json format, for visualization
        import json
        Qvalues, scores = self.agentSolve(return_score=True)

        tree = {}
        start = self.gameState
        tree["user_id"] = "\n".join([" ".join(x) \
                                     for x in start.printBoard(print_to_screen=False)])
        tree["name"] = tree["user_id"]
        tree["children"] = []

        stack = [(start, tree)]
        curr = self.gameState
        while len(stack) > 0:
            curr, curr_tree = stack.pop()
            actions = curr.getLegalActions()
            if not actions:
                continue
            for action in actions:
                child = curr.getSuccessor(action)[0]
                child_tree = {}
                child_tree["user_id"] = \
                        "\n".join([" ".join(x)
                                   for x in child.printBoard(print_to_screen=False)])
                prefix = "Place at "
                if not curr.holding:
                    val = curr.board[action[0]][action[1]]
                    prefix = "Pick up " + str(val) + " at "
                child_tree["name"] = prefix + str(action) + ": " + \
                                     format(Qvalues[(curr, action)], '.2f') + \
                                     " [Score: " + \
                                     format(scores[(curr, action)], '.2f') + "]"
                child_tree["children"] = []

                curr_tree["children"].append(child_tree)
                stack.append((child, child_tree))

        with open(output_fname, 'w') as outfile:
            json.dump(tree, outfile, indent=2)
            

game = Game()
game.jsonSearchTree()  # generates json file for visualization purposes
#game.exploreTree()
