from ..problem import Problem
from ..node import Node


class SearchMethod:
    def __init__(self, problem):
        self.problem = problem
        self.frontier = [(problem.initial, [])] # [(<Node>, [<path>, <from>, <origin>])]
        self.explored = []      # [<Node>, <Node>, <Node>, ...]
        self.result = None      # <Node>
        self.final_path = []    # [<Node>, <Node>, <Node>, ...]

    def search(self):
        raise NotImplementedError

    def distance_heuristic(self, node):
        ###Computes the minimum Euclidean distance from node to any goal.###
        if node in self.problem.goal:
            return 0
        min_dist = float('inf')
        for goal in self.problem.goal:
            dx = node.coordinates[0] - goal.coordinates[0]
            dy = node.coordinates[1] - goal.coordinates[1]
            dist = (dx**2 + dy**2)**0.5  # Euclidean distance
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
        print("GOAL:", " or ".join(map(str, self.problem.goal)))
        print("=================")
        print("        |")
        print("        v")
