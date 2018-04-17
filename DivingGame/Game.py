from divegame import diveGame


def manDist(A, B):
    return abs(A[0] - B[0]) + abs(A[1] - B[1])
class Game: 
    def __init__(self):
        self.gameState = diveGame(board = None, playerLoc = (0,0), holding = [], cash = 0, gameOver = False)
    def humanPlay(self):
        reward = 0
        while True:
            if self.gameState.isOver():
                print()
                print("FINAL REWARD:", reward)
                return
            self.gameState.printBoard()
            actions = [(a,b) for a,b in enumerate(self.gameState.getLegalActions())]
            print()
            print('ACTIONS')
            for x,y in actions:
                if y[2] == "exit":
                    print(x, "exit")
                if y[2] == "tank":
                    print(x, "buy tank:", y[1], "for cost:", y[0])
                if y[2] == "move": 
                    print(x, "move:", y[:2])
            a = int(input())           
            nxt = self.gameState.getSuccessor(actions[a][1])
            self.gameState = nxt[0]
            reward += nxt[1]
game = Game()
game.humanPlay()
