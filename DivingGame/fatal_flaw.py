#!/usr/bin/env python

#from max_diff_valsV2 import print_max_diff_vals
import m2
from divegame import diveGame
import pdb
from joblib import Parallel, delayed
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
def getSoFarScore(rewards, index):
    return sum(rewards[:index])
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

def getActions(state, depth, num_iters):
    if state.isOver():
        s = m2.State()
        s.gs = state
        node = m2.Node(s)
        node.reward = s.gs.cash
        return state.cash, []

    actions = state.getLegalActions()
    nxt_states = [state.getSuccessor(i) for i in actions]
    pool = Parallel(n_jobs=len(nxt_states))
    results = pool(delayed(m2.getRollout)(nxt[0], num_iters) for nxt in nxt_states)

    values = [scores[-1] for _,_,scores,_ in results]
    bestIdx = max(range(len(values)), key = lambda x: values[x])
    bestScore = values[bestIdx]
    assert bestScore == max(values)
    bestActions = [actions[bestIdx]] + results[bestIdx][1]
    NA = [(results[i][-1],actions[i]) for i in range(len(results))]

    return bestScore, bestActions, NA

def main():
    game = diveGame()
    human_rollout, rewards, humanscores = getHumanRollout(game, getscore = True)
    # #printActions(game, getActions(game, qvalues))
    print()
    print()
    print("Your Actions:")
    printActions(game, [s[1] for s in human_rollout[:-1]])
    finalScore = getToComeScore(rewards, 0)
    print("Your score: ", finalScore)
    print()

    maxAction = None
    maxDiff = 0
    maxIndex = 0
    index = 0
    Bhscore = 0
    Brscore = 0
    BrRollout = None
    assert humanscores[-1] == finalScore
    for state, human_action in human_rollout:
        sofar = getSoFarScore(rewards, index)
        if human_action == None:
            break
        #pdb.set_trace()
        #rhscore, hractions = getActions(state.getSuccessor(human_action)[0], 0, 50000)
        s = m2.State()
        s.gs = state
        rscore, ractions, NA = getActions(state, 1, 100000)
        humanNode = [x for x, y in NA if y == human_action][0]
        rhscore = max(humanNode.reward, finalScore)

        if finalScore <= rscore:
            print(index, "| BestAction", ractions[0], "~best score: ", formatScore(rscore), "| humanAction", human_action,"~best score: ", formatScore(rhscore))
        else:
            rscore = finalScore
            ractions = [s[1] for s in human_rollout[index:]]
            print("uh oh, human's score is better than our best estimate!!!")
            print(index, "| BestAction", ractions[0], "~best score: ", formatScore(rscore), "| humanAction", human_action,
            "~best score: ", formatScore(rhscore))
        diff = rscore - rhscore
        if diff > maxDiff and human_action != ractions[0]:
            maxDiff = diff
            maxAction = ractions[0]
            maxIndex = index
            Bhscore = rhscore
            Brscore = rscore
            BrRollout = ractions
        index += 1

    state, human_action = human_rollout[maxIndex]
    print("Fatal Flaw state")
    state.printBoard()
    print()
    print("Your actions: ")
    printActions(game, [s[1] for s in human_rollout])
    print("There was a fatal flaw at action index", maxIndex)
    print()
    print("You took: ", human_action, "~best score of", Bhscore)
    print("Your actions starting at fatal flaw:")
    printActions(state, [s[1] for s in human_rollout[maxIndex : -1]])
    print()
    print("You should have taken: ", maxAction, "with a ~best score of ", Brscore)
    print("Optimal actions starting at fatal flaw, starting with corrected action:")
    printActions(state, BrRollout + [None])
    print("You could have gotten", Brscore)
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
