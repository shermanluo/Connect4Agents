from Agent import K1GreedyAgent, MaxAgent
from gridGame import gridGame
from random import randint

THRESHOLD = 20
N_BOARDS = 10

def generateRandomBoard(numpieces = 4):
    pieces = {}
    while(len(pieces) < numpieces):
        i = randint(0, 9)
        j = randint(0, 9)
        if (i, j) != (0, 0) and (i, j) != (0, 9) and  (i, j) != (9, 0) and (i, j) != (9, 9) and (i, j) not in pieces:
            piece = randint(20, 40)
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
    double_options = [(0,9), (9,9), (9,0)]
    double_idx = randint(0,len(double_options)-1)
    return gridGame(numpieces, board, double=double_options[double_idx])

def playGame(game, agent, return_rollout=False):
    curr = game
    total_score = 0
    rollout = [game]
    scores = [total_score]
    while curr.getLegalActions():
        curr, score = curr.getSuccessor(agent.getAction(curr))
        total_score += score
        rollout.append(curr)
        scores.append(total_score)
    if return_rollout:
        return total_score, rollout, scores
    return total_score

def findInterestingBoards(threshold=THRESHOLD, n_boards=N_BOARDS, numpieces = 4):
    k10agent = MaxAgent(depth=10)
    k2agent = MaxAgent(depth=2)
    k1agent = MaxAgent(depth=1)
    games = []
    n_tried = 0
    while len(games) < n_boards:
        scoreGreedy = 0
        ggame = generateRandomBoard(numpieces)
        scoreK10 = k10agent.value(ggame)[0]
        scoreK2 = playGame(ggame, k2agent)
        scoreK1 = playGame(ggame, k1agent)
        print(scoreK10, scoreK2, scoreK1)
        print("\t", scoreK10-scoreK2, scoreK10-scoreK1)
        if scoreK10 - scoreK1 >= threshold and scoreK10 - scoreK2 >= threshold:
            games.append((ggame, scoreK10, scoreK2, scoreK1))
            print("FOUND")
        n_tried += 1
    print("number boards tried:", n_tried)
    for game in games:
        print()
        game[0].printBoard()
        print("OPTIMAL (K=10)", game[1], "GREEDY (K=1)", game[3], \
              "SUBOPT (K=2)", game[2])
    return [x[0] for x in games]

def main():
    findInterestingBoards()

if __name__ == "__main__":
    main()

