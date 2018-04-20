#!/usr/bin/env python

#from max_diff_valsV2 import print_max_diff_vals
import m2
from divegame import diveGame
import pdb
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
    m = [2,0,9,1,4,5,2,6,1,7,5,0]
    iterm = iter(m)
    while actions:
        print("SCORE: ", score)
        scores.append(score)
        [print(str(a) + ": " + str(b)) for a, b in enumerate(actions)]
        i = next(iterm)
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
def printActions(gameState, actions):
    aIter = iter(actions)
    curr = ''
    while True:
        action = next(aIter, None)
        if not action:
            curr += "|DIED"
            print(curr)
            return
        elif action[2] == "exit":
            curr += "|EXIT"
            print(curr)
            return
        elif action in {(0,0, "move"),(0,5, "move"),(0,9, "move")}:
            if action == (0,0, "move"):
                drop = "Top Left"
            elif action == (0, 5, "move"):
                drop = "Top Middle"
            elif action == (0, 9, "move"):
                drop = "Top Right"
            curr += "|" + drop
        elif action[2] == "tank":
            curr += "|tank: " + str(action[1])
        else:
            curr += "|" + str(gameState.board[action[0]][action[1]])

def getActions(state, depth, num_iters, nodes):
    if state.isOver():
        s = m2.State()
        s.gs = state
        node = m2.Node(s)
        node.reward = s.gs.cash
        nodes[s] = node
        return state.cash, []
    bestScore = 0
    bestActions = []
    NA = []
    for i in state.getLegalActions():
        nxt = state.getSuccessor(i)
        states, rollout, scores, node = m2.getRollout(nxt[0], num_iters, nodes)
        value = scores[-1]
        NA.append((node, i))
        if value >= bestScore:
            bestActions = [i] + rollout
            bestScore = value
    return bestScore, bestActions, NA




def main():
    game = diveGame()
    human_rollout, rewards, humanscores = getHumanRollout(game, getscore = True)
    # #printActions(game, getActions(game, qvalues))
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
        #pdb.set_trace()
        #rhscore, hractions = getActions(state.getSuccessor(human_action)[0], 0, 50000)
        s = m2.State()
        s.gs = state
        nodes = {}
        rscore, ractions, NA = getActions(state, 1, 50000, nodes)
        humanNode = [x for x, y in NA if y == human_action][0]
        rhscore = humanNode.reward
        print(index, "| BestAction", ractions[0], "estimated Qvalue: ", formatScore(rscore), "humanAction", human_action,
            "estimated Qvalue: ", formatScore(rhscore))
        diff = rscore - rhscore
        if diff > maxDiff and human_action != ractions[0]:
            maxDiff = diff
            maxAction = ractions[0]
            maxIndex = index
        index += 1

    state, human_action = human_rollout[maxIndex]
    print("Fatal Flaw state")
    state.printBoard()
    print()
    print("There was a fatal flaw at action index", maxIndex)
    print()
    print("You took: ", human_action, "with a to-come score of ", formatScore(getToComeScore(rewards, maxIndex)))
    # print("Your actions starting at fatal flaw:")
    # printActions(state, [s[1] for s in human_rollout[maxIndex : -1]])
    # print()
    # print("You should have taken: ", maxAction, "with a possible to-come score of ", formatScore(qvalues[state, maxAction]))
    # print("Optimal actions starting at fatal flaw, starting with corrected action:")
    # rR, rA, rS = getActions(state, qvalues)
    # printActions(state, rA)
    # hR = [x[0] for x in human_rollout][maxIndex:]
    # hS = [score - humanscores[maxIndex] for score in humanscores][maxIndex:]
    # print()
    # print("Starting Fatal Flaw state")
    # state.printBoard()
    # k2Agent = MaxAgent(depth=2)
    # valuefn = lambda s: k2Agent.value(s)[0]
    # print_max_diff_vals(rR, hR, valuefn, rS, hS)




    

if __name__ == "__main__":
    main()
