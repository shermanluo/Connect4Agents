#!/usr/bin/env python

from interestingBoards import findInterestingBoards
from Agent import QSolveAgent
#returns state, action rollout. Last action will be None
def getHumanRollout(game):
    rollout = []
    actions = game.getLegalActions()
    while actions:
        print("choose index of action")
        print(actions)
        i = int(input())
        rollout.append((game, actions[i]))
        game = game.getSuccessor(actions[i])[0]
        actions = game.getLegalActions()
        game.printBoard()
    rollout.append((game, None))
    return rollout

def main():
    game = findInterestingBoards(threshold=15, n_boards=1, numpieces = 3)[0]
    human_rollout = getHumanRollout(game)
    qagent = QSolveAgent()
    print("HI")
    qagent.value(game)
    qvalues = qagent.Qvalues


    maxAction = None
    maxDiff = 0
    maxIndex = 0
    index = 0
    for state, human_action in human_rollout:
        if human_action == None:
            break
        actions = state.getLegalActions()
        bestAction = max(actions, key = lambda x: qvalues[(state, x)])
        diff = qvalues[(state, bestAction)] - qvalues[(state, human_action)]
        print("index: ", index, "BestAction", bestAction, "Qvalue: ", qvalues[(state, bestAction)], "humanAction", human_action,
            "Qvalue: ", qvalues[(state, human_action)])
        if diff > maxDiff:
            maxDiff = diff
            maxAction = bestAction
            maxIndex = index
        index += 1
    for i in range(maxIndex):
        state, human_action = human_rollout[i]
        state.printBoard()
        print("taken: ", human_action)
    state, human_action = human_rollout[maxIndex]
    state.printBoard()
    print("index: ", maxIndex)
    print("taken: ", human_action, "Qvalue: ", qvalues[(state, human_action)])
    print("correction: ", maxAction, "Qvalue: ", qvalues[state, maxAction])


    

if __name__ == "__main__":
    main()
