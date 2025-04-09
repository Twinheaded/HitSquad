from .search_method import SearchMethod

# Jack
# ============================================================
class DFS(SearchMethod):
    def __init__(self, problem):
        super().__init__(problem)
        self.name = "DFS"


    def search(self):
        goal_test, get_actions = self.problem.goal_test, self.problem.get_actions # Methods

        while self.frontier:
            node, path = self.frontier.pop()          # state - the current node
            path = path + [node]
            if goal_test(node):
                return node, len(self.explored), path
            self.explored.append(node)
            ## A list of connected nodes (actions) sorted by the shortest distance to the nearest destination
            print(self.explored)
            actions = [node for node in reversed(get_actions(node).keys())]
            for a in actions:
                if not a in self.explored:
                    self.frontier.append((a, path))
            ################
            # self.print_state(node, get_actions(node)) # <-- For debugging only
            ################
        return None
