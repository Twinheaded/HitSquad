from .search_method import SearchMethod

class BS(SearchMethod):
    name = "BS"

    def search(self, beam_width=2):
        h = self.problem.distance_heuristic

        while self.frontier:
            node, path = self.frontier.pop()
            path = path + [node]
            self.explored.append(node)

            if self.problem.goal_test(node):
                self.result = node
                self.final_path = path
                return

            ## A list of connected nodes (actions) sorted by the shortest distance to the nearest destination
            actions_sorted_by_id = [a for a in sorted(self.problem.get_actions(node).keys(), key=lambda x: x.node_id, reverse=True)]
            actions = [a for a in sorted(actions_sorted_by_id, key=lambda x: h(x), reverse=True)]
            for a in actions[-beam_width:]:
                if not a in self.explored:
                    self.frontier.append((a, path))

            ################
            # self.print_state(node, actions) # <-- For debugging only
            ################
