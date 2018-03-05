class gameState:

	def getSuccessor(action):
		return


	def isFinished():
		return

class connectFourGS(gameState):
	wins = None
	''' connectFour Gamestate is represented by six python lists, each containing either a 1, 2, 
	representing pieces of different players. 
	    | 0 0 0 0 0 0 |
	    | 0 0 0 0 0 0 |
	    | 0 0 0 0 1 0 |
	    | 0 0 0 0 2 0 |
	    | 0 0 0 2 2 0 |
	    | 1 1 2 2 1 1 |
	is represented by:
	[[1]
	[1]
	[2]
	[2 2]
	[1 2 2 1]
	[1]
	[]]'''
	def __init__(self):
		self.board = [[],[],[],[],[],[]]
	def __init__(self, board):
		self.board = board
	#action is a number [0,6]
	#player is either player 1 or player 2
	def getSuccessor(self, player, action):
		if len(self.board[action]) == 6:
			return "INVALID MOVE"
		self.board[action].append(player)
		t = connectFourGS([self.board[0][:], self.board[1][:], self.board[2][:],
			self.board[3][:], self.board[4][:], self.board[5][:]])
		self.board[action].pop()
		return t
	def getLegalActions(self):
		actions = set()
		for i in range(6):
			if len(self.board[i]) < 6:
				actions.add(i)
		return actions
	def whoWins(self):
		#checking vertical win
		oneCount = 0
		twoCount = 0
		for i in range(6):
			column = self.board[i]
			for j in column:
				if j == 1:
					oneCount += 1
					twoCount = 0
				if j == 2:
					twoCount += 1
					oneCount = 0
				if oneCount == 4:
					return 1
				if twoCount == 4:
					return 2
			oneCount = 0
			twoCount = 0
		#checking horizontal win
		oneCount = 0
		twoCount = 0
		for i in range(6):
			for j in range(6):
				try:
					if self.board[j][i] == 1:
						oneCount += 1
						twoCount = 0
					if self.board[j][i] == 2:
						twoCount += 1
						oneCount = 0
					if oneCount == 4:
						return 1
					if twoCount == 4:
						return 2
				except:
					oneCount = 0
					twoCount = 0
			oneCount = 0
			twoCount = 0
		#checking diagonal win
		oneCount = 0
		twoCount = 0
		for i in range(0, 3):
			for j in range(0, 6 - i):
				try:
					if self.board[i + j][j] == 1:
						oneCount += 1
						twoCount = 0
					if self.board[i + j][j] == 2:
						twoCount += 1
						oneCount = 0
					if oneCount == 4:
						return 1
					if twoCount == 4:
						return 2
				except: 
					oneCount = 0
					twoCount = 0
			oneCount = 0
			twoCount = 0
		oneCount = 0
		twoCount = 0
		for i in range(1, 3):
			for j in range(0, 6 - i):
				try:
					if self.board[j][i + j] == 1:
						oneCount += 1
						twoCount = 0
					if self.board[j][i + j] == 2:
						twoCount += 1
						oneCount = 0
					if oneCount == 4:
						return 1
					if twoCount == 4:
						return 2
				except: 
					oneCount = 0
					twoCount = 0
			oneCount = 0
			twoCount = 0		
		oneCount = 0
		twoCount = 0
		for i in range(3, 6):
			for j in range(0, i + 1):
				try:
					if self.board[i - j][j] == 1:
						oneCount += 1
						twoCount = 0
					if self.board[i - j][j] == 2:
						twoCount += 1
						oneCount = 0
					if oneCount == 4:
						return 1
					if twoCount == 4:
						return 2
				except: 
					oneCount = 0
					twoCount = 0
			oneCount = 0
			twoCount = 0
		oneCount = 0
		twoCount = 0
		for i in range(1, 3):
			for j in reversed(range(i, 6)):
				try:
					if self.board[j][i + (5 - j)] == 1:
						oneCount += 1
						twoCount = 0
					if self.board[j][i + (5 - j)] == 2:
						twoCount += 1
						oneCount = 0
					if oneCount == 4:
						return 1
					if twoCount == 4:
						return 2
				except: 
					oneCount = 0
					twoCount = 0
			oneCount = 0
			twoCount = 0		
		for i in self.board:
			if len(i) < 6:
				return 0
		return 3 #TIE

	def isWin(self):
		if self.wins == 1 or self.wins == 3:
			return True
		self.wins = self.whoWins()
		return self.wins == 1 or self.wins == 3

	def isLose(self):
		if self.wins == 2 or self.wins == 3:
			return True
		self.wins = self.whoWins()
		return self.wins == 2 or self.wins == 3

class connectThreeGS(gameState):
	wins = None
	''' connectFour Gamestate is represented by 4 python lists, each containing either a 1, 2, 
	representing pieces of different players. 
	    | 0 0 0 0 |
	    | 0 0 0 0 |
	    | 0 0 0 2 |
	    | 1 1 2 2 |
	is represented by:
	[[1]
	[1]
	[2]
	[2 2]]'''
	def __init__(self, board):
		self.board = board
	#action is a number [0,6]
	#player is either player 1 or player 2
	def getSuccessor(self, player, action):
		if len(self.board[action]) == 4:
			return "INVALID MOVE"
		self.board[action].append(player)
		b = connectThreeGS([self.board[0][:], self.board[1][:], self.board[2][:],
			self.board[3][:]])
		self.board[action].pop()
		return b
	def getLegalActions(self, player):
		actions = set()
		for i in range(4):
			if len(self.board[i]) < 4:
				actions.add(i)
		return actions
	def whoWins(self):
		#checking vertical win
		oneCount = 0
		twoCount = 0
		for i in range(4):
			column = self.board[i]
			for j in column:
				if j == 1:
					oneCount += 1
					twoCount = 0
				if j == 2:
					twoCount += 1
					oneCount = 0
				if oneCount == 3:
					return 1
				if twoCount == 3:
					return 2
			oneCount = 0
			twoCount = 0
		#checking horizontal win
		oneCount = 0
		twoCount = 0
		for i in range(4):
			for j in range(4):
				try:
					if self.board[j][i] == 1:
						oneCount += 1
						twoCount = 0
					if self.board[j][i] == 2:
						twoCount += 1
						oneCount = 0
					if oneCount == 3:
						return 1
					if twoCount == 3:
						return 2
				except:
					oneCount = 0
					twoCount = 0
			oneCount = 0
			twoCount = 0
		#checking diagonal win
		board = []
		for column in self.board:
			copy = column[:]
			while len(copy) < 4:
				copy.append(0)
			board.append(copy)
		if (board[1][0] == 1 and board[2][1] == 1 and board[3][2] == 1) or (board[0][0] == 1 and board[1][1] == 1 and board[2][2] == 1) or (board[1][1] == 1 and board[2][2] == 1 and board[3][3] == 1) or (board[0][1] == 1 and board[1][2] == 1 and board[2][3] == 1) or (board[0][2] == 1 and board[1][1] == 1 and board[2][0] == 1) or (board[0][3] == 1 and board[1][2] == 1 and board[2][1] == 1) or (board[1][2] == 1 and board[2][1] == 1 and board[3][0] == 1) or (board[1][3] == 1 and board[2][2] == 1 and board[3][1] == 1):
			return 1
		if (board[1][0] == 2 and board[2][1] == 2 and board[3][2] == 2) or (board[0][0] == 2 and board[1][1] == 2 and board[2][2] == 2) or (board[1][1] == 2 and board[2][2] == 2 and board[3][3] == 2) or (board[0][1] == 2 and board[1][2] == 2 and board[2][3] == 2) or (board[0][2] == 2 and board[1][1] == 2 and board[2][0] == 2) or (board[0][3] == 2 and board[1][2] == 2 and board[2][1] == 2) or (board[1][2] == 2 and board[2][1] == 2 and board[3][0] == 2) or (board[1][3] == 2 and board[2][2] == 2 and board[3][1] == 2):
			return 2



		for i in self.board:
			if len(i) < 4:
				return 0
		return 3 #TIE

	def isWin(self):
		if self.wins == 1 or self.wins == 3:
			return True
		self.wins = self.whoWins()
		return self.wins == 1 or self.wins == 3

	def isLose(self):
		if self.wins == 2 or self.wins == 3:
			return True
		self.wins = self.whoWins()
		return self.wins == 2 or self.wins == 3

	def printBoard(self):
		for i in range(4):
			lst = []
			for j in range(4):
				try: 
					item = self.board[j][3 - i]
				except:
					item = 0
				lst.append(item)
			print(lst)




def test():
	board =[[1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1]]
	gs = connectFourGS(board)
	print(gs.isWin())
	print(gs.isLose())

	board =[[2, 2, 2, 2, 2, 2],
			[2, 2, 2, 2, 2, 2],
			[2, 2, 2, 2, 2, 2],
			[2, 2, 2, 2, 2, 2],
			[2, 2, 2, 2, 2, 2],
			[2, 2, 2, 2, 2, 2]]
	gs = connectFourGS(board)
	print(gs.isWin())
	print(gs.isLose())

	board = [[1, 2, 1, 2, 1, 2],
			 [1, 1, 1, 2, 1, 1],
			 [1, 2, 1, 1, 2, 2],
			 [2, 1, 2, 2, 2, 1],
			 [1, 2, 1, 1, 1, 2],
			 [2, 1, 1, 2, 1, 1]]
	gs = connectFourGS(board)
	print(gs.isWin())
	print(gs.isLose())

	board = [[1, 2, 1, 2, 1, 1],
			 [1, 1, 1, 2, 1, 2],
			 [1, 2, 2, 1, 2, 1],
			 [2, 1, 2, 1, 2, 1],
			 [1, 2, 2, 1, 1, 2],
			 [2, 1, 1, 2, 1, 1]]
	gs = connectFourGS(board)
	print(gs.isWin())
	print(gs.isLose())

	board = [[1, 2, 1, 2],
			 [2, 1, 2, 1],
			 [2, 1, 2, 1],
			 [1, 2, 1, 2]]
	gs = connectThreeGS(board)
	print(gs.isWin())
	print(gs.isLose())
	gs.printBoard()

#test()