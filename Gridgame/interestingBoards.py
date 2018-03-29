from Agent import K1GreedyAgent, MaxAgent
from gridGame import gridGame
from random import randint

def generateRandomBoard(numpieces = 4):
    pieces = {}
    while(len(pieces) < numpieces):
        i = randint(0, 9)
        j = randint(0, 9)
        if (i, j) != (0, 0) and (i, j) != (0, 9) and  (i, j) != (9, 0) and (i, j) != (9, 9) and (i, j) not in pieces:
            piece = randint(1, 20)
            pieces[(i,j)] = piece
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for k,v in pieces.items():
        board[k[0]][k[1]] = v
    return gridGame(numpieces, board)


def findInterestingBoards():
    gagent = K1GreedyAgent()
    oagent = MaxAgent()
    games = []
    while len(games) < 5:
        scoreGreedy = 0
        ggame = generateRandomBoard(4)
        game = ggame
        actions = game.getLegalActions()
        while actions:
            nxt = game.getSuccessor(gagent.getAction(game))
            scoreGreedy += nxt[1]
            game = nxt[0]
            actions = game.getLegalActions()
        scoreOptimal = oagent.value(ggame)[0]
        print(scoreOptimal, scoreGreedy)
        if scoreOptimal - scoreGreedy >= 15:
            games.append((ggame, scoreOptimal, scoreGreedy))
            print("FOUND")
    for game in games:
        print()
        game[0].printBoard()
        print("OPTIMAL", game[1], "GREEDY", game[2])


findInterestingBoards()

