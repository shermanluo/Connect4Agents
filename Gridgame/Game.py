

from Agent import MaxAgent, QSolveAgent
from gridGame import gridGame
import itertools
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.paths import Path
from asciimatics.sprites import Sprite
from asciimatics.renderers import StaticRenderer
from asciimatics.event import KeyboardEvent, MouseEvent
import time

from random import randint
import math

def euclidDist(A, B):
    return abs(A[0] - B[0]) + abs(A[1] - B[1])
class Game: 

    def __init__(self):
        # first option
        self.gameState = gridGame(3,     [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 20, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 6, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                  double=(0,9), playerLoc=(0,0))
    def humanPlay(self):
        reward = 0
        while True:
            self.gameState.printBoard()
            print(self.gameState.getLegalActions())
            print("Reward: ", reward)
            if self.gameState.isOver():
                return
            a = int(input())
            b = int(input())                
            nxt = self.gameState.getSuccessor((a, b))
            self.gameState = nxt[0]
            reward += nxt[1]
    def agentPlay(self):
        reward = 0
        agent = MaxAgent()
        actions = agent.value(self.gameState)[1]
        while True:
            self.gameState.printBoard()
            print("Reward: ", reward)
            if self.gameState.isOver():
                return
            action = actions.pop(0)
            nxt = self.gameState.getSuccessor(action)
            self.gameState = nxt[0]
            reward += nxt[1]

    def agentSolve(self, return_score=False):
        agent = QSolveAgent()
        agent.value(self.gameState)
        if return_score:
            return agent.Qvalues, agent.scores, agent.rewards
        return agent.Qvalues

    def exploreTree(self):
        Qvalues = self.agentSolve()
        stack = []   #stack keeps track of previous states
        start = self.gameState
        curr = self.gameState
        while True:
            print()
            curr.printBoard()
            if start == curr: 
                print("Start of game, don't type -1")
            if (curr.holding):
                print("Holding: ", curr.holding)
                print("Choose where to place it. To return to previous state, type -1.")
            else:
                print('Go pick up a piece!')
                print("Type the index of your action. To return to previous state, type -1.")
            actions = curr.getLegalActions()
            for i, action in enumerate(actions):
                print(i, action, "| Distance: ~", format(euclidDist(action, curr.playerLoc), '.2f'), "| QValue: ~", format(Qvalues[(curr, action)], '.2f'))
            if not actions:
                print("game is done!")

            request = input()
            if request == -2:
                return
            if int(request) == -1:
                curr = stack.pop()
                continue
            stack.append(curr)
            curr = curr.getSuccessor(actions[int(request)])[0]

    def jsonSearchTree(self, output_fname="gridgame_qvals.json"):
        # Generate search tree in json format, for visualization
        import json
        Qvalues, scores, rewards = self.agentSolve(return_score=True)

        tree = {}
        start = self.gameState
        tree["user_id"] = "\n".join([" ".join(x) \
                                     for x in start.printBoard(print_to_screen=False)])
        tree["name"] = tree["user_id"]
        tree["children"] = []

        stack = [(start, tree)]
        curr = self.gameState
        while len(stack) > 0:
            curr, curr_tree = stack.pop()
            actions = curr.getLegalActions()
            if not actions:
                continue
            for action in actions:
                child = curr.getSuccessor(action)[0]
                child_tree = {}
                child_tree["user_id"] = \
                        "\n".join([" ".join(x)
                                   for x in child.printBoard(print_to_screen=False)])
                prefix = "Place at "
                if not curr.holding:
                    val = curr.board[action[0]][action[1]]
                    prefix = "Pick up " + str(val) + " at "
                child_tree["name"] = prefix + str(action) + ": " + \
                                     format(Qvalues[(curr, action)], '.2f') + \
                                     " [Reward: " + \
                                     format(rewards[(curr, action)], '.2f') + \
                                     ", Total: " + \
                                     format(scores[(curr, action)], '.2f') + "]"
                child_tree["children"] = []

                curr_tree["children"].append(child_tree)
                stack.append((child, child_tree))

        with open(output_fname, 'w') as outfile:
            json.dump(tree, outfile, indent=2)


    def visual(self):
        qValues, scores, rewards = game.agentSolve(True)
        actions = []
        gs2 = None
        s2 = 0
        gs1 = game.gameState
        s1 = 0
        def test(screen): #START: ASK FOR FOUR MOVES 
            nonlocal gs2
            gs = game.gameState
            h = 3
            screen.print_at('CLICK FOUR VALID MOVES',
                            3, 
                            2)
            for i in range(10):
                screen.print_at('+---+---+---+---+---+---+---+---+---+---+',
                             3, 
                             h,
                             colour=Screen.COLOUR_WHITE)
                h += 1
                screen.print_at('|   |   |   |   |   |   |   |   |   |   |',
                             3, 
                             h,
                             colour=Screen.COLOUR_WHITE)
                h += 1
            for i in range(0, 10):
                for j in range(0, 10):
                    if gs.playerLoc[0] == j and gs.playerLoc[1] == i:             
                        screen.print_at(str('P'),
                                         4 + 4*i, 
                                         4 + 2*j,
                                         colour=Screen.COLOUR_WHITE,
                                         bg=Screen.COLOUR_RED)
                    elif gs.board[j][i]:             
                        screen.print_at(str(gs.board[j][i]),
                                         4 + 4*i, 
                                         4 + 2*j,
                                         colour=Screen.COLOUR_WHITE,
                                         bg=Screen.COLOUR_BLACK)
                    elif gs.double[0] == j and gs.double[1] == i:
                        screen.print_at(str('2'),
                                         4 + 4*i, 
                                         4 + 2*j,
                                         colour=Screen.COLOUR_YELLOW)
            screen.print_at('+---+---+---+---+---+---+---+---+---+---+',
                             3, 
                             h,
                            colour=Screen.COLOUR_WHITE)
            screen.print_at('HOLDING: ' + str(gs.holding) + "     ",
                            3, 
                            h + 1)
            screen.refresh()
            while (len(actions) < 4):
                click = screen.get_event()
                if isinstance(click, MouseEvent) and click.buttons and MouseEvent.LEFT_CLICK != 0:
                    click.y = click.y - 4
                    click.y = math.floor(float(click.y) / 2)
                    click.x = click.x - 4
                    click.x = math.floor(float(click.x) / 4)
                    actions.append((click.y, click.x))
                elif isinstance(click, MouseEvent):
                    click.y = click.y - 4
                    click.y = math.floor(float(click.y) / 2)
                    click.x = click.x - 4
                    click.x = math.floor(float(click.x) / 4)
                    screen.print_at('MOUSEPOS: ' + '(' + str(click.y) + ' ' + str(click.x) + ')' + "     ",
                            3, 
                            h + 2)
                s = ''
                for action in actions:
                    s += str(action) + " "
                screen.print_at(s, 3, h + 3)
                screen.refresh()
            time.sleep(1)
            nonlocal s2
            gs2 = game.gameState
            for action in actions:
                h = 3
                screen.print_at('TAKING YOUR ACTIONS               ',
                                3, 
                                2)
                for i in range(10):
                    screen.print_at('+---+---+---+---+---+---+---+---+---+---+',3, h, colour=Screen.COLOUR_WHITE)
                    h += 1
                    screen.print_at('|   |   |   |   |   |   |   |   |   |   |',
                                         3, 
                                         h,
                                         colour=Screen.COLOUR_WHITE)
                    h += 1
                for i in range(0, 10):
                    for j in range(0, 10):
                        if gs2.playerLoc[0] == j and gs2.playerLoc[1] == i:             
                            screen.print_at(str('P'),
                                                     4 + 4*i, 
                                                     4 + 2*j,
                                                     colour=Screen.COLOUR_WHITE,
                                                     bg=Screen.COLOUR_RED)
                        elif gs2.board[j][i]:             
                                    screen.print_at(str(gs2.board[j][i]),
                                                     4 + 4*i, 
                                                     4 + 2*j,
                                                     colour=Screen.COLOUR_WHITE,
                                                     bg=Screen.COLOUR_BLACK)
                        elif gs2.double[0] == j and gs2.double[1] == i:
                                    screen.print_at(str('2'),
                                                     4 + 4*i, 
                                                     4 + 2*j,
                                                     colour=Screen.COLOUR_YELLOW)
                screen.print_at('+---+---+---+---+---+---+---+---+---+---+',
                                         3, 
                                         h,
                                         colour=Screen.COLOUR_WHITE)
                screen.print_at('HOLDING: ' + str(gs2.holding) + "     ",
                                        3, 
                                        h + 1)
                screen.print_at('SCORE: ' + format(s2, '.2f') + "                      ",
                                        3, 
                                        h + 2)
                if gs2 == game.gameState:
                    screen.print_at('START                                     ',
                                        3, 
                                        h + 3,
                                        bg=Screen.COLOUR_RED)
                else:
                    screen.print_at('                                               ',
                                        3, 
                                        h + 3)
            

                nxt = gs2.getSuccessor(action)
                gs2 = nxt[0]
                s2 += nxt[1]
                screen.refresh()
                time.sleep(3)
            nonlocal gs1
            nonlocal s1
            count = 0
            while gs1.getLegalActions() and count < 4:
                h = 3
                screen.print_at('TAKING OPTIMAL ACTIONS FOR FOUR STEPS               ',
                                3, 
                                2)
                for i in range(10):
                    screen.print_at('+---+---+---+---+---+---+---+---+---+---+',3, h, colour=Screen.COLOUR_WHITE)
                    h += 1
                    screen.print_at('|   |   |   |   |   |   |   |   |   |   |',
                                         3, 
                                         h,
                                         colour=Screen.COLOUR_WHITE)
                    h += 1
                for i in range(0, 10):
                    for j in range(0, 10):
                        if gs1.playerLoc[0] == j and gs1.playerLoc[1] == i:             
                            screen.print_at(str('P'),
                                                     4 + 4*i, 
                                                     4 + 2*j,
                                                     colour=Screen.COLOUR_WHITE,
                                                     bg=Screen.COLOUR_RED)
                        elif gs1.board[j][i]:             
                                    screen.print_at(str(gs1.board[j][i]),
                                                     4 + 4*i, 
                                                     4 + 2*j,
                                                     colour=Screen.COLOUR_WHITE,
                                                     bg=Screen.COLOUR_BLACK)
                        elif gs1.double[0] == j and gs1.double[1] == i:
                                    screen.print_at(str('2'),
                                                     4 + 4*i, 
                                                     4 + 2*j,
                                                     colour=Screen.COLOUR_YELLOW)
                screen.print_at('+---+---+---+---+---+---+---+---+---+---+',
                                         3, 
                                         h,
                                         colour=Screen.COLOUR_WHITE)
                screen.print_at('HOLDING: ' + str(gs1.holding) + "     ",
                                        3, 
                                        h + 1)
                screen.print_at('SCORE: ' + format(s1, '.2f') + "                      ",
                                        3, 
                                        h + 2)
                if gs1 == game.gameState:
                    screen.print_at('START                                     ',
                                        3, 
                                        h + 3,
                                        bg=Screen.COLOUR_RED)
                else:
                    screen.print_at('                                               ',
                                        3, 
                                        h + 3)
                moves = gs1.getLegalActions()
                bact = max(moves, key = lambda x: qValues[(gs1, x)])
                nxt = gs1.getSuccessor(bact)
                gs1 = nxt[0]
                s1 += nxt[1]
                screen.refresh()
                count += 1
                time.sleep(3)
        Screen.wrapper(test)
        def visualGame(screen): #VISUAL COMPARISON
            def compareLeaves(gs1, gs2):
                start1 = gs1
                start2 = gs2
                score1 = s1
                score2 = s2
                while True:
                    h = 3
                    screen.print_at('OPTIMAL LEAF',
                            3, 
                            2)
                    for i in range(10):
                        screen.print_at('+---+---+---+---+---+---+---+---+---+---+',
                                     3, 
                                     h,
                                     colour=Screen.COLOUR_WHITE)
                        h += 1
                        screen.print_at('|   |   |   |   |   |   |   |   |   |   |',
                                     3, 
                                     h,
                                     colour=Screen.COLOUR_WHITE)
                        h += 1
                    for i in range(0, 10):
                        for j in range(0, 10):
                            if gs1.playerLoc[0] == j and gs1.playerLoc[1] == i:             
                                screen.print_at(str('P'),
                                                 4 + 4*i, 
                                                 4 + 2*j,
                                                 colour=Screen.COLOUR_WHITE,
                                                 bg=Screen.COLOUR_RED)
                            elif gs1.board[j][i]:             
                                screen.print_at(str(gs1.board[j][i]),
                                                 4 + 4*i, 
                                                 4 + 2*j,
                                                 colour=Screen.COLOUR_WHITE,
                                                 bg=Screen.COLOUR_BLACK)
                            elif gs1.double[0] == j and gs1.double[1] == i:
                                screen.print_at(str('2'),
                                                 4 + 4*i, 
                                                 4 + 2*j,
                                                 colour=Screen.COLOUR_YELLOW)
                    screen.print_at('+---+---+---+---+---+---+---+---+---+---+',
                                     3, 
                                     h,
                                     colour=Screen.COLOUR_WHITE)
                    screen.print_at('HOLDING: ' + str(gs1.holding) + "     ",
                                    3, 
                                    h + 1)
                    screen.print_at('SCORE: ' + format(score1, '.2f'),
                                    3, 
                                    h + 2)
                    if gs1 == start1:
                        screen.print_at('START',
                                    3, 
                                    h + 3,
                                    bg=Screen.COLOUR_RED)
                    elif not gs1.getLegalActions():
                        screen.print_at('END   ',
                                    3, 
                                    h + 3,
                                    bg=Screen.COLOUR_RED)
                    else:
                        screen.print_at('      ',
                                    3, 
                                    h + 3)
                    actions = [action for action in gs1.getLegalActions()]
                    if actions:
                        bact = max(actions, key = lambda x: qValues[(gs1, x)])
                        nxt = gs1.getSuccessor(bact)
                        gs1 = nxt[0]
                        score1 += nxt[1]
                    else:
                        gs1 = start1
                        score1 = s1


                    h = 3
                    screen.print_at("YOUR LEAF",
                            50, 
                            2)
                    for i in range(10):
                        screen.print_at('+---+---+---+---+---+---+---+---+---+---+',
                                     50, 
                                     h,
                                     colour=Screen.COLOUR_WHITE)
                        h += 1
                        screen.print_at('|   |   |   |   |   |   |   |   |   |   |',
                                     50, 
                                     h,
                                     colour=Screen.COLOUR_WHITE)
                        h += 1
                    for i in range(0, 10):
                        for j in range(0, 10):
                            if gs2.playerLoc[0] == j and gs2.playerLoc[1] == i:             
                                screen.print_at(str('P'),
                                                 51 + 4*i, 
                                                 4 + 2*j,
                                                 colour=Screen.COLOUR_WHITE,
                                                 bg=Screen.COLOUR_RED)
                            elif gs2.board[j][i]:             
                                screen.print_at(str(gs2.board[j][i]),
                                                 51 + 4*i, 
                                                 4 + 2*j,
                                                 colour=Screen.COLOUR_WHITE,
                                                 bg=Screen.COLOUR_BLACK)
                            elif gs2.double[0] == j and gs2.double[1] == i:
                                screen.print_at(str('2'),
                                                 51 + 4*i, 
                                                 4 + 2*j,
                                                 colour=Screen.COLOUR_YELLOW)
                    screen.print_at('+---+---+---+---+---+---+---+---+---+---+',
                                     50, 
                                     h,
                                     colour=Screen.COLOUR_WHITE)
                    screen.print_at('HOLDING: ' + str(gs2.holding) + "     ",
                                    50, 
                                    h + 1)
                    screen.print_at('SCORE: ' + format(score2, '.2f'),
                                    50, 
                                    h + 2)
                    if gs2 == start2:
                        screen.print_at('START',
                                    50, 
                                    h + 3,
                                    bg=Screen.COLOUR_RED)
                    elif not gs2.getLegalActions():
                        screen.print_at('END   ',
                                    50, 
                                    h + 3,
                                    bg=Screen.COLOUR_RED)
                    else:
                        screen.print_at('      ',
                                    50, 
                                    h + 3)
                    actions = [action for action in gs2.getLegalActions()]
                    if actions:
                        bact = max(actions, key = lambda x: qValues[(gs2, x)])
                        nxt = gs2.getSuccessor(bact)
                        gs2 = nxt[0]
                        score2 += nxt[1]
                    else:
                        gs2 = start2
                        score2 = s2
                    screen.refresh()
                    time.sleep(3)
            compareLeaves(gs1, gs2)
        Screen.wrapper(visualGame)



game = Game()
game.agentSolve()
#game.agentPlay()
#game.visual()
#game.jsonSearchTree()  # generates json file for visualization purposes
#game.exploreTree()
