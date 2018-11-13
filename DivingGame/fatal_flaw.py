#!/usr/bin/env python

#from max_diff_valsV2 import print_max_diff_vals
import m2
from divegame import diveGame
import pdb
from Agent import QSolveAgent, MaxAgent
from max_diff_valsV2 import print_max_diff_vals
from joblib import Parallel, delayed
from comparison import explainKgreatestPlus1, explainKgreatest, explainIncreasinglyLarge, explainIncreasinglyLargePlus1, skip2
import pickle
import argparse
import pdb
from categorize import categorize, groupMistake
#returns state, action rollout. Last action will be None

NUM_ITERS = 100000

def formatScore(score):
    return format(score, '.2f')
def getHumanRollout(game, moves, getscore = False):
    rollout = []
    rewards = []
    scores = []
    score = 0
    for m in moves:
        scores.append(score)
        rollout.append((game, m))
        nxt = game.getSuccessor(m)
        game = nxt[0]
        score += nxt[1]
        rewards.append(nxt[1])
        actions = game.getLegalActions()
    #print(m)
    rollout.append((game, None))
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
            return curr
        elif action[2] == "exit":
            curr += "|EXIT"
            print(curr)
            return curr
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

def getActions(state, depth, num_iters, allData = False, allRollouts = False, allRolloutsAdd = False):
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
    bestStates = [states for states,_,_,_ in results]
    bestIdx = max(range(len(values)), key = lambda x: values[x])
    bestScore = values[bestIdx]
    assert bestScore == max(values)
    bestActions = [actions[bestIdx]] + results[bestIdx][1]
    NA = [(results[i][-1],actions[i]) for i in range(len(results))] #NA is state u ended up at, and what action you took to get there
    if allRollouts:
        return [[actions[i]] + results[i][1] for i in range(len(actions))], values
    if allData:
        return [[state.cash] + scores for _,_,scores,_ in results], bestStates, bestIdx, NA, [state] + bestStates[bestIdx], bestActions
    if allRolloutsAdd:
        return bestScore, bestActions, NA, [state] + bestStates[bestIdx], [[actions[i]] + results[i][1] for i in range(len(actions))], values
    return bestScore, bestActions, NA, [state] + bestStates[bestIdx]

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
    BrActions = None
    assert humanscores[-1] == finalScore
    for state, human_action in human_rollout:
        sofar = getSoFarScore(rewards, index)
        if human_action == None:
            break
        #pdb.set_trace()
        #rhscore, hractions = getActions(state.getSuccessor(human_action)[0], 0, 50000)
        s = m2.State()
        s.gs = state
        rscore, ractions, NA, rstates = getActions(state, 1, NUM_ITERS)
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
            BrRollout = rstates
            BrActions = ractions
        index += 1
    BrActions = BrActions + [None]
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
    printActions(state, BrActions)
    print("You could have gotten", Brscore)
 
    print("Starting Fatal Flaw state")

    state.printBoard()

    k2Agent = MaxAgent(depth=2)
    valuefn = lambda s: k2Agent.value(s)[0]
    hR = [x[0] for x in human_rollout][maxIndex:]
    hS = [x.cash for x in hR]
    rS = [x.cash for x in BrRollout]

    f = open('store.pckl', 'wb')
    pickle.dump((BrRollout, rS, hR, hS, BrActions, [x[1] for x in human_rollout][maxIndex:]), f)
    f.close()
    #print_max_diff_vals(BrRollout, hR, valuefn, rS, hS)
    explain(BrRollout, rS)


# def dataCalc(states, actions): 
#     data = []
#     for i in range(len(states) - 1):
#         state = states[i]
#         takenAction = actions[i]
#         possibleActions = state.getLegalActions()
#         idxTaken = [x for x, y in enumerate(possibleActions) if y == takenAction][0]
#         scores, bestStates, bestIdx, stateActions, BestRollout, bestActions = getActions(state, 1, NUM_ITERS, allData = True)
#         data.append((idxTaken, bestIdx, scores, BestRollout, bestActions))
#     return data

# def fatalFlaw(game, moves):
#     human_rollout, rewards, humanscores = getHumanRollout(game, moves, getscore = True)
#     data = dataCalc([x[0] for x in human_rollout], moves)
    
#     biggestDiff = -10000000000
#     maxIndex = None
#     Rr = None
#     rS = None

#     index = 0

#     for idxTaken, bestIdx, scores, bestRollout, bestActions in data:
#         diff = scores[bestIdx][-1] - scores[idxTaken][-1]
#         if diff > biggestDiff:
#             biggestDiff = diff
#             maxIndex = index
#             Rr = bestRollout
#             rS = scores
#         index += 1

#     return Rr, rS, human_rollout, humanscores, bestActions, [x[1] for x in human_rollout][maxIndex:], maxIndex, data
def fatalFlaw(game, moves, threeGroups = False):
    human_rollout, rewards, humanscores = getHumanRollout(game, moves, getscore = True)
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
    BrActions = None
    group = None
    assert humanscores[-1] == finalScore
    for state, human_action in human_rollout:
        sofar = getSoFarScore(rewards, index)
        if human_action == None:
            break
        #pdb.set_trace()
        #rhscore, hractions = getActions(state.getSuccessor(human_action)[0], 0, 50000)
        s = m2.State()
        s.gs = state
        rscore, ractions, NA, rstates, rollouts, scores = getActions(state, 1, NUM_ITERS, allRolloutsAdd = True)
        humanOptimalRollout = [roll for roll in rollouts if roll[0] == human_action][0]
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
        if human_action != ractions[0]:
            mType = categorize(state, human_action, ractions, humanOptimalRollout)
            print(mType)
            group = groupMistake(mType)
            print(group)
        if (diff > maxDiff and human_action != ractions[0] and not threeGroups) or (diff > maxDiff and human_action != ractions[0] and group):
            maxDiff = diff
            maxAction = ractions[0]
            maxIndex = index
            Bhscore = rhscore
            Brscore = rscore
            BrRollout = rstates
            BrActions = ractions
            maxGroup = group
        index += 1
    if not BrActions:
        return None, None, None, None, None, None, None, None
    BrActions = BrActions + [None]
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
    printActions(state, BrActions)
    print("You could have gotten", Brscore)
 
    print("Starting Fatal Flaw state")

    state.printBoard()

    k2Agent = MaxAgent(depth=2)
    valuefn = lambda s: k2Agent.value(s)[0]
    hR = [x[0] for x in human_rollout][maxIndex:]
    hS = [x.cash for x in hR]
    rS = [x.cash for x in BrRollout]

    f = open('store.pckl', 'wb')
    pickle.dump((BrRollout, rS, hR, hS, BrActions, [x[1] for x in human_rollout][maxIndex:]), f)
    f.close()
    #print_max_diff_vals(BrRollout, hR, valuefn, rS, hS)
    #explain(BrRollout, rS)
    return BrRollout, rS, hR, hS, BrActions, [x[1] for x in human_rollout][maxIndex:], maxIndex, maxGroup



def getPickle():
    f = open('store.pckl', 'rb')
    rR, rS, hR, hS, rA, hA = pickle.load(f)
    return rR, rS, hR, hS, rA, hA  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=':)')
    parser.add_argument('phase')
    parser.add_argument('hr')
    args = parser.parse_args()
    if args.phase == '1':
        main()
    elif args.phase == '2':       
        rR, rS, hR, hS, rA, hA = getPickle()
        if args.hr == 'r':
            rollout = rR
            score = rS 
            actions = rA
        if args.hr == 'h':
            rollout = hR
            score = hS
            actions = hA
        info = printActions(rollout[0], actions)

        print("0 | explainKgreatestPlus1")
        print("1 | explainKgreatest")
        print("2 | explainIncreasinglyLargePlus1")
        print("3 | explainIncreasinglyLarge")
        print("4 | skip2")
        choice = int(input())
        if choice == 0:
            explainKgreatestPlus1(rollout, score, info)
        if choice == 1:
            explainKgreatest(rollout, score, info)
        if choice == 2:
            explainIncreasinglyLargePlus1(rollout, score, info)
        if choice == 3:
            explainIncreasinglyLarge(rollout, score, info)
        if choice == 4:
            skip2(rollout, score, info)

