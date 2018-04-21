#!/usr/bin/env python
import random
import math
import hashlib
import logging
import argparse
from divegame import diveGame
import pdb

#MCTS scalar.  
SCALAR= 4500

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('MyLogger')

class State:
    def __init__(self):
            self.gs = diveGame()

    def terminal(self):
        return self.gs.isOver()

    def next_state(self):
        move=random.choice([x for x  in self.gs.getLegalActions()])
        nxt = self.gs.getSuccessor(move)
        new = State()
        new.gs = nxt[0]
        return new, move

    def reward(self):
        r = self.gs.cash
        return r
    def __hash__(self):
        return self.gs.__hash__()
    def __eq__(self,other):
        return self.gs.__eq__(other.gs)
    def __repr__(self):
        return self.gs.__repr__()
  

class Node():
    def __init__(self, state, parent=None):
        self.visits=1
        self.reward=0.0 
        self.state=state
        self.children=[]
        self.parent=parent  
    def add_child(self,child_state, move):
        child=Node(child_state,self)
        self.children.append((child, move))
        return child
    def update(self,reward):
        self.reward=reward
        self.visits+=1
    def fully_expanded(self):
        if len(self.children)==len(self.state.gs.getLegalActions()):
            return True
        return False
    def __repr__(self):
        s="Node; children: %d; visits: %d; Projected reward: %f"%(len(self.children),self.visits,self.reward)
        return s
    def __eq__(self, other):
        if other == None:
            return False
        return self.state == other.state
        


def UCTSEARCH(budget,root):
    #print("searching...")
    for iter in range(int(budget)):
        if iter%10000==9999:
            logger.info("simulation: %d"%iter)
            logger.info(root)
        front=TREEPOLICY(root)
        reward, front =DEFAULTPOLICY(front)
        BACKUP(front,reward)
    return BESTCHILD(root,0, True)

def TREEPOLICY(node):
    #a hack to force 'exploitation' in a game where there are many options, and you may never/not want to fully expand first
    while node.state.terminal()==False:
        if len(node.children)==0:
            return EXPAND(node)
        elif random.uniform(0,1)<.5:
            node=BESTCHILD(node,SCALAR)
        else:
            if node.fully_expanded()==False:    
                return EXPAND(node)
            else:
                node=BESTCHILD(node,SCALAR)
    return node

def EXPAND(node):
    tried_children=[d for c, d in node.children]
    new_state, move =node.state.next_state()
    while move in tried_children:
        new_state, move=node.state.next_state()
    node.add_child(new_state, move)
    return node.children[-1][0]

#current this uses the most vanilla MCTS formula it is worth experimenting with THRESHOLD ASCENT (TAGS)
def BESTCHILD(node,scalar, action = False):
    bestscore= 0
    bestchildren = []
    if len(node.children) == 0:
        print(node.state.gs.gameOver)
        node.state.gs.printBoard()
    for c, d in node.children:
        exploit=c.reward
        explore=math.sqrt(2.0*math.log(node.visits)/float(c.visits))    
        score=exploit+scalar*explore
        if score==bestscore:
            bestchildren.append((c, d))
        if score>bestscore:
            bestchildren=[(c, d)]
            bestscore=score
    if len(bestchildren)==0:
        logger.warn("OOPS: no best child found, probably fatal")
    if action:
        return random.choice(bestchildren)
    return random.choice(bestchildren)[0]

def DEFAULTPOLICY(node):
    while node.state.terminal()==False:
        state, action = node.state.next_state()
        if Node(state) in node.children:
            node = [x for x in node.children if Node(state) == x]
        else:
            node = node.add_child(state, action)
    return node.state.reward(), node

def BACKUP(node,reward):
    while node!=None:
        node.visits+=1
        node.reward = max(reward, node.reward)
        node=node.parent
    return


def getRollout(diveGame, num_sims):
    rollout = []
    scores = []
    states = []
    states.append(diveGame)
    scores.append(diveGame.cash)
    state = State()
    state.gs = diveGame
    node = Node(state)
    startNode = node
    startNode.reward = startNode.state.gs.cash
    if diveGame.isOver():
        return [diveGame], [], [diveGame.cash], startNode
    rollout = []
    scores = []
    states = []
    states.append(diveGame)
    scores.append(diveGame.cash)
    state = State()
    state.gs = diveGame
    node = Node(state)
    startNode = node
    while not node.state.gs.isOver():
        UCTSEARCH(num_sims, node)
        node, action = BESTCHILD(node, 0, True)
        rollout.append(action)
        states.append(node.state.gs)
        scores.append(node.state.gs.cash)
        num_sims = 1000
        count += 1
    return states, rollout, scores, startNode




if __name__=="__main__":
    parser = argparse.ArgumentParser(description='MCTS research code')
    parser.add_argument('--num_sims', action="store", required=True, type=int)
    args=parser.parse_args()
    s = State()
    nxt = s.gs.getSuccessor((2, 0, "move"))
    s = nxt[0]
    nxt = s.getSuccessor((0, 5, "move"))
    s = nxt[0]
    state = State()
    state.gs = s
    current_node=Node(State())
    current_node.state.gs.printBoard()
    while not current_node.state.gs.isOver():
        temp, action=UCTSEARCH(args.num_sims,current_node)
        print("Num Children: %d"%len(current_node.children))
        for i,c in enumerate(current_node.children):
            print(i,c)
        print("Best Child: %s"%current_node.state)
        current_node = temp
        current_node.state.gs.printBoard()
        print("--------------------------------")   
            