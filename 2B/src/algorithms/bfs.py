from .search_method import SearchMethod

class BFS(SearchMethod):
    name = "BFS"

    def search(self):
        while self.frontier:
            current_site, path = self.frontier.pop(0)
            self.explored.append(current_site)

            if self.problem.goal_test(current_site):
                self.result = current_site 
                self.final_path = path + [current_site]
                return

            ## A list of linked sites (actions) sorted by SCATS number
            actions = sorted(self.problem.get_actions(current_site), key=lambda x: x.scats_num)
            for site in actions:
                if not site in self.explored and all(n[0] != site for n in self.frontier):
                    self.frontier.append((site, path + [current_site]))

            ################
            # self.print_state(current_site, self.problem.get_actions(current_site)) # <-- For debugging only
            ################
