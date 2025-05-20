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
                return

            ## A list of linked sites (actions) sorted by SCATS number
            actions = [site for site in reversed(sorted(self.problem.get_actions(current_site.scats_num), key=lambda x: x.scats_num))]
            for a in actions:
                if not a in self.explored:
                    self.frontier.append((a, path))

            # ################
            # self.print_state(current_site, actions) # <-- For debugging only
            # ################
