def manDist(A, B):
    return abs(A[0] - B[0]) + abs(A[1] - B[1])

def boardCopy(board):
    copy = []
    for i in board:
        copy.append(i[:])
    return copy
def zeroBoard():
    board = [[0 for _ in range(10)] for __ in range(20)]
    return board

def formatPrint(lst, board):
    # Add leading spaces to align columns of board printout
    new_lst = []
    target_len = 2
    #target_len = np.max([len(str(j)) for i in board for j in i])
    for i in lst:
        new_lst.append(" "*(target_len - len(i)) + i)
    return new_lst

class diveGame:
    # | P 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |                       
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |                       
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    # | 0 0 0 0 0 0 0 0 0 0 |
    #(0,0) is defined at top left
    #(0,9) is defined at top right
    #(19,0) is defined as bottom left
    #player starts at (0,0)
    tanks = {(20, 35, "tank"), (30, 45, "tank"), (60, 55, "tank")} #cost, size
    defaultOxygen = 20
    defaultTank = 20
    defaultTime = 90

    def __init__(self, board = None, playerLoc = (0,0), timeLeft = defaultTime, oxygenLeft = defaultOxygen, holding = [], tankSize = defaultTank, cash = 0, gameOver = False):
        self.board = board
        if not board and playerLoc:
            self.board = zeroBoard()
            self.board[1][5] = 5
            self.board[2][0] = 16
            self.board[3][9] = 21
            self.board[7][6] = 23
            self.board[8][3] = 24
            self.board[10][9] = 31
            self.board[12][5] = 15
            self.board[13][2] = 52
            self.board[10][1] = 29
            self.board[19][2] = 161
            self.board[15][7] = 75
        self.playerLoc = playerLoc
        self.timeLeft = timeLeft
        self.tankSize = tankSize
        self.oxygenLeft = oxygenLeft
        self.holding = holding
        self.cash = cash
        self.gameOver = gameOver

    def getLegalActions(self):
        actions = []
        if self.playerLoc[0] == 0:
            actions.append((None, None, "exit"))
        if self.playerLoc[0] == 0:
            for tank in diveGame.tanks:
                if tank[0] <= self.cash and tank[1] > self.tankSize:
                    actions.append(tank)
        for i in range(0, 20):
                for j in range(0, 10):
                    if self.board[i][j]:
                        if manDist(self.playerLoc, (i, j)) <= self.timeLeft:
                            actions.append((i , j, "move"))
        for i in range(10):
            if not (self.playerLoc[1] == i and self.playerLoc[0] == 0) and i == 0 or i == 5 or i == 9:
                actions.append((0, i, "move"))
        return actions
    def isOver(self):
        return self.gameOver

    def getSuccessor(self, action):
        if (action[2] == "exit"):
            return (diveGame(board = None, playerLoc = None, oxygenLeft = None, 
                holding = None, tankSize = None, cash = None, gameOver = True), 0)

        if (action[2] == "move"):
            location = (action[0], action[1])
            dist = manDist(self.playerLoc, location)

            if dist > self.oxygenLeft:
                return (diveGame(board = None, playerLoc = None, oxygenLeft = None, 
                holding = None, tankSize = None, cash = None, gameOver = True), -10000000)

            if location[0] == 0:
                return (diveGame(board = boardCopy(self.board), playerLoc = location, timeLeft = self.timeLeft - dist, 
                oxygenLeft = self.tankSize, holding = [], tankSize = self.tankSize, cash = self.cash + sum(self.holding), 
                gameOver = False), sum(self.holding))
            newBoard = boardCopy(self.board)
            newBoard[location[0]][location[1]] = 0
            return (diveGame(board = newBoard, playerLoc = location, timeLeft = self.timeLeft - dist, 
                    oxygenLeft = self.oxygenLeft - dist, holding = self.holding + [self.board[location[0]][location[1]]], 
                    tankSize = self.tankSize, cash = self.cash, gameOver = False), 0)

        if (action[2] == "tank"):
            tankCost = action[0]
            tank = action[1]
            return (diveGame(self.board, playerLoc = self.playerLoc, timeLeft = self.timeLeft, 
                oxygenLeft = tank, holding = [], tankSize = tank, cash = self.cash - tankCost, 
                gameOver = False), -tankCost)

    def printBoard(self, print_to_screen = True):
        board = []
        for i in range(0, 20):
            toPrint = []
            for j in range(0, 10):
                if self.playerLoc[0] == i and self.playerLoc[1] ==j:
                    toPrint.append("P")
                else:
                    toPrint.append(str(self.board[i][j]))
            if print_to_screen:
                #listPrint(toPrint)
                toPrint = [x.replace('0', ' _ ') for x in toPrint]
                print(" ".join(formatPrint(toPrint, self.board)))
            board.append(formatPrint(toPrint, self.board))
        if print_to_screen:
            print("tank size:", self.tankSize)
            print("cash:", self.cash)
            print("oxygen:", self.oxygenLeft)
            print("timeLeft:", self.timeLeft)
            print("holding:", self.holding)
        for i in range(len(board)):
            board[i] = [x.replace(' 0', ' _') for x in board[i]]
        return board




