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
    def add_child(self,child_state, move, nodes):
        child=Node(child_state,self)
        nodes[child_state] = child
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
        


def UCTSEARCH(budget,root, nodes):
    #print("searching...")
    if not root.state:
        nodes[root.state] = root
    for iter in range(int(budget)):
        if iter%10000==9999:
            logger.info("simulation: %d"%iter)
            logger.info(root)
        front=TREEPOLICY(root, nodes)
        reward, front =DEFAULTPOLICY(front, nodes)
        BACKUP(front,reward)
    return BESTCHILD(root,0, True)

def TREEPOLICY(node, nodes):
    #a hack to force 'exploitation' in a game where there are many options, and you may never/not want to fully expand first
    while node.state.terminal()==False:
        if len(node.children)==0:
            return EXPAND(node, nodes)
        elif random.uniform(0,1)<.5:
            node=BESTCHILD(node,SCALAR)
        else:
            if node.fully_expanded()==False:    
                return EXPAND(node, nodes)
            else:
                node=BESTCHILD(node,SCALAR)
    return node

def EXPAND(node, nodes):
    tried_children=[d for c, d in node.children]
    new_state, move =node.state.next_state()
    while move in tried_children:
        new_state, move=node.state.next_state()
    node.add_child(new_state, move, nodes)
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

def DEFAULTPOLICY(node, nodes):
    while node.state.terminal()==False:
        state, action = node.state.next_state()
        if Node(state) in node.children:
            node = nodes[state]
        else:
            node = node.add_child(state, action, nodes)
    return node.state.reward(), node

def BACKUP(node,reward):
    while node!=None:
        node.visits+=1
        node.reward = max(reward, node.reward)
        node=node.parent
    return


def getRollout(diveGame, num_sims, nodes):
    rollout = []
    scores = []
    states = []
    states.append(diveGame)
    scores.append(diveGame.cash)
    state = State()
    state.gs = diveGame
    node = Node(state)
    nodes[state] = node
    startNode = node
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
    nodes[state] = node
    startNode = node

    node, action=UCTSEARCH(num_sims, node, nodes)

    states.append(node.state.gs)
    scores.append(node.state.gs.cash)
    rollout.append(action)
    while not node.state.gs.isOver():
        #node.state.gs.printBoard()
        try:
            node, action = BESTCHILD(node, 0, True)
        except:
            pdb.set_trace()
            node.state.gs.printBoard()
            print(node.state.terminal(), node.reward, len(node.children))
            1 / 0
        rollout.append(action)
        states.append(node.state.gs)
        scores.append(node.state.gs.cash)
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
    nodes[State()] = current_node
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
        print("Nodes:", len(nodes))
            