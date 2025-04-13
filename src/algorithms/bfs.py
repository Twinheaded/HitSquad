from .search_method import SearchMethod
from multiprocessing import Queue

from .search_method import SearchMethod
from collections import deque

class BFS(SearchMethod):
    name = "BFS"

    def search(self):
        while self.frontier:
            current_node, path = self.frontier.pop(0)
            self.explored.append(current_node)

            if self.problem.goal_test(current_node):
                self.final_path = path + [current_node]
                self.result = current_node
                return self.result

            neighbors = self.problem.get_actions(current_node)
            
            for neighbor in neighbors:
                if neighbor not in self.explored and all(n[0] != neighbor for n in self.frontier):
                    self.frontier.append((neighbor, path + [current_node]))

          
            ################
            self.print_state(current_node, self.problem.get_actions(current_node)) # <-- For debugging only
            ################
