from .search_method import SearchMethod

class AS(SearchMethod):
    name = "A*"

    def search(self):
        h = self.problem.distance_heuristic

        while self.frontier:
            node, path = self.frontier.pop() # state - the current node
            path = path + [node]
            self.explored.append(node)

            if self.problem.goal_test(node):
                self.result = node
                self.final_path = path
                return

            ## A list of connected nodes (actions) sorted by the shortest distance to the nearest destination
            actions_sorted_by_id = [a for a in sorted(self.problem.get_actions(node).keys(), key=lambda x: x.node_id, reverse=True)]
            actions = [a for a in sorted(actions_sorted_by_id, key=lambda x: self.problem.path_cost(node, x) + h(x), reverse=True)]
            for a in actions:
                if not a in self.explored:
                    self.frontier.append((a, path))

            ################
            # self.print_state(node, actions) # <-- For debugging only
            ################
