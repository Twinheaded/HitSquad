from .search_method import SearchMethod

class DFS(SearchMethod):
    name = "DFS"

    def search(self, start_scats, goal_scats):
        start = self.problem.get_intersection_by_scats(start_scats)
        goal = self.problem.get_intersection_by_scats(goal_scats)
        self.frontier = [(start, [])]
        self.explored = []

        while self.frontier:
            current_site, path = self.frontier.pop()
            path = path + [current_site]
            self.explored.append(current_site)

            if current_site == goal or self.problem.goal_test(current_site):
                self.result = current_site
                self.final_path = path
                return path

            actions = [site for site in reversed(sorted(self.problem.get_actions(current_site), key=lambda x: x.scats_num))]
            for a in actions:
                if not a in self.explored:
                    self.frontier.append((a, path))

        return []
