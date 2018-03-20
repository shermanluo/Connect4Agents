def euclidDist(A, B):
	return pow(pow(A[0] - B[0], 2) + pow(A[1] - B[1], 2), 0.5)
def boardCopy(board):
	copy = []
	for i in board:
		copy.append(i[:])
	return copy
def doubleSwitch(double):
	if double == (0,0):
		return (10,10)
	return (0,0)
class gridGame:
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
	#(0,10) is defined at top right
	#(10, 0) is defined as bottom left
	#player starts at (0,0)
	def __init__(self, board = None, holding = None, double = (10,10), playerLoc = (0,0)):
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

	def getLegalActions(self):
		if self.holding:
			return [(0,0), (10,10)]
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
				return (gridGame(boardCopy(self.board), None, doubleSwitch(self.double), action), reward)
			else:
				reward = h - dist
				return (gridGame(boardCopy(self.board), None, self.double, action), reward)

		h = self.board[action[0]][action[1]]
		newBoard = boardCopy(self.board)
		newBoard[action[0]][action[1]] = 0
		return (gridGame(newBoard, h, self.double, action), - dist)

	def isOver(self):
		return len(self.getLegalActions()) == 0

	def printBoard(self):
		for i in range(0, 10):
			toPrint = []
			for j in range(0, 10):
				if self.playerLoc[0] == i and self.playerLoc[1] ==j:
					toPrint.append("P ")
				else:
					toPrint.append(str(self.board[i][j]) + " ")
			print(toPrint)

				
		







