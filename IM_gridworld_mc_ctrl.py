# -*- coding: utf-8 -*-
"""
Created on Wed May  8 16:36:25 2019

@author: acer
"""


import numpy as np
import random

class Grid:
    def __init__(self, width, height, start_x, start_y):
        self.width = width
        self.height = height
        self.i = start_x
        self.j = start_y
        
    def reward_action(self, reward, action, action_start):
        # rewards should be a dict of: (i, j): r (row, col): reward
        # actions should be a dict of: (i, j): A (row, col): list of possible actions
        self.reward = reward
        self.action = action
        self.action_start = action_start
        
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
#                val = np.random.randn()
                val = 0
                
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

action_start = {
#                 (0, 0): ('D', 'R'),
#                (1, 0): ('U', 'D'),
                (2, 0): ('U', 'R'),
#                (2, 3): ('L', 'U')
                }

g.reward_action(reward, action, action_start)
V = v_init(3, 4)
P = policy_sel(V, 3, 4)


#monte carlo + control epsilongreedy + update return right the way

for i in range(50):
    #random starting point
    sp_i, sp_j = list(g.action_start.keys())[random.randint(0,len(g.action_start.keys())-1)]
    state_reward = []
    g.set_state(sp_i, sp_j)
    loop = True
    while loop:
        gv = 0
        state_reward.append(((sp_i, sp_j), V[(sp_i, sp_j)]))
        if (sp_i, sp_j) == (0, 3) or (sp_i, sp_j) == (1, 3):
            state_reward.reverse()
            for j in range(len(state_reward)):
                x, y = state_reward[j][0]
                
                gv = -1.5 + 0.9*gv

                if (x, y) == (0, 3) or (x, y) == (1, 3):
                    gv = V[(x, y)]
                else:
                    V[(x, y)] = V[(x, y)] + (1/(50))*(gv - V[(x, y)])
                
            loop = False
        else:
            new_v = 0
            curr_v = -100
            pos_act = g.action[(sp_i, sp_j)]
            
            curr_i, curr_j = sp_i, sp_j
            
            for curr_act in g.action[(curr_i, curr_j)]:
                g.move(curr_act)
                new_i, new_j = g.where()
                new_v = V[(new_i, new_j)]
                
                if curr_v <= new_v:
                    curr_v = new_v
                    act = curr_act
                else:
                    curr_v = curr_v
                    
                g.set_state(curr_i, curr_j)
            
            rand = random.randint(1,10)
            if rand >= 3:
                act = act
            else:
                act = str(g.action[(sp_i, sp_j)][random.randint(0,len(g.action[(sp_i, sp_j)])-1)])
                
            g.set_state(sp_i, sp_j)
            g.move(act)
            sp_i, sp_j = g.where()[0], g.where()[1]
            

P = policy_sel(V, 3, 4)

print_values(V, g)
print_policy(P, g)



