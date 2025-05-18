from .search_method import SearchMethod

class IDDFS(SearchMethod):
    name = "IDDFS"

    def __init__(self, problem):
        super().__init__(problem)
        self.frontier = [(self.problem.origin, [], 0)] # Same as parent class but with a third 'depth' value

    def search(self, start_scats, goal_scats):
        start = self.problem.get_intersection_by_scats(start_scats)
        goal = self.problem.get_intersection_by_scats(goal_scats)
        depth = 0
        while True:
            self.frontier = [(start, [], 0)]
            if self.depth_limited_dfs(goal, depth):
                return self.final_path
            depth += 1

    def depth_limited_dfs(self, goal, depth_limit):   # also known as Depth Limited Search (DLS)
        local_explored = []
        
        while self.frontier:
            current_site, path, depth = self.frontier.pop()
            path = path + [current_site]
            local_explored.append(current_site)

            if current_site == goal or self.problem.goal_test(current_site):
                self.result = current_site
                self.explored += [current_site]
                self.final_path = path
                return True

            if depth > depth_limit:     
                self.explored += local_explored                 # self.explored will hold the paths of all DLS iterations
                return False

            actions = [site for site in reversed(sorted(self.problem.get_actions(current_site), key=lambda x: x.scats_num))]
            for a in actions:
                if not a in local_explored:
                    self.frontier.append((a, path, depth + 1))

            ################
            self.print_state(current_site, actions) # <-- For debugging only
            ################
        return False
