from .search_method import SearchMethod

class GBFS(SearchMethod):
    name = "GBFS"

    def search(self):
        h = self.problem.distance_heuristic

        while self.frontier:
            current_site, path = self.frontier.pop()          # state - the current node
            path = path + [current_site]
            self.explored.append(current_site)

            if self.problem.goal_test(current_site):
                self.result = current_site
                self.final_path = path
                return

            ## A list of connected sites (actions) sorted by the shortest distance to the nearest destination
            actions_sorted_by_id = [a for a in sorted(self.problem.get_actions(current_site), key=lambda x: x.scats_num, reverse=True)]
            actions = [a for a in sorted(actions_sorted_by_id, key=lambda x: h(x), reverse=True)]
            for a in actions:
                if not a in self.explored:
                    self.frontier.append((a, path))

            ################
            # self.print_state(current_site, actions) # <-- For debugging only
            ################
