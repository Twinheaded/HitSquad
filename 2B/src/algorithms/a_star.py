from .search_method import SearchMethod

class AS(SearchMethod):
    name = "A*"

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

            ## A list of connected nodes (actions) sorted by the shortest distance to the nearest destination
            neighbors_sorted_by_id = [site for site in sorted(self.problem.get_actions(current_site), key=lambda x: x.scats_num, reverse=True)]
            neighbors = [a for a in sorted(neighbors_sorted_by_id, key=lambda x: self.problem.travel_time(current_site, x) + h(x), reverse=True)]
            for neighbor in neighbors:
                if not neighbor in self.explored:
                    self.frontier.append((neighbor, path))

        return []
