from .search_method import SearchMethod

class DFS(SearchMethod):
    name = "DFS"

    def search(self):
        while self.frontier:
            current_site, path = self.frontier.pop()
            path = path + [current_site]
            self.explored.append(current_site)

            if self.problem.goal_test(current_site):
                self.result = current_site
                self.final_path = path
                for i in range(len(self.final_path) - 1):
                    self.travel_time += self.problem.travel_time(self.final_path[i], self.final_path[i+1], self.ml_model)
                return

            ## A list of linked sites (actions) sorted by SCATS number
            actions = [site for site in reversed(sorted(self.problem.get_actions(current_site), key=lambda x: x.scats_num))]
            for site in actions:
                if not site in self.explored:
                    self.frontier.append((site, path))

            # ################
            # self.print_state(current_site, actions) # <-- For debugging only
            # ################
