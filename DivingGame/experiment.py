from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, PhotoImage
import tkinter
from divegame import diveGame
import time
import pickle

def manDist(A, B):
    return abs(A[0] - B[0]) + abs(A[1] - B[1])


class Experiment:

    def __init__(self, master):
        self.filename = str(input())
        master.minsize(2000,1000)
        self.state = diveGame()
        self.master = master
        master.title("Calculator")

        self.topLabel = Label(master, text = "", font = ("Helvetica", 40))
        self.topLabel.grid(row=0, column = 25)

        self.lbl = Label(master, text="Click on a valid location to prepare your next move. If a tank is available and you are surfaced then you can purchase it.", font=("Helvetica", 25))
        self.lbl.grid(row = 5, column=25)

        self.var = tkinter.IntVar()
        self.showing = False


        f = open('store.pckl', 'rb')
        rR, rS, hR, hS, rA, hA = pickle.load(f)
        #self.showRollout(rR)
        self.playGame()


    def displayBoard(self, playing = True):
        if playing:
            self.lbl.config( text="Click on a valid location to prepare your next move. If a tank is available and you are surfaced then you can purchase it.")




        try:
            self.exit.destroy()
        except:
            pass
        tanks = [tank for tank in self.state.tanks]

        self.cash = Label(self.master, text = "     Cash: " + str(self.state.cash) + "     ", font = ("Helvetica", 18))
        self.cash.grid(row = 15, column = 25)
        self.time = Label(self.master, text = "    Time: " + str(self.state.timeLeft) + "     ", font = ("Helvetica", 18))
        self.time.grid(row = 16, column = 25)
        self.oxygen = Label(self.master, text = "        Oxygen Left: " + str(self.state.oxygenLeft) + "       ", font = ("Helvetica", 18))
        self.oxygen.grid(row = 17, column = 25)

        def clickTank(action):
            def executeMove():
                def do():
                    self.var.set(1)
                    self.move = action
                if not self.showing:    
                    if  (self.state.playerLoc == (0,0) or self.state.playerLoc == (0,5) or self.state.playerLoc == (0,9)) and self.state.cash >= action[1]:
                        self.lbl.config(text = "Tank | Cost: " + str(action[0]) + " | Size: " + str(action[1]))
                        self.next = Button(self.master, text="Execute Move", font = ("Helvetica", 18), command = do)
                        self.next.grid(row = 6, column=25)
                    else:
                        self.lbl.config(text = "Cannot Buy Tank")
            return executeMove
        c = 0
        for tank in tanks:
            t = Button(self.master, text = "Tank | Cost: " + str(tank[0]) + " | Size: " + str(tank[1]), font = ("Helvetica", 18), command = clickTank(tank))
            t.grid(row = 10 + c, column = 25)
            c += 1


        if self.state.playerLoc == (0,0) or self.state.playerLoc == (0,5) or self.state.playerLoc == (0,9) and playing:
            def exit():
                self.move = (None, None, 'exit')
                self.var.set(1) 
            print("EXIT")
            self.exit = Button(self.master, text = "EXIT with all your current cash! ", font = ("Helvetica", 18), command = exit)
            self.exit.grid(row = 19, column = 25)


        for i in range(0, 20):
            for j in range(0, 10):
                color = "white"
                if self.state.board[i][j]:
                    color = "Gray"
                    text = str(self.state.board[i][j])
                elif (i, j) == (0,0) or (i, j) == (0,5) or (i, j) == (0,9):
                    text = "EXIT"
                    color = "Green"
                else:
                    text = ""


                if self.state.playerLoc == (i, j):
                    text = "P"
                    color = "Yellow"
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
                            if (i, j) == (0, 0) or (i, j) == (0, 5) or (i, j) == (0, 9):
                                valid = True
                                text = "Surface Location: " + str((i, j)) + "| distance is " + str(manDist((i, j), self.state.playerLoc))
                            if self.state.board[i][j]:
                                valid = True
                                text = "Pick up " + str(self.state.board[i][j])+ " at location " + str((i, j)) + " | distance is " + str(manDist((i, j), self.state.playerLoc))
                            if valid:
                                self.lbl.config(text = text)
                                self.next = Button(self.master, text="Execute Move", font = ("Helvetica", 18), command = executeMove(action))
                                self.next.grid(row = 6, column=25)


                    return do
                
                b.config(text = text, width="4",height="2",font=("Helvetica", 12), command = click((i, j, 'move')), background = color)

    def playGame(self):
        self.showing = False
        self.topLabel.config(text="YOU ARE PLAYING THE GAME")
        stateActions = []
        self.displayBoard()
        self.move = None
        while (not self.state.isOver()):
            action = self.displayBoard()
            root.wait_variable(self.var)
            stateActions.append((self.state, self.move))
            self.state = self.state.getSuccessor(self.move)[0]
            self.move = None
            self.var.set(0)
        f = open(self.filename, "wb")
        self.lbl.config(text="Game Over, Your Score: " + str(self.state.cash))
        self.topLabel.config(text="")
        pickle.dump((self.state.cash, stateActions), f)

    def showRollout(self, states):
        self.showing = True
        self.topLabel.config(text="YOU ARE OBSERVING A SERIES OF STATES IN A PLAN")
        self.nextState = tkinter.IntVar()
        def nextState():
            self.nextState.set(1)
        i = 0
        for state in states:
            self.lbl.config(text = "STATE NUMBER: " + str(i))
            self.state = state
            self.displayBoard(playing = False)
            self.nextStateButton = Button(self.master, text = "Next State", font = ("Helvetica", 18), command = nextState)
            self.nextStateButton.grid(row=6, column = 25)
            root.wait_variable(self.nextState)
            self.nextState.set(0)
            i += 1
        self.nextStateButton.destroy()
        self.topLabel.config(text="")



root = Tk()
my_gui = Experiment(root)
root.mainloop()



