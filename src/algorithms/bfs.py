from .search_method import SearchMethod
from multiprocessing import Queue

from .search_method import SearchMethod
from collections import deque

class BFS(SearchMethod):
    name = "BFS"

    def search(self):
        frontier = deque()
        frontier.append((self.problem.initial, []))  # (current_node, path)
        self.explored = []
        self.result = None
        self.final_path = []

        while frontier:
            current_node, path = frontier.popleft()
            self.explored.append(current_node)

            if self.problem.goal_test(current_node):
                self.final_path = path + [current_node]
                self.result = current_node
                return self.result

            neighbors = self.problem.get_actions(current_node)
            
            for neighbor in neighbors:
                if neighbor not in self.explored and all(n[0] != neighbor for n in frontier):
                    frontier.append((neighbor, path + [current_node]))

          
        ################
        # self.print_state(node, get_actions(node)) # <-- For debugging only
        ################
