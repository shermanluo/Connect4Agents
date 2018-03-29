import numpy as np

def euclidDist(A, B):
    return pow(pow(A[0] - B[0], 2) + pow(A[1] - B[1], 2), 0.5)
def boardCopy(board):
    copy = []
    for i in board:
        copy.append(i[:])
    return copy
def doubleSwitch(double):
    if double == (0,0):
        return (0, 9)
    if double == (0, 9):
        return (9, 9)
    if double == (9, 9):
        return (9, 0)
    else:
        return (0,0)
def listPrint(lst):
    s = ''
    for i in lst:
        s = s + str(i) + "  "
    print(s)
def formatPrint(lst, board):
    # Add leading spaces to align columns of board printout
    new_lst = []
    target_len = 2
    #target_len = np.max([len(str(j)) for i in board for j in i])
    for i in lst:
        new_lst.append(" "*(target_len - len(i)) + i)
    return new_lst
        
class gridGame(object):
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |                       
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 X |
    #(0,0) is defined at top left
    #(0,9) is defined at top right
    #(9, 0) is defined as bottom left
    #player starts at (0,0)
    def __init__(self, numPieces, board = None, holding = None, double = (0,9), playerLoc = (0,0), actions_taken = []):
        if board:
            self.board = board
        else:
            self.board = []
            for i in range(0, 10):
                temp = []
                for i in range(0, 10):
                    temp.append(0)
                self.board.append(temp)
        self.holding = holding
        self.playerLoc = playerLoc
        self.double = double
        self.numPieces = numPieces
        self.actions_taken = actions_taken

    def getLegalActions(self):
        if self.holding:
            return [(0,0), (9,9), (0,9), (9, 0)]
        actions = []
        for i in range(0, 10):
            for j in range(0, 10):
                if self.board[i][j]:
                    actions.append((i,j))
        return actions

    #returns state, reward
    def getSuccessor(self, action):
        dist = euclidDist(action, self.playerLoc)
        if self.holding:
            h = self.holding
            if self.double == action:
                reward = 2 * h - dist
                return (gridGame(self.numPieces, boardCopy(self.board), None, doubleSwitch(self.double), action, actions_taken = self.actions_taken + [action]), reward)
            else:
                reward = h - dist
                return (gridGame(self.numPieces, boardCopy(self.board), None, self.double, action, actions_taken = self.actions_taken + [action]), reward)

        h = self.board[action[0]][action[1]]
        newBoard = boardCopy(self.board)
        newBoard[action[0]][action[1]] = 0
        return (gridGame(self.numPieces - 1, newBoard, h, self.double, action, actions_taken = self.actions_taken + [action]), - dist)

    def isOver(self):
        return len(self.getLegalActions()) == 0

    def printBoard(self, print_to_screen=True):
        board = []
        for i in range(0, 10):
            toPrint = []
            for j in range(0, 10):
                if self.playerLoc[0] == i and self.playerLoc[1] ==j:
                    toPrint.append("P")
                elif self.double[0] == i and self.double[1] == j:
                    toPrint.append("2")
                else:
                    toPrint.append(str(self.board[i][j]))
            if print_to_screen:
                listPrint(toPrint)
            board.append(formatPrint(toPrint, self.board))
        return board

    def getPiecesandLocations(self):
        ret = set()
        for i in range(0, 10):
            for j in range(0, 10):
                if self.board[i][j]:
                    red.add((i, j, self.board[i][j]))
        return ret 

    def __hash__(self):
        total = 0
        count = 1
        for i in range(0, 10):
            for j in range(0, 10):
                count += 1
                total += self.board[i][j] * count
        total *= 1000
        total += self.playerLoc[0]
        total *= 10
        total += self.playerLoc[1]
        total *= 10
        total += self.double[0]
        total *= 10
        total += self.double[1]
        total *= 10
        if self.holding:
            total += 9
        else:
            total += 2
        return total

    def __eq__(self, game2):
        if self.holding != game2.holding:
            return False
        for i in range(0, 10):
            if self.board[i] != game2.board[i]:
                return False
        if (self.playerLoc != game2.playerLoc):
            return False
        if len(self.actions_taken) != len(game2.actions_taken):
            return False
        for i in range(len(self.actions_taken)):
            if self.actions_taken[i] != game2.actions_taken[i]:
                return False
        return True



        






