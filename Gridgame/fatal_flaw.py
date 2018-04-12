#!/usr/bin/env python

from interestingBoards import findInterestingBoards
from Agent import QSolveAgent, MaxAgent
from max_diff_valsV2 import print_max_diff_vals
from gridGame import gridGame
#returns state, action rollout. Last action will be None
def formatScore(score):
    return format(score, '.2f')
def getHumanRollout(game, getscore = False):
    rollout = []
    rewards = []
    scores = []
    actions = game.getLegalActions()
    score = 0
    game.printBoard()
    while actions:
        print("SCORE: ", score)
        scores.append(score)
        print([str(a) + ": " + str(b) for a, b in enumerate(actions)])
        i = int(input())
        rollout.append((game, actions[i]))
        nxt = game.getSuccessor(actions[i])
        game = nxt[0]
        score += nxt[1]
        rewards.append(nxt[1])
        actions = game.getLegalActions()
        game.printBoard()
    rollout.append((game, None))
    print("SCORE: ", score)
    scores.append(score)
    return rollout, rewards, scores 
def getToComeScore(rewards, index):
    return sum(rewards[index:])
def getActions(gameState, Qvalues):
    rollout = []
    scores = []
    states = []
    states.append(gameState)
    score = 0
    scores.append(score)
    while gameState.getLegalActions():
        actions = gameState.getLegalActions()
        bestAction = max(actions, key = lambda x: Qvalues[(gameState, x)])
        rollout.append(bestAction)
        nxt = gameState.getSuccessor(bestAction)
        gameState = nxt[0]
        score += nxt[1]
        scores.append(score)
        states.append(gameState)
    return states, rollout, scores
def printActions(gameState, actions):
    aIter = iter(actions)
    curr = ''
    curr += 'Collect: '
    while True:
        action = next(aIter, None)
        if not action:
            print(curr[:-7])
            return
        if action in {(0,0),(0,9),(9,0),(9,9)}:
            if action == (0,0):
                drop = "Top Left"
            elif action == (0, 9):
                drop = "Top Right"
            elif action == (9, 9):
                drop = "Bottom Right"
            else:
                drop = "Bottom Left"
            curr += "Drop: " + drop + ', '
            curr += "Get: "
        else:
            curr += str(gameState.board[action[0]][action[1]]) + ", "

def main():
    game = gridGame(3,     [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 26, 0, 0, 0, 0, 26, 0],
                                         [0, 38, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 28, 0, 0]],
                                  double=(9,0), playerLoc=(0,0))
    #game = findInterestingBoards(threshold=10, n_boards=1, numpieces = 4)[0]
    human_rollout, rewards, humanscores = getHumanRollout(game, getscore = True)
    qagent = QSolveAgent()
    qagent.value(game)
    qvalues = qagent.Qvalues
    #printActions(game, getActions(game, qvalues))
    print()
    print()
    print("Your Actions:")
    printActions(game, [s[1] for s in human_rollout[:-1]])
    print("Your score: ", getToComeScore(rewards, 0))
    print()

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
        print(index, "| BestAction", bestAction, "Qvalue: ", formatScore(qvalues[(state, bestAction)]), "humanAction", human_action,
            "Qvalue: ", formatScore(qvalues[(state, human_action)]))
        if diff > maxDiff:
            maxDiff = diff
            maxAction = bestAction
            maxIndex = index
        index += 1
    # for i in range(maxIndex):
    #     state, human_action = human_rollout[i]
    #     state.printBoard()
    #     print("taken: ", human_action)
    print()
    state, human_action = human_rollout[maxIndex]
    print("Fatal Flaw state")
    state.printBoard()
    print()
    print("There was a fatal flaw at action index", maxIndex)
    print()
    print("You took: ", human_action, "with a to-come score of ", formatScore(getToComeScore(rewards, maxIndex)))
    print("Your actions starting at fatal flaw:")
    printActions(state, [s[1] for s in human_rollout[maxIndex : -1]])
    print()
    print("You should have taken: ", maxAction, "with a possible to-come score of ", formatScore(qvalues[state, maxAction]))
    print("Optimal actions starting at fatal flaw, starting with corrected action:")
    rR, rA, rS = getActions(state, qvalues)
    printActions(state, rA)
    hR = [x[0] for x in human_rollout][maxIndex:]
    hS = [score - humanscores[maxIndex] for score in humanscores][maxIndex:]
    print()
    print("Starting Fatal Flaw state")
    state.printBoard()
    k2Agent = MaxAgent(depth=2)
    valuefn = lambda s: k2Agent.value(s)[0]
    print_max_diff_vals(rR, hR, valuefn, rS, hS)




    

if __name__ == "__main__":
    main()
