from abstract_classes import *

def depth_first_search():
    print('\nRunning DFS algorithm...\n')

    
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)

    routeGraph = RouteGraph()
    routeGraph.connect(n1, n2, 4)
    routeGraph.connect(n2, n3, 4)

    problem = RouteFindingProblem(n1, [n3], routeGraph)

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
