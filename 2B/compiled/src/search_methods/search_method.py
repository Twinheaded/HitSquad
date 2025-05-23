from src.data_structures.traffic_problem import TrafficProblem
from src.data_structures.site import Site

class SearchMethod:
    def __init__(self, problem):
        self.problem = problem
        self.frontier = [(problem.origin, [])] # [(<Site>, [path, from, origin])]
        self.explored = []      # [<Site>, <Site>, <Site>, ...]
        self.result = None      # <Site>
        self.final_path = []    # [<Site>, <Site>, <Site>, ...]

    def search(self):
        raise NotImplementedError
    
    def print_state(self, state, actions, actions_sort_key=None):
        print("=================")
        print("STATE:", state)
        print("\nAvailable actions:")
        if actions:
            for a in actions:
                c = self.problem.travel_time(state, a)
                h = self.problem.distance_heuristic(a)
                print(f"-> {a} | cost: {c} | h(x): {h:.3f} | cost + h(x): {c + h:.3f}")
            print("")
        else:
            print("None\n")
        print("FRONTIER:", self.frontier)
        print("EXPLORED:", self.explored)
        print("DESTINATION:", self.problem.destination)

        print("=================")
        print("        |")
        print("        v")
