from .search_method import SearchMethod

class AS(SearchMethod):
    name = "A*"

    def search(self):
        h = self.problem.distance_heuristic
        g = self.problem.travel_time

        while self.frontier:
            current_site, path = self.frontier.pop()
            path = path + [current_site]
            self.explored.append(current_site)

            if self.problem.goal_test(current_site):
                self.result = current_site
                self.final_path = path
                return

            ## A list of connected nodes (actions) sorted by the shortest distance to the nearest destination
            actions_sorted_by_id = sorted(self.problem.get_actions(current_site), key=lambda x: x.scats_num, reverse=True)
            actions = sorted(actions_sorted_by_id, key=lambda x: g(current_site, x) + h(x), reverse=True)
            for site in actions:
                if not site in self.explored:
                    self.frontier.append((site, path))

            ################
            # self.print_state(current_site, actions) # <-- For debugging only
            ################
