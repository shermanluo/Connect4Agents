from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, PhotoImage
import tkinter
from divegame import diveGame
import time

def manDist(A, B):
    return abs(A[0] - B[0]) + abs(A[1] - B[1])


class Experiment:

    def __init__(self, master):
        master.minsize(2000,1000)
        self.state = diveGame()
        self.master = master
        master.title("Calculator")

        self.lbl = Label(master, text="Click on a valid location to prepare your next move. If a tank is available and you are surfaced then you can purchase it.", font=("Helvetica", 25))
        self.lbl.grid(row = 5, column=25)

        self.playGame()



    def displayBoard(self):
        self.lbl.config( text="Click on a valid location to prepare your next move. If a tank is available and you are surfaced then you can purchase it.")
        try:
            self.exit.destroy()
        except:
            pass
        tanks = [tank for tank in self.state.tanks]

        self.cash = Label(self.master, text = "Cash: " + str(self.state.cash), font = ("Helvetica", 18))
        self.cash.grid(row = 15, column = 25)
        self.time = Label(self.master, text = "Time: " + str(self.state.timeLeft), font = ("Helvetica", 18))
        self.time.grid(row = 16, column = 25)
        self.oxygen = Label(self.master, text = "        Oxygen Left: " + str(self.state.oxygenLeft) + "       ", font = ("Helvetica", 18))
        self.oxygen.grid(row = 17, column = 25)

        def clickTank(action):
            def executeMove():
                def do():
                    self.var.set(1)
                    self.move = action
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


        if self.state.playerLoc == (0,0) or self.state.playerLoc == (0,5) or self.state.playerLoc == (0,9):
            def exit():
                self.move = (None, None, 'exit')
                self.var.set(1) 
            print("EXIT")
            self.exit = Button(self.master, text = "EXIT with all your current cash! ", font = ("Helvetica", 18), command = exit)
            self.exit.grid(row = 19, column = 25)


        for i in range(0, 20):
            for j in range(0, 10):
                if self.state.board[i][j]:
                    text = str(self.state.board[i][j])
                elif (i, j) == (0,0) or (i, j) == (0,5) or (i, j) == (0,9):
                    text = "E"
                else:
                    text = ""


                if self.state.playerLoc == (i, j):
                    text = "P"
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
                
                b.config(text = text, width="4",height="2",font=("Helvetica", 12), command = click((i, j, 'move')))

    def playGame(self):
        self.displayBoard()
        self.var = tkinter.IntVar()
        self.move = None
        while (not self.state.isOver()):
            action = self.displayBoard()
            root.wait_variable(self.var)
            self.state = self.state.getSuccessor(self.move)[0]
            self.move = None
            self.var.set(0)
        self.lbl.config(text="Game Over, Your Score: " + str(self.state.cash))


root = Tk()
my_gui = Experiment(root)
root.mainloop()



