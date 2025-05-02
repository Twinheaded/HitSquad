from .search_method import SearchMethod

class DFS(SearchMethod):
    name = "DFS"

    def search(self):
        while self.frontier:
            node, path = self.frontier.pop()          # state - the current node
            path = path + [node]
            self.explored.append(node)

            if self.problem.goal_test(node):
                self.result = node
                self.final_path = path
                return

            ## A list of connected nodes (actions) sorted by the shortest distance to the nearest destination
            actions = [node for node in reversed(sorted(self.problem.get_actions(node).keys(), key=lambda x: x.node_id))]
            for a in actions:
                if not a in self.explored:
                    self.frontier.append((a, path))

            ################
            # self.print_state(node, actions) # <-- For debugging only
            ################
