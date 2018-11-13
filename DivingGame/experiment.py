from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, PhotoImage
import tkinter
from divegame import diveGame, zeroBoard
import time
import pickle
from fatal_flaw import fatalFlaw
import pdb
from softmaxExplain import findStates2

def manDist(A, B):
    return abs(A[0] - B[0]) + abs(A[1] - B[1])

board1 = zeroBoard()
board1[1][9] = 11
board1[3][2] = 15
board1[3][9] = 12
board1[5][3] = 27
board1[7][8] =  24
board1[11][4] = 31
board1[13][4] = 52
board1[8][1] = 29
board1[14][2] = 131
board1[19][7] = 89

practiceBoard1 = diveGame(
    board = board1, 
    playerLoc = (0,0), 
    timeLeft = 85, 
    oxygenLeft = 25, 
    holding = [], 
    tankSize = 25, 
    cash = 0, 
    gameOver = False, 
    tanks = {(30, 30, "tank"), (70, 55, "tank")})

board2 = zeroBoard()
board2[1][3] = 31
board2[3][1] = 17
board2[4][9] = 25
board2[5][3] = 21
board2[7][8] =  40
board2[11][4] = 77
board2[13][2] = 54
board2[7][1] = 51
board2[12][6] = 131
board2[18][6] = 89


practiceBoard2 = diveGame(
    board = board2, 
    playerLoc = (0,0), 
    timeLeft = 80, 
    oxygenLeft = 30, 
    holding = [], 
    tankSize = 30, 
    cash = 0, 
    gameOver = False, 
    tanks = {(100, 40, "tank"), (150, 50, "tank")})





class Experiment:

    def __init__(self, master):
        print("Ask")
        self.filename = "playdata/" + str(input())
        master.maxsize(1600, 900)
        master.minsize(1600, 900)
        self.state = diveGame()
        self.master = master
        master.title("Calculator")

        self.topLabel = Label(master, text = "", font = ("Helvetica", 25))
        self.topLabel.grid(row=0, column = 15)

        self.lbl = Label(master, text="Click on a location to prepare a move. If a tank is available and you are surfaced then you can purchase it.", font=("Helvetica", 15))
        self.lbl.grid(row = 5, column=15)

        self.var = tkinter.IntVar()
        self.showing = False


        f = open('store.pckl', 'rb')
        rR, rS, hR, hS, rA, hA = pickle.load(f)
        #self.showRollout(rR)
        self.experiment()
        #self.playGame()


    def displayBoard(self, playing = True):
        if playing:
            self.lbl.config( text="Click on a location to prepare a move. If a tank is available and you are surfaced then you can purchase it.", fg = "black")
        if self.state.isOver():
            self.lbl.config(text = "GAMEOVER", fg = "red")
        tanks = [tank for tank in self.state.tanks]
        self.cash = Label(self.master, text = "     Cash: " + str(self.state.cash) + "     ", font = ("Helvetica", 15))
        self.cash.grid(row = 15, column = 15)
        self.time = Label(self.master, text = "    Time: " + str(self.state.timeLeft) + "     ", font = ("Helvetica", 15))
        self.time.grid(row = 16, column = 15)
        self.oxygen = Label(self.master, text = "        Oxygen Left: " + str(self.state.oxygenLeft) + "       ", font = ("Helvetica", 15))
        self.oxygen.grid(row = 17, column = 15)
        self.holding = Label(self.master, text = "     Holding: " + str(sum((self.state.holding))) + "     ", font = ("Helvetica", 15))
        self.holding.grid(row = 18, column = 15)
        if playing:
            def clickTank(action):
                def executeMove():
                    def do():
                        self.var.set(1)
                        self.move = action
                    if not self.showing:    
                        if  (self.state.playerLoc == (0,0) or self.state.playerLoc == (0,9)) and self.state.cash >= action[0]:
                            self.lbl.config(text = "Tank | Cost: " + str(action[0]) + " | Size: " + str(action[1]))
                            self.next = Button(self.master, text="Execute Move", font = ("Helvetica", 15), command = do)
                            self.next.grid(row = 6, column=15)
                        else:
                            print(self.state.cash, action[1])
                            self.lbl.config(text = "Cannot Buy Tank")
                return executeMove
        else:
            def clickTank(action):
                pass
        c = 0
        if playing:
            enabled = "normal"
        else:
            enabled = "disabled"
        self.tanks = []
        for tank in tanks:
            if tank in self.state.getLegalActions():
                t = Button(self.master, text = "Tank | Cost: " + str(tank[0]) + " | Size: " + str(tank[1]), font = ("Helvetica", 15), command = clickTank(tank), state = enabled)
                t.grid(row = 10 + c, column = 15)
                self.tanks.append(t)
                c += 1
            else:
                t = Button(self.master, text = "Tank | Cost: " + str(tank[0]) + " | Size: " + str(tank[1]), font = ("Helvetica", 15), command = clickTank(tank), state = enabled)
                t.config(state = "disabled")
                t.grid(row = 10 + c, column = 15)
                self.tanks.append(t)
                c += 1
        if self.state.playerLoc == (0,0) or self.state.playerLoc == (0,9) and playing:
            def exit():
                self.move = (None, None, 'exit')
                self.var.set(1) 
            print("EXIT")
            self.exit = Button(self.master, text = "EXIT with all your current cash! ", font = ("Helvetica", 15), command = exit, state = enabled)
            if not (self.state.playerLoc == (0, 0) or self.state.playerLoc == (0, 9)):
                seld.exit.config(state = "disabled")
            self.exit.grid(row = 19, column = 15)
        for i in range(0, 20):
            for j in range(0, 10):
                fg = "black"
                color = "white"
                font = ("Helvetica", 11)
                if i > 0:
                    color = "navy"
                if self.state.board[i][j]:
                    color = "Light Gray"
                    text = str(self.state.board[i][j])
                elif (i, j) == (0,0) or (i, j) == (0,9):
                    text = "EXIT"
                    color = "Green"
                else:
                    text = ""
                if self.state.playerLoc == (i, j):
                    text = "P"
                    fg = "brown4"
                    font = ("Helvetica", 10, "bold")
                if self.state.playerLoc == (i, j) and self.state.playerLoc[0] != 0: 
                    color = "white"
                b = Button(self.master)
                b.grid(row=i, column = j)
                b.row = i
                b.column = j
                def click(action):
                    i = action[0]
                    j = action[1]
                    def do():
                        valid = False
                        def executeMove(action):
                            def do():
                                print(action)
                                self.var.set(1)
                                self.move = action
                            return do 
                        if not self.showing:
                            if (i, j) == (0, 0) or (i, j) == (0, 9):
                                valid = True
                                text = "Surface Location: " + str((i, j)) + "| distance is " + str(manDist((i, j), self.state.playerLoc))
                            if self.state.board[i][j]:
                                valid = True
                                text = "Pick up " + str(self.state.board[i][j])+ " at location " + str((i, j)) + " | distance is " + str(manDist((i, j), self.state.playerLoc))
                            if valid:
                                self.lbl.config(text = text)
                                self.next = Button(self.master, text="Execute Move", font = ("Helvetica", 15), command = executeMove(action), state = enabled)
                                self.next.grid(row = 6, column=15)
                    return do    
                b.config(highlightthickness=0, text = text, width="3",height="2",font= font, fg = fg, command = click((i, j, "move")), background = color)


    def playGame(self):
        self.showing = False
        self.topLabel.config(text="                              YOU ARE PLAYING THE GAME                    ")
        stateActions = []
        states = []
        states.append(self.state)
        actions = []
        self.displayBoard()
        self.move = None
        while (not self.state.isOver()):
            self.displayBoard()
            root.wait_variable(self.var)
            if self.move not in self.state.getLegalActions():
                print(self.move, self.state.getLegalActions())
                raise Exception
            stateActions.append((self.state, self.move))
            actions.append(self.move)
            self.state = self.state.getSuccessor(self.move)[0]
            self.move = None
            self.var.set(0)
            states.append(self.state)
        f = open(self.filename, "wb")
        self.lbl.config(text="Game Over, Your Score: " + str(self.state.cash))
        self.topLabel.config(text="")
        pickle.dump((self.state.cash, stateActions), f)
        return actions, states

    def playStates(self, states):
        self.showing = False
        self.topLabel.config(text="                              Choose the next move in the state                    ")
        stateActions = []
        for state in states:
            self.state = state
            self.displayBoard()
            root.wait_variable(self.var)
            if self.move not in self.state.getLegalActions():
                raise Exception 
            stateActions.append((self.state, self.move))
            self.move = None
            self.var.set(0)
            for tank in self.tanks:
                print("GI")
                tank.destroy()
        return stateActions

    def showRollout(self, states):
        self.next.config(state = "disabled")
        self.exit.config(state = "disabled")
        self.showing = True
        self.topLabel.config(text="YOU ARE OBSERVING A SERIES OF STATES IN A PLAN")
        self.nextState = tkinter.IntVar()
        def nextState():
            self.nextState.set(1)
        for index, state in states:
            self.lbl.config(text = "STATE NUMBER: " + str(index), fg = "green")
            self.state = state
            self.displayBoard(playing = False)
            self.nextStateButton = Button(self.master, text = "Next State", font = ("Helvetica", 15), command = nextState)
            self.nextStateButton.grid(row=6, column = 16)
            root.wait_variable(self.nextState)
            self.nextState.set(0)
        self.nextStateButton.destroy()
        self.topLabel.config(text="")

    def showRolloutWithBack(self, states, ff = False):
        self.showing = True
        self.topLabel.config(text="YOU ARE OBSERVING A SERIES OF STATES IN A PLAN")
        self.nextState = tkinter.IntVar()
        def nextState():
            self.nextState.set(1)
            self.prev = False
        def prevState():
            self.nextState.set(1)
            self.prev  = True
        i = 0
        while i < len(states):
            if ff:
                if i == len(states) - 2:
                    self.topLabel.config(text = "                              Right before your Fatal Flaw", fg = "red")
                elif i == len(states) - 1:
                    self.topLabel.config(text = "                              Result of your Fatal Flaw", fg = "red")
                else:
                    self.topLabel.config(text=" YOU ARE OBSERVING A SERIES OF STATES IN A PLAN", fg = "black")

            index, state = states[i]
            self.lbl.config(text = "STATE NUMBER: " + str(index), fg = "green")
            self.state = state
            self.displayBoard(playing = False)

            self.nextStateButton = Button(self.master, text = "Next State", font = ("Helvetica", 15), command = nextState)
            self.nextStateButton.grid(row=6, column = 17)
            self.prevStateButton = Button(self.master, text = "Prev State", font = ("Helvetica", 15), command = prevState)
            self.prevStateButton.grid(row=6, column = 16)

            root.wait_variable(self.nextState)

            if self.prev:
                if i > 0:
                    i -= 1
            else:
                i += 1
            self.nextState.set(0)
        self.nextStateButton.config(state = 'disabled')
        self.prevStateButton.config(state = 'disabled')
        # self.nextStateButton.grid_forget()
        # self.prevStateButton.grid_forget()
        self.topLabel.config(text="")

    def experiment(self):
        # self.state = practiceBoard1
        # startState = self.state
        # actions, states = self.playGame()

        # rR, rS, hR, hS, rA, hA, flawIndex, group = fatalFlaw(startState, actions, threeGroups = True)
        # if not group:
        #     self.state = practiceBoard2 #<- FILLER
        #     startState = self.state
        #     actions, states = self.playGame()
        #     self.next.grid_forget()
        #     rR, rS, hR, hS, rA, hA, flawIndex, group = fatalFlaw(startState, actions, threeGroups = True)

        # print("Group:", group)

        group = 3

        if group:
            # idxs = findStates2(rR, rA)
            # def click():
            #     self.windowClick.set(1)
            # self.windowClick = tkinter.IntVar()
            # self.topLabel.config(text = "You will see where you made the biggest error. We start from the beginning.", fg = 'red')
            # self.topLabelButton = Button(self.master, text = 'Begin', font = ("Helvetica", 18), command = click)
            # self.topLabelButton.grid(row=1, column = 15)
            # root.wait_variable(self.windowClick)
            # self.topLabel.config(fg = 'black')

            # self.topLabelButton.config(state = 'disabled')

            # self.showRolloutWithBack([(x, y) for x, y in enumerate(states) if x < flawIndex + 2], ff = True)

            # self.topLabelButton.config(state = 'normal')
            # self.windowClick.set(0)
            # self.topLabel.config(text = "This is what you should have done instead!", fg = 'red')
            # root.wait_variable(self.windowClick)

            # self.topLabelButton.grid_forget()

            # self.topLabel.config(fg = 'black')
            # self.windowClick.set(0)

            # self.showRolloutWithBack([(x + flawIndex, y) for x, y in enumerate(rR) if x in idxs])


            if group == 1:
                f = open("group1States", "rb")
            if group == 2:
                f = open("group2States", "rb")
            if group == 3:
                f = open("group3States", "rb")
            tStates = reconstructStates(pickle.load(f))     
            stateActions = self.playStates(tStates)
            f = open(self.filename + "D", "wb")
            pickle.dump((states, actions, stateActions), f)
            pass


def reconstructStates(dicts):
    states = []
    for d in dicts:
        s = diveGame(
            board = d['board'], 
            playerLoc = d['playerLoc'], 
            timeLeft = d['timeLeft'], 
            oxygenLeft =d['oxygenLeft'], 
            holding = d['holding'], 
            tankSize = d['tankSize'], 
            cash = d['cash'], 
            gameOver = d['gameOver'], 
            tanks = d['tanks']
            )
        states.append(s)
    return states




if __name__ == "__main__":
    root = Tk()
    my_gui = Experiment(root)



