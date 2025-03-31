# from search import nodes, problem from classes import *
def depth_first_search(problem):
    print('\nRunning DFS algorithm...\n')

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

def breadth_first_search():
    raise NotImplementedError

def greedy_best_first_search():
    raise NotImplementedError

def a_star_search():
    raise NotImplementedError

def custom_algorithm_1():
    raise NotImplementedError

def custom_algorithm_2():
    raise NotImplementedError
