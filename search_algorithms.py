import sys
import warnings
import argparse
import numpy as np
import pandas as pd
from queue import Queue
from collections import deque

# TEMP
from jack_classes import *

#############################################################################
# ALGORITHMS TO FINISH

def depth_first_search(problem):
    # n1 = Node(1,1,1)
    # n2 = Node(2,2,2)
    # n3 = Node(3,3,3)
    # graph = Graph()
    # graph.connect(n1,n2,5)
    # graph.connect(n2,n3,5)

    # problem = RouteFindingProblem(n1, [n2, n3], graph)

    init = problem.initial       # The first Node (origin)
    goal_test = problem.goal_test
    actions = problem.actions
    
    frontier = [init]
    explored = []
    
    while frontier:
        s = frontier.pop()          # state - the current node

        if s in explored:
            frontier.pop()

        if goal_test(s):
            print("")
            print("GOAL REACHED")
            frontier.append(s)
            result = [init]
            result.extend(frontier)
            return f"{s} reached. Path: {result}"

        explored.append(s)

        actions_sorted = list(actions(s).keys())
        actions_sorted.reverse()

        print("---------")
        print("STATE:", s)
        for a in actions_sorted:
            if not (a in explored or a in frontier):
                frontier.append(a)

        print("Actions:", actions(s))
        print("FRONTIER:", frontier)
        
    return None

def greedy_best_first_search():
    raise NotImplementedError

def a_star_search():
    raise NotImplementedError

def custom_algorithm_1():
    raise NotImplementedError

def custom_algorithm_2():
    raise NotImplementedError


#############################################################################
# AARON'S CODE (+objects)

def breadth_first_search (problem): # Using Queue because of LIFO
    actions      = problem.actions
    goal_test    = problem.goal_test
    origin       = problem.initial
    destinations = problem.goal
    
    finalpaths = {} # Dictionary containing all final paths selected for each destination in destination
    
    visited = [origin]                      # marks all visited nodes 
    start_path = [origin]                   # Beginning Path, only contains origin
    frontier = Queue() 
    frontier.put(start_path) 
    while not frontier.empty(): 
        path = frontier.get()               # Pulls First value
        last_node = path[-1]                # Checks last node from value
        if goal_test(last_node):            # Is the current state a goal state?
            finalpaths[last_node] = path 
            if len(finalpaths) == len(destinations):
                return finalpaths
        for n in actions(last_node):        # For all possible neighbours
            if n not in visited:
                visited.append(n)
                frontier.put(path + [n])    # adds to the frontier
        
    return finalpaths

#############################################################################

#############################################################################
# AARON'S CODE

# def breadth_first_search (origin, destinations, graph): # Using Queue because of LIFO
#     finalpaths = {} # Dictionary containing all final paths selected for each destination in destination
    
#     visited = [origin] # marks all visited nodes 
#     start_path = [origin] # Beginning Path, only contains origin
#     frontier = Queue() 
#     frontier.put(start_path) 
#     while not frontier.empty(): 
#         path = frontier.get() #Pulls First value
#         last_node = path[-1] #Checks last node from value
#         if last_node in destinations: #Checks last node
#                 finalpaths[last_node] = path 
#                 if len(finalpaths) == len(destinations):
#                     return finalpaths
#         for n in graph.get(last_node, []):  # For all possible neighbours
#             if n not in visited:
#                 visited.append(n)
#                 new_path = path + [n]
#                 frontier.put(new_path) # adds to the frontier
        
#     return finalpaths

#############################################################################

#############################################################################
# JACK'S CODE

def example_search_algorithm(problem):
    #######################################
    # EXPLANATION OF THE 'problem' OBJECT #
    #######################################
    # The following code is for reference #
    # only.                               #
    #                                     #
    # Nodes should not be assigned to     #
    # variables this way...               #
    #                                     #
    # I've just written it like this so   #
    # you can see clearly what each       #
    # method of the 'problem' class does. #
    #######################################

    n1 = problem.graph.nodes()[0]
    n2 = problem.graph.nodes()[1]
    n3 = problem.graph.nodes()[2]
    n4 = problem.graph.nodes()[3]
    n5 = problem.graph.nodes()[4]

    # (returns) a dictionary of {Nodes: costs}; all possible actions from Node 2
    print(problem.actions(n2))

    # (returns) a Node; the resulting state after attempting to traverse from Node 3 to Node 1
    print(problem.result(n3, n1))

    # (returns) a boolean; whether or not the current state Node 5 is a goal state
    print(problem.goal_test(n5))

    # (returns) an int; the cost of traversing from Node 2 to Node 1
    print(problem.path_cost(n2, n1))

    # (returns) an int; the cost of traversing from Node 2 to Node 1 + the cost spent so far
    #           Useful for the A* algorithm
    print(problem.path_cost(n2, n1, 14))

    # (returns) an int; the lowest edge cost in the environment
    print(problem.find_min_edge())

#############################################################################
