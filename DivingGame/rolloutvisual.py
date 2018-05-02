from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.paths import Path
from asciimatics.sprites import Sprite
from asciimatics.renderers import StaticRenderer
from asciimatics.event import KeyboardEvent, MouseEvent
import time
from random import randint
import math

def printActions(gameState, actions):
    aIter = iter(actions)
    curr = ''
    while True:
        action = next(aIter, None)
        if not action:
            curr += "|DIED"
            print(curr)
            return
        elif action[2] == "exit":
            curr += "|EXIT"
            print(curr)
            return
        elif action in {(0,0, "move"),(0,5, "move"),(0,9, "move")}:
            if action == (0,0, "move"):
                drop = "Top Left"
            elif action == (0, 5, "move"):
                drop = "Top Middle"
            elif action == (0, 9, "move"):
                drop = "Top Right"
            curr += "|" + drop
        elif action[2] == "tank":
            curr += "|tank: " + str(action[1])
        else:
            curr += "|" + str(gameState.board[action[0]][action[1]])

def helper(screen, rollout, info): #START: ASK FOR FOUR MOVES 
    screen.print_at("ACTIONS: " + info,3, 2)
    for gs2 in rollout:
        time.sleep(0.5)
        h = 3
        for i in range(20):
            screen.print_at('+---+---+---+---+---+---+---+---+---+---+',3, h, colour=Screen.COLOUR_WHITE)
            h += 1
            screen.print_at('|   |   |   |   |   |   |   |   |   |   |',
                                 3, 
                                 h,
                                 colour=Screen.COLOUR_WHITE)
            h += 1
        for i in range(0, 10):
            for j in range(0, 20):
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
        screen.print_at('+---+---+---+---+---+---+---+---+---+---+',
                                 3, 
                                 h,
                                 colour=Screen.COLOUR_WHITE)
        screen.print_at('HOLDING: ' + str(gs2.holding) + "                               ",
                                3, 
                                h + 1)
        screen.print_at('Time Left: ' + str(gs2.timeLeft) + "                   ",
                                3,  
                                h + 2)
        screen.print_at('Oxygen: ' + str(gs2.oxygenLeft) + "                   ",
                                3, 
                                h + 3)
        screen.print_at('Tank Size: ' + str(gs2.tankSize) + "                             ",
                                3, 
                                h + 4)
        screen.print_at('cash: ' + str(gs2.cash) + "                                    ",
                                3, 
                                h + 5)
        screen.refresh()
        while True:
            time.sleep(0.1)
            if isinstance(screen.get_event(), KeyboardEvent):
                break
def visualize(rollout, info):
    Screen.wrapper(helper, arguments = [rollout, info])