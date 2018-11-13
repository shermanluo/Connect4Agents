def manDist(A, B):
    if B[0] == None or B[1] == None:
        print(A, B)
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


    #tanks = {(20, 30, "tank"), (45, 45, "tank"), (60, 55, "tank")} #cost, size
    tanks = {(20, 30, "tank"), (45, 45, "tank"), (60, 55, "tank")} #cost, size
    #tanks = {(20, 30, "tank"), (50, 45, "tank"), (70, 55, "tank")} #cost, size
    #tanks = {(25, 30, "tank"), (40, 45, "tank"), (60, 50, "tank")} #cost, size
    #tanks = {(25, 30, "tank"), (45, 45, "tank"), (60, 55, "tank")} #cost, size


    # defaultOxygen = 25
    # defaultTank = 25
    # defaultTime = 85

    defaultOxygen = 25
    defaultTank = 25
    defaultTime = 80

    # defaultOxygen = 17
    # defaultTank = 17
    # defaultTime = 90

    # defaultOxygen = 20
    # defaultTank = 20
    # defaultTime = 75

    # defaultOxygen = 20
    # defaultTank = 20
    # defaultTime = 80



    def __init__(self, board = None, playerLoc = (0,0), timeLeft = defaultTime, oxygenLeft = defaultOxygen, holding = [], tankSize = defaultTank, cash = 0, gameOver = False, tanks = tanks):
        self.board = board
        if tanks or tanks == {}:
            self.tanks = tanks
        if not board and playerLoc:
            self.board = zeroBoard()

            # self.board[1][5] = 11
            # self.board[3][2] = 15
            # self.board[3][9] = 21
            # self.board[7][6] = 26
            # self.board[8][3] =  21
            # self.board[11][9] = 41
            # self.board[13][4] = 52
            # self.board[10][1] = 29
            # self.board[19][2] = 151
            # self.board[16][7] = 79

            self.board[3][2] = 9
            self.board[3][7] = 17
            self.board[4][5] = 15
            self.board[5][9] = 21
            self.board[9][6] = 28
            self.board[8][1] =  41
            self.board[11][9] = 29
            self.board[13][4] = 31
            self.board[10][2] = 37
            self.board[19][7] = 91
            self.board[16][3] = 51

            # self.board[4][5] = 5
            # self.board[3][2] = 17
            # self.board[5][9] = 11
            # self.board[1][9] = 21
            # self.board[5][7] = 24
            # self.board[7][0] =  32
            # self.board[11][9] = 29
            # self.board[14][7] = 42
            # self.board[10][2] = 37
            # self.board[19][2] = 85
            # self.board[17][3] = 70

            # self.board[4][5] = 15
            # self.board[3][2] = 17
            # self.board[5][9] = 24
            # self.board[7][0] =  34
            # self.board[11][9] = 29
            # self.board[14][7] = 42
            # self.board[10][2] = 51
            # self.board[19][2] = 101
            # self.board[17][3] = 70

            # self.board[3][5] = 9
            # self.board[8][2] = 17
            # self.board[5][9] = 24
            # self.board[7][0] =  34
            # self.board[11][9] = 29
            # self.board[14][7] = 42
            # self.board[10][2] = 29
            # self.board[19][2] = 90
            # self.board[17][3] = 42
            # self.board[19][9] = 39


        self.playerLoc = playerLoc
        self.timeLeft = timeLeft
        self.tankSize = tankSize
        self.oxygenLeft = oxygenLeft
        self.holding = holding
        self.cash = cash
        self.gameOver = gameOver


    def clone(self):
        return diveGame(board = boardCopy(self.board), playerLoc = self.playerLoc, timeLeft = self.timeLeft, oxygenLeft = self.oxygenLeft, holding = self.holding[:], tankSize = self.tankSize, cash = self.cash, gameOver = self.gameOver, tanks = self.tanks)

    def getLegalActions(self):
        if self.gameOver:
            return []
        actions = []
        if self.playerLoc[0] == 0:
            actions.append((None, None, "exit"))
        if self.playerLoc[0] == 0:
            for tank in self.tanks:
                if tank[0] <= self.cash and tank[1] > self.tankSize:
                    actions.append(tank)
        for i in range(0, 20):
                for j in range(0, 10):
                    if self.board[i][j]:
                        if manDist(self.playerLoc, (i, j)) <= self.timeLeft:
                            actions.append((i , j, "move"))
        for i in range(10):
            if not (self.playerLoc[1] == i and self.playerLoc[0] == 0) and (i == 0 or i == 9):
                actions.append((0, i, "move"))
        return actions
    def isOver(self):
        return self.gameOver

    def getSuccessor(self, action):
        assert action in self.getLegalActions()
        if (action[2] == "exit"):
            return (diveGame(board = boardCopy(self.board), playerLoc = self.playerLoc, timeLeft = self.timeLeft, oxygenLeft = self.oxygenLeft, 
                holding = self.holding[:], tankSize = self.tankSize, cash = self.cash, gameOver = True, tanks = self.tanks), 0)

        if (action[2] == "move"):
            location = (action[0], action[1])
            dist = manDist(self.playerLoc, location)

            if dist > self.oxygenLeft:
                return (diveGame(board = boardCopy(self.board), playerLoc = location, timeLeft = self.timeLeft - dist, oxygenLeft = self.oxygenLeft - dist, 
                holding = self.holding[:], tankSize = self.tankSize, cash = 0, gameOver = True, tanks = self.tanks), -self.cash)

            if dist > self.timeLeft:
                return (diveGame(board = boardCopy(self.board), playerLoc = location, timeLeft = self.timeLeft - dist, oxygenLeft = self.oxygenLeft - dist, 
                holding = self.holding[:], tankSize = self.tankSize, cash = 0, gameOver = True, tanks = self.tanks), 0)

            if location[0] == 0:
                return (diveGame(board = boardCopy(self.board), playerLoc = location, timeLeft = self.timeLeft - dist, 
                oxygenLeft = self.tankSize, holding = [], tankSize = self.tankSize, cash = self.cash + sum(self.holding), 
                gameOver = False, tanks = self.tanks), sum(self.holding))
            newBoard = boardCopy(self.board)
            newBoard[location[0]][location[1]] = 0
            return (diveGame(board = newBoard, playerLoc = location, timeLeft = self.timeLeft - dist, 
                    oxygenLeft = self.oxygenLeft - dist, holding = self.holding + [self.board[location[0]][location[1]]], 
                    tankSize = self.tankSize, cash = self.cash, gameOver = False, tanks = self.tanks), 0)

        if (action[2] == "tank"):
            tankCost = action[0]
            tank = action[1]
            return (diveGame(self.board, playerLoc = self.playerLoc, timeLeft = self.timeLeft, 
                oxygenLeft = tank, holding = [], tankSize = tank, cash = self.cash - tankCost, 
                gameOver = False, tanks = self.tanks), -tankCost)

    def printBoard(self, print_to_screen = True):
        if self.gameOver:
            print("GAMEOVER STATE")
        board = []
        for i in range(0, 20):
            toPrint = []
            for j in range(0, 10):
                if self.playerLoc[0] == i and self.playerLoc[1] ==j:
                    toPrint.append("P")
                else:
                    toPrint.append(str(self.board[i][j]))
            if print_to_screen:
                toPrint = [" _ " if x == "0" else x for x in toPrint ]
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
    def compareBoard(self, other):
        for i in range(0, 20):
            if self.board[i] != other.board[i]:
                return False
        return True

    def __hash__(self):
        total = 0
        total += self.playerLoc[0] * 2 + self.playerLoc[1] * 3
        total *= 10
        total += sum(self.holding) 
        total *= 10
        total += self.tankSize
        total *= 10 
        total += self.oxygenLeft + self.timeLeft
        total += self.cash * 12
        return total 

    def __eq__(self,other):
        if self.gameOver != other.gameOver:
            return False
        if self.gameOver:
            return self.tankSize == other.tankSize and self.cash == other.cash and self.timeLeft == other.timeLeft and self.oxygenLeft == self.oxygenLeft and self.playerLoc == self.playerLoc and self.holding == other.holding and self.compareBoard(other)
        else:
            return self.cash == other.cash and self.timeLeft == other.timeLeft and self.oxygenLeft == other.oxygenLeft and \
            sum(self.holding) == sum(other.holding) and self.playerLoc == other.playerLoc and self.tankSize == other.tankSize and \
            self.compareBoard(other) and self.tanks == other.tanks and self.gameOver == other.gameOver

    def __repr__(self):
        s="Cash: %d"%(self.cash)
        return s




