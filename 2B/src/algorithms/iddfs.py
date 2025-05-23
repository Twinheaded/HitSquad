from .search_method import SearchMethod

class IDDFS(SearchMethod):
    name = "IDDFS"

    def __init__(self, problem):
        super().__init__(problem)

    def search(self, max_depth=15):  # Add a max depth limit to avoid infinite loops
        for depth in range(max_depth + 1):
            self.frontier = [(self.problem.initial, [], 0)]  # Reset frontier each iteration
            local_explored = []
            if self.depth_limited_dfs(depth, local_explored):
                return
            self.explored += local_explored  # Accumulate explored nodes across depths

    def depth_limited_dfs(self, depth_limit, local_explored):
        while self.frontier:
            current_site, path, depth = self.frontier.pop()
            path = path + [current_site]
            local_explored.append(current_site)

            if self.problem.goal_test(current_site):
                self.result = current_site
                self.final_path = path
                return True

            if depth < depth_limit:
                actions = list(reversed(sorted(self.problem.get_actions(current_site), key=lambda x: x.scats_num)))
                for site in actions:
                    if site not in local_explored:
                        self.frontier.append((site, path, depth + 1))

            ################
            # self.print_state(node, actions) # <-- For debugging only
            ################
        return False