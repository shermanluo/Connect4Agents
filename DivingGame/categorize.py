from divegame import diveGame
from enum import Enum
import pickle


class CorrectionType(Enum):
    A = "Should have returned to the surface"
    B = "Went to the wrong surface location"
    C = "Got the wrong piece" 
    D = "Should have bought a tank"
    E = "Should not have bought a tank"
    F = "Bought the wrong tank"
    G = "Exits early"
    H = "Should have exit"
    I = "Should have changed Surface Locations"
    J = "Should have gotten piece instead of went to other surface"
    K = "Should have gotten piece instead of surfacing"

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

def categorize(state, action, correction):
    actions = state.getLegalActions()
    assert action in actions 
    assert correction in actions 
    assert action != correction


    if isUnderwater(state) and targetsPiece(action) and targetsSurface(correction):
        return CorrectionType.A
    if isUnderwater(state) and targetsSurface(action) and targetsSurface(correction):
        return CorrectionType.B
    if targetsPiece(action) and targetsPiece(correction):
        return CorrectionType.C
    if not buysTank(action) and buysTank(correction):
        return CorrectionType.D
    if buysTank(action) and not buysTank(correction):
        return CorrectionType.E
    if buysTank(action) and buysTank(correction):
        return CorrectionType.F
    if exits(action) and not exits(correction):
        return CorrectionType.G
    if not exits(action) and exits(correction):
        return CorrectionType.H
    if not isUnderwater(state) and targetsPiece(action) and targetsSurface(correction):
        return CorrectionType.I
    if isUnderwater(state) and targetsSurface(action) and targetsPiece(correction):
        return CorrectionType.J
    if not isUnderwater(state) and targetsSurface(action) and targetsPiece(correction):
        return CorrectionType.K

    print(isUnderwater(state), targetsSurface(action), targetsSurface(correction))
    print(state.playerLoc, action, correction)
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
