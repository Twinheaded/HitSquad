import sys
import warnings
import argparse
import numpy as np
import pandas as pd
import heapq
from queue import Queue
from collections import deque

from jack_classes import *

#############################################################################
# JACK'S CODE

def print_step(state, explored, action_details, frontier):
    print("====================")
    print("STATE:", state)
    print("\nAvailable actions:")
    if action_details:
        for x in reversed(action_details):
            print("->", x)
        print("")
    else:
        print("None\n")
    print("FRONTIER:", frontier)
    
    # print("--------------------")
    print("EXPLORED:", explored)
    print("====================")
    print("         |")
    print("         v")


def depth_first_search(problem):
    frontier = [(problem.initial, [])]       # The first Node (origin)
    explored = []

    while frontier:
        s = frontier.pop()          # state - the current node and its path
        node = s[0]
        path = s[1]
        if problem.goal_test(node):
            return path + [node]
        explored.append(node)
        actions = [n for n in reversed(problem.actions(node).keys())]
        for a in actions:
            if not a in explored:
                frontier.append((a, path + [node]))
        print_step(node, explored, actions, [n[0] for n in frontier])
    return None
#############################################################################

#############################################################################
# JORDAN'S CODE

def greedy_best_first_search(problem):
    ### Greedy Best First Search always expands the node that appears to be closest to goal ###

    def heuristic(node): 
        min_dist = float('inf') # infinite
        for goal in problem.goal: 
            dist = abs(node.x - goal.x) + abs(node.y - goal.y) #Manhattan Distance Formula
            if dist < min_dist: # finds the smallest distance
                min_dist = dist 
        return min_dist

    origin = problem.initial
    frontier = [] #for a priority queue
    heapq.heappush(frontier, (heuristic(origin), [origin])) # heuristic value, path
    explored = set() # marks all visited nodes
    finalpaths = {} # Dictionary containing all final paths selected for each destination

    while frontier: 
        path = heapq.heappop(frontier) # pulls first value
        node = path[-1] # checks last node

        if problem.goal_test(node):
            finalpaths[node] = path 
            if len(finalpaths) == len(problem.goal): # checks if all paths have been found
                return finalpaths

        if node not in explored:
            explored.add(node)
            for neighbor in problem.actions(node):
                if neighbor not in explored:
                    new_path = path + [neighbor] # adds to the frontier
                    heapq.heappush(frontier, (heuristic(neighbor), new_path)) 

    return finalpaths




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
# EXAMPLE USAGE OF THE PROBLEM OBJECT

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
