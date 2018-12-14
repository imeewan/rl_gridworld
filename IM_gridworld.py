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
    
    def all_states(self):
    # possibly buggy but simple way to get all states
    # either a position that has possible next actions
    # or a position that yields a reward
        return set(self.action.keys()) | set(self.reward.keys())

        
g = Grid(3, 4, 2, 0)
reward = {(0, 3): 1, (1, 3): -1}
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
g.move('R')
g.where()
print(g.is_terminal(g.where()[0], g.where()[1]))
g.game_over()
#attrs = vars(g)
#print(attrs.items())

g.all_states()










