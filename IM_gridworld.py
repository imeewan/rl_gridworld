# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 11:46:29 2018

@author: acer
"""

import numpy as np

class Grid:
    def __init__(self, width, height, start_x, start_y):
        self.width = width
        self.height = height
        self.i = start_x
        self.j = start_y
        
    def reward_action(self, reward, action):
        # rewards should be a dict of: (i, j): r (row, col): reward
        # actions should be a dict of: (i, j): A (row, col): list of possible actions
        self.reward = reward
        self.action = action
        
    def set_state(self, si, sj):
        self.i = si
        self.j = sj
        
    def current_state(self):
        return (self.i, self.j)
    
    def is_terminal(self, si, sj):
        return (si, sj) not in self.action
    
    def game_over(self):
        return (self.i, self.j) not in self.action
    
    def move(self, act):
        self.act = str(act)
        if act in self.action[(self.i, self.j)]:
            if act == "U":
                self.i -= 1
            if act == "D":
                self.i += 1            
            if act == "L":
                self.j -= 1
            if act == "R":
                self.j += 1
        else:
            print("action not allowed")
            
    def where(self):
        return self.i, self.j
    
    def action(self):
        
        return set(action.keys())
    
    def all_states(self):
    # possibly buggy but simple way to get all states
    # either a position that has possible next actions
    # or a position that yields a reward
        return set(self.action.keys()) | set(self.reward.keys())
#        return set(self.action.keys())

def print_values(V, g):
  for i in range(g.width):
    print("---------------------------")
    for j in range(g.height):
      v = V.get((i,j), 0)
      if v >= 0:
        print(" %.2f|" % v, end="")
      else:
        print("%.2f|" % v, end="") # -ve sign takes up an extra space
    print("")


def print_policy(P, g):
  for i in range(g.width):
    print("---------------------------")
    for j in range(g.height):
      a = P.get((i,j), ' ')
      print("  %s  |" % a, end="")
    print("")

def v_init(width, height):
    V = {}
    for w in range(int(width)):
        for h in range(int(height)):
            s = w, h
            if s == (0, 3):
                val = 10
            elif s == (1, 3):
                val = -10

            else:
                val = np.random.randn()
#                val = 0
                
            if s != (1, 1):
                V.update({s: val})  
    return V


def policy_sel(V, width, height):
    P = {}
    for s in action.keys():
        si, sj = s
        g.set_state(si, sj)
        max_v = -10
        act = 'L'
        pos_act = g.action[s]
        for pos in pos_act:
            g.set_state(si, sj)
            g.move(pos)
            v = V[g.where()]
            if v >= max_v:
                max_v = v
                act = pos
        P.update({s: act})
    return P


g = Grid(3, 4, 2, 0)
reward = {(0, 3): 10, (1, 3): -10}
action = {(0, 0): ('D', 'R'),
    (0, 1): ('L', 'R'),
    (0, 2): ('L', 'D', 'R'),
    (1, 0): ('U', 'D'),
    (1, 2): ('U', 'D', 'R'),
    (2, 0): ('U', 'R'),
    (2, 1): ('L', 'R'),
    (2, 2): ('L', 'R', 'U'),
    (2, 3): ('L', 'U'),}


g.reward_action(reward, action)
V = v_init(3, 4)
P = policy_sel(V, 3, 4)

print_values(V, g)
print_policy(P, g)

#g.reward_action(reward, action)
#g.move('R')
#g.where()
#print(g.is_terminal(g.where()[0], g.where()[1]))
#g.game_over()


#attrs = vars(g)
#print(attrs.items())

#g.all_states()

#action.values()
#action.keys()
#action[(0, 0)]

#policy Evaluation
V = v_init(3, 4)
P = policy_sel(V, 3, 4)
small_number = 0.8

for i in range(1000):
    temp  = set(V.values())
    for s in action.keys():
        si, sj = s
        g.set_state(si, sj)
        new_v = 0
        delta = 0
        pos_act = g.action[s]

        for pos in pos_act:
            e = 1 / len(pos_act)
            g.set_state(si, sj)
            g.move(pos)
            v = V[g.where()]
            new_v += e*(v*small_number - 2)
        
        if i % 1000 == 0:
            print(i)
            
        V[si, sj] = new_v
        
 
print_values(V, g)
P = policy_sel(V, 3, 4)
print_policy(P, g)

#Value iteration  
V = v_init(3, 4)
P = policy_sel(V, 3, 4)
small_number = 0.9
for i in range(1000):
    temp  = set(V.values())
    for s in action.keys():
        si, sj = s
        g.set_state(si, sj)
        curr_v = -100
        pos_act = g.action[s]

        for pos in pos_act:
            e = 1 / len(pos_act)
            g.set_state(si, sj)
            g.move(pos)
            v = V[g.where()]
            new_v = e*(v*small_number - 2)
            
            if new_v >= curr_v:
                curr_v = new_v
            
        V[si, sj] = curr_v
        
print_values(V, g)
P = policy_sel(V, 3, 4)
print_policy(P, g)

