from .search_method import SearchMethod

class AS(SearchMethod):
    name = "A*"

    def search(self):
        goal_test, get_actions = self.problem.goal_test, self.problem.get_actions # Methods
        h = self.distance_heuristic

        while self.frontier:
            node, path = self.frontier.pop()          # state - the current node
            path = path + [node]
            self.explored.append(node)
            if goal_test(node):
                self.result = node
                self.final_path = path
                return
            ## A list of connected nodes (actions) sorted by the shortest distance to the nearest destination
            actions = [
                    a[0] for a in sorted(
                        get_actions(node).items(),
                        key=lambda x: self.problem.path_cost(node, x[0]) + h(x[0]),
                        reverse=True)
                    ]
            for a in actions:
                if not a in self.explored:
                    self.frontier.append((a, path))
            ################
            # self.print_state(node, actions) # <-- For debugging only
            ################
