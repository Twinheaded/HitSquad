from .search_method import SearchMethod

class AS(SearchMethod):
    name = "A*"

    def search(self):
        h = self.problem.distance_heuristic # h(s) -> Haversine distance between site 's' and the destination
        g = self.problem.travel_time # g(a,b, ml_model) -> Travel time (seconds) to reach site 'b' from site 'a'

        # h(s) and g(a,b) approximately return 1.5 and 120 respectively.
        # A* will be more effective if both heuristics return similar values, so G_MULTIPLIER converts the value of g() from seconds to minutes.
        G_MULTIPLIER = 1/60

        while self.frontier:
            current_site, path = self.frontier.pop()
            path = path + [current_site]
            self.explored.append(current_site)

            if self.problem.goal_test(current_site):
                self.result = current_site
                self.final_path = path
                for i in range(len(self.final_path) - 1):
                    self.travel_time += self.problem.travel_time(self.final_path[i], self.final_path[i+1], self.ml_model)
                print("Final path:", self.final_path)
                print("Total:", self.travel_time)
                return

            ## A list of connected nodes (actions) sorted by the shortest distance to the nearest destination
            actions_sorted_by_id = [site for site in sorted(self.problem.get_actions(current_site), key=lambda x: x.scats_num, reverse=True)]
            actions = [site for site in sorted(actions_sorted_by_id, key=lambda x: g(current_site, x, self.ml_model)*G_MULTIPLIER + h(x), reverse=True)]
            for site in actions:
                if not site in self.explored and not site in [s[0] for s in self.frontier]:
                    self.frontier.append((site, path))

            ################
            # self.print_state(current_site, actions) # <-- For debugging only
            ################
