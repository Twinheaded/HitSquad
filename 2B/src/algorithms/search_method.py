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
    
    def print_state(self, state, actions, actions_sort_key=None):
        print("=================")
        print("STATE:", state)
        print("\nAvailable actions:")
        if actions:
            for a in actions:
                c = self.problem.path_cost(state, a)
                h = self.problem.distance_heuristic(a)
                print(f"-> {a} | cost: {c} | h(x): {h:.3f} | cost + h(x): {c + h:.3f}")
            print("")
        else:
            print("None\n")
        print("FRONTIER:", self.frontier)
        print("EXPLORED:", self.explored)
        print("GOAL:", " or ".join(map(str, self.problem.goal)))

        print("=================")
        print("        |")
        print("        v")
