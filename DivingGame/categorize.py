from divegame import diveGame
from enum import Enum
import pickle
from divegame import manDist


class CorrectionType(Enum):
    A = "Should have returned to the surface"
    B = "Went to the wrong surface location"
    C1 = "Missed piece along the way from Underwater"
    C2 = "Missed piece along the way from Surface" 
    C3 = "Got piece too deep from surface"
    C4 = "Got piece too shallow from surface"
    C = "Got the wrong piece" 

    D = "Should have bought a tank"
    E = "Should not have bought a tank"
    F = "Bought the wrong tank"
    G = "Exits early"
    H = "Should have exit"
    I = "Should have changed Surface Locations"
    J = "Should have gotten piece instead of surfacing"
    K =  "Should have gotten piece instead of going to other surface"

#G&H may be grouped together, exit errors
#D&F may be grouped together, failing to buy a good tank. Maybe also E?d

def targetsPiece(action):
    return action[2] == "move" and action[0] != 0

def targetsSurface(action):
    return action[2] == "move" and action[0] == 0

def buysTank(action):
    return action[2] == "tank"

def exits(action):
    return action[2] == "exit"

def isUnderwater(state):
    return state.playerLoc[0] != 0

def testPlay():
    gameState = diveGame(board = None, playerLoc = (0,0), holding = [], cash = 0, gameOver = False)
    reward = 0
    start = gameState
    stateActions = []

    f = open("testStates.pckl", 'rb')
    currStates = pickle.load(f)
    f = open("testStates.pckl", 'wb')

    while True:
        if gameState.isOver():
            print()
            print("FINAL REWARD:", reward)
            print(stateActions)
            return stateActions
        gameState.printBoard()
        actions = [(a,b) for a,b in enumerate(gameState.getLegalActions())]
        print()
        print('ACTIONS')
        for x,y in actions:
            if y[2] == "exit":
                print(x, "exit")
            if y[2] == "tank":
                print(x, "buy tank:", y[1], "for cost:", y[0])
            if y[2] == "move": 
                print(x, "move:", y[:2])
        a = input()
        if a == "exit":
            f.close()
            return
        if a == "save":
            currStates.append(gameState)
            pickle.dump(currStates, f)
        a = int(input())
        stateActions.append((gameState, actions[a][1]))           
        nxt = gameState.getSuccessor(actions[a][1])
        gameState = nxt[0]
        reward += nxt[1]
    f.close()




# def categorize(state, action, cRollout, aRollout):
#     actions = state.getLegalActions()
#     correction = cRollout[0]

#     assert action in actions 
#     assert correction in actions 
#     assert action != correction


#     # if isUnderwater(state) and targetsPiece(correction) and targetsPiece(action) and goingBack2(state, action, aRollout):
#     #     print("GI")

#     if (isUnderwater(state) and targetsPiece(action) and targetsSurface(correction)) or (goingBack(state, action, correction, cRollout)):
#         return CorrectionType.A
#     if (isUnderwater(state) and targetsSurface(action) and targetsSurface(correction)) or (isUnderwater(state) and goingdiffback(state, action, correction, aRollout, cRollout)):
#         return CorrectionType.B

#     if (isUnderwater(state) and targetsSurface(action) and targetsPiece(correction)) or (isUnderwater(state) and targetsPiece(correction) and targetsPiece(action) and goingBack2(state, action, aRollout)):
#         return CorrectionType.J

#     if targetsPiece(action) and targetsPiece(correction):
#         return CorrectionType.C

#     if not buysTank(action) and buysTank(correction):
#         return CorrectionType.D
#     if buysTank(action) and not buysTank(correction):
#         return CorrectionType.E
#     if buysTank(action) and buysTank(correction):
#         return CorrectionType.F
#     if exits(action) and not exits(correction):
#         return CorrectionType.G
#     if not exits(action) and exits(correction):
#         return CorrectionType.H
#     if not isUnderwater(state) and targetsPiece(action) and targetsSurface(correction):
#         return CorrectionType.I
#     if not isUnderwater(state) and targetsSurface(action) and targetsPiece(correction):
#         return CorrectionType.K

#     raise Exception("No category found!")

def nextSurface(cRollout):
    surf = None
    for action in cRollout:
        if targetsSurface(action):
            surf = action
            return surf
    return None

def tanks(rollout):
    tanks = set()
    for action in rollout:
        if buysTank(action):
            tanks.add(action)
    return tanks

def goingToGoal(state, rollout, goal, slack):
    if not goal:
        return False
    if goal not in rollout:
        return False
    currPos = state.playerLoc
    goalLoc = (goal[0], goal[1])
    dist = manDist(currPos, goalLoc)
    traveled = 0
    for action in rollout:
        if action[0] == None:
            print(action, rollout)
        traveled += manDist(currPos, (action[0], action[1]))
        currPos = (action[0], action[1])
        if traveled > dist + slack: #leniency of 4 when returning
            return False
        if currPos == goalLoc:
            return str(traveled - dist)
    raise Exception("YOU SHOULDN'T HAVE GOTTEN HERE")

def otherSurface(loc):
    if loc == (0, 0):
        return (0, 9)
    else:
        return (0, 0)

def heightDiff(action, correction):
    return action[0] - correction[0]

def groupMistake(mistake):
    if mistake == CorrectionType.A or mistake == CorrectionType.J or mistake == CorrectionType.B:
        return 1
    if mistake == CorrectionType.D or mistake == CorrectionType.E or mistake == CorrectionType.F:
        return 2
    if mistake == CorrectionType.I or mistake == CorrectionType.K:
        return 3
    return None

def categorize(state, action, cRollout, aRollout):
    actions = state.getLegalActions()
    correction = cRollout[0]

    assert action in actions 
    assert correction in actions 
    assert action != correction

    aSurface = nextSurface(aRollout)
    cSurface = nextSurface(cRollout)
    atanks = tanks(aRollout)
    ctanks = tanks(cRollout)


    if isUnderwater(state): #Should have returned to the surface
        if not goingToGoal(state, aRollout, aSurface, 4) and goingToGoal(state, cRollout, cSurface, 4):
            return CorrectionType.A

    if isUnderwater(state): #Should have gotten another piece instead of surfacing
        if goingToGoal(state, aRollout, aSurface, 4) and not goingToGoal(state, cRollout, cSurface, 4):
            return CorrectionType.J

    if isUnderwater(state): #wrong surface location 
        if aSurface != cSurface and goingToGoal(state, aRollout, aSurface, 4) and goingToGoal(state, cRollout, cSurface, 4):
            return CorrectionType.B

    if isUnderwater(state): 
        if aSurface == cSurface and goingToGoal(state, aRollout, aSurface, 4) and goingToGoal(state, cRollout, cSurface, 4):
            aslack = int(goingToGoal(state, aRollout, aSurface, 4))
            cslack = int(goingToGoal(state, cRollout, cSurface, 4))
            assert aslack <= 4 and cslack <= 4
            if aslack < cslack:
                return CorrectionType.J #Should have gotten piece instead of surfacing
            if aslack > cslack:
                return CorrectionType.A #should have gone back to surface




    if not isUnderwater(state) and targetsPiece(correction) and targetsPiece(action) and goingToGoal(state, cRollout, action, 2):
        return CorrectionType.C1 #missed something along the way


#------------------------------

    if not isUnderwater(state): #should have bought a tank
        if buysTank(correction) and not buysTank(action):
            return CorrectionType.D
    if not isUnderwater(state): #should not have bought a tank
        if buysTank(action) and not buysTank(correction):
            return CorrectionType.E                               #E AND F COULD BE THE SAME MISTAKE
    if buysTank(action) and buysTank(correction): #bought the wrong tank
         return CorrectionType.F

#------------------------------
    if not isUnderwater(state): #should not have switched surface
        if aSurface and not goingToGoal(state, cRollout, aSurface, 2) and goingToGoal(state, aRollout, aSurface, 2):
            return CorrectionType.K

    if not isUnderwater(state): #should have switched surface
        if cSurface and goingToGoal(state, cRollout, cSurface, 2) and not goingToGoal(state, aRollout, cSurface, 2):
            return CorrectionType.I

    if not isUnderwater(state): #should have switched surface
        if cSurface == aSurface and cSurface and state.playerLoc != (cSurface[0], cSurface[1]) and goingToGoal(state, cRollout, cSurface, 2) and goingToGoal(state, aRollout, cSurface, 2):
            if action == aSurface:
                return CorrectionType.K
            else:
                return CorrectionType.I

    if not isUnderwater(state) and targetsPiece(correction) and targetsPiece(action) and goingToGoal(state, cRollout, action, 2):
        return CorrectionType.C2 #missed something along the way


#------------------------------------
    if not isUnderwater(state) and exits(action) and not exits(correction): #exits early
        return CorrectionType.G

    if not isUnderwater(state) and not exits(action) and exits(correction): #exits late
        return CorrectionType.H

#------------------------------



    #if isUnderwater(state):
    if targetsPiece(action) and targetsPiece(correction):
        if heightDiff(action, correction) > 0:
            return CorrectionType.C3
        if heightDiff(action, correction) < 0:
            return CorrectionType.C4

    return CorrectionType.C



    print(state.playerLoc)
    print(aRollout)
    print(cRollout)


    raise Exception("No category found!")






def testCategorize():
    stateActions = testPlay()
    for state, action in stateActions:
        alternatives = [a for a in state.getLegalActions() if a != action]
        for alt in alternatives:
            corrtype = categorize(state, action, alt)
            if isUnderwater(state):
                text = "UNDERWATER"
            else:
                text = "SURFACE,"
            print(text, "Action:", action, "Correction:", alt, "Correction Type:", corrtype)

#testPlay()
