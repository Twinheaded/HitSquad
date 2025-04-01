import sys
import warnings
import argparse
import numpy as np
import pandas as pd
from queue import Queue
from collections import deque

def depth_first_search ():
    raise NotImplementedError

def breadth_first_search (origin, destinations, graph): # Using Queue because of LIFO
    finalpaths = {} # Dictionary containing all final paths selected for each destination in destination
    
    visited = [origin] # marks all visited nodes 
    start_path = [origin] # Beginning Path, only contains origin
    frontier = Queue() 
    frontier.put(start_path) 
    while not frontier.empty(): 
        path = frontier.get() #Pulls First value
        last_node = path[-1] #Checks last node from value
        if last_node in destinations: #Checks last node
                finalpaths[last_node] = path 
                if len(finalpaths) == len(destinations):
                    return finalpaths
        for n in graph.get(last_node, []):  # For all possible neighbours
            if n not in visited:
                visited.append(n)
                new_path = path + [n]
                frontier.put(new_path) # adds to the frontier
        
    return finalpaths

def astar_search():
    raise NotImplementedError

def greedy_first_best_search():
    raise NotImplementedError

def iterative_deepening_depth_first_search():
    raise NotImplementedError

def beam_search():
    raise NotImplementedError
