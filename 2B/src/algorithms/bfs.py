from .search_method import SearchMethod

class BFS(SearchMethod):
    name = "BFS"

    def search(self, start_scats, goal_scats):
        start = self.problem.get_intersection_by_scats(start_scats)
        goal = self.problem.get_intersection_by_scats(goal_scats)
        self.frontier = [(start, [])]
        self.explored = []

        while self.frontier:
            current_site, path = self.frontier.pop(0)
            self.explored.append(current_site)

            if current_site == goal or self.problem.goal_test(current_site):
                self.result = current_site 
                self.final_path = path + [current_site]
                return self.final_path  # Return path as list of Intersection objects

            neighbors = [site for site in sorted(self.problem.get_actions(current_site), key=lambda x: x.scats_num)]
            for neighbor in neighbors:
                if neighbor not in self.explored and all(n[0] != neighbor for n in self.frontier):
                    self.frontier.append((neighbor, path + [current_site]))

        return []  # No path found
