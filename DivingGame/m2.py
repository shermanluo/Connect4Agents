#!/usr/bin/env python
import random
import math
import hashlib
import logging
import argparse
from divegame import diveGame
import pdb

#MCTS scalar.  Larger scalar will increase exploitation, smaller will increase exploration. 
SCALAR= 50

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
    def update(self,reward):
        self.reward+=reward
        self.visits+=1
    def fully_expanded(self):
        if len(self.children)==len(self.state.gs.getLegalActions()):
            return True
        return False
    def __repr__(self):
        s="Node; children: %d; visits: %d; Average reward: %f"%(len(self.children),self.visits,self.reward / self.visits)
        return s
        


def UCTSEARCH(budget,root):
    for iter in range(int(budget)):
        if iter%10000==9999:
            logger.info("simulation: %d"%iter)
            logger.info(root)
        front=TREEPOLICY(root)
        reward=DEFAULTPOLICY(front.state)
        BACKUP(front,reward)
    return BESTCHILD(root,0)

def TREEPOLICY(node):
    #a hack to force 'exploitation' in a game where there are many options, and you may never/not want to fully expand first
    while node.state.terminal()==False:
        if len(node.children)==0:
            return EXPAND(node)
        elif random.uniform(0,1)<.5:
            node=BESTCHILD(node,SCALAR)
        else:
            if node.fully_expanded()==False:    
                ret = EXPAND(node)
                if ret == "exit":
                    print("exited")
                    node.expanded = True
                    return node
                return ret
            else:
                node=BESTCHILD(node,SCALAR)
    return node

def EXPAND(node):
    tried_children=[d for c, d in node.children]
    new_state, move =node.state.next_state()
    count = 0
    while move in tried_children:
        new_state, move=node.state.next_state()
        count += 1
    node.add_child(new_state, move)
    return node.children[-1][0]

#current this uses the most vanilla MCTS formula it is worth experimenting with THRESHOLD ASCENT (TAGS)
def BESTCHILD(node,scalar):
    bestscore= 0
    bestchildren = []
    if len(node.children) == 0:
        print(node.state.gs.gameOver)
        node.state.gs.printBoard()
    for c, d in node.children:
        exploit=c.reward/c.visits
        explore=math.sqrt(2.0*math.log(node.visits)/float(c.visits))    
        score=exploit+scalar*explore
        if score==bestscore:
            bestchildren.append(c)
        if score>bestscore:
            bestchildren=[c]
            bestscore=score
    if len(bestchildren)==0:
        logger.warn("OOPS: no best child found, probably fatal")
    return random.choice(bestchildren)

def DEFAULTPOLICY(state):
    while state.terminal()==False:
        state, action=state.next_state()
    return state.reward()

def BACKUP(node,reward):
    while node!=None:
        node.visits+=1
        node.reward = max(reward, node.reward)
        node=node.parent
    return

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
        temp=UCTSEARCH(args.num_sims,current_node)
        print("Num Children: %d"%len(current_node.children))
        for i,c in enumerate(current_node.children):
            print(i,c)
        print("Best Child: %s"%current_node.state)
        current_node = temp
        current_node.state.gs.printBoard()
        print("--------------------------------")   
            