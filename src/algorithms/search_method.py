from ..problem import Problem
from ..node import Node

class SearchMethod:
    def __init__(self, problem):
        self.problem = problem
        self.frontier = [(problem.initial, [])]
        self.explored = []

    def search(self):
        raise NotImplementedError

    def distance_heuristic(self, node):
        if node in self.problem.goal:
            return 0
        x1, y1 = node.coordinates
        min_dist = float('inf')
        for d in self.problem.goal:
            x2, y2 = d.coordinates
            dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            if dist < min_dist:
                min_dist = dist
        return min_dist
    
    def print_state(self, state, actions, actions_sort_key=None):
        print("=================")
        print("STATE:", state)
        print("\nAvailable actions:")
        if actions:
            # for x in sorted(actions, key=actions_sort_key):
            for a in actions:
                print("->", a, "| cost:", self.problem.path_cost(state, a), "| h(x):", self.distance_heuristic(a))
            print("")
        else:
            print("None\n")
        print("FRONTIER:", self.frontier)
        print("EXPLORED:", self.explored)
        print("=================")
        print("        |")
        print("        v")
