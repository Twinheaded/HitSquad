from .search_method import SearchMethod

class GBFS(SearchMethod):
    name = "GBFS"

    def search(self, start_scats, goal_scats):
        start = self.problem.get_intersection_by_scats(start_scats)
        goal = self.problem.get_intersection_by_scats(goal_scats)
        h = self.problem.distance_heuristic
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

            actions_sorted_by_id = [a for a in sorted(self.problem.get_actions(current_site), key=lambda x: x.scats_num, reverse=True)]
            actions = [a for a in sorted(actions_sorted_by_id, key=lambda x: h(x), reverse=True)]
            for a in actions:
                if not a in self.explored:
                    self.frontier.append((a, path))

        return []
