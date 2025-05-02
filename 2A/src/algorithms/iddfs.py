from .search_method import SearchMethod

class IDDFS(SearchMethod):
    name = "IDDFS"

    def __init__(self, problem):
        super().__init__(problem)
        self.frontier = [(self.problem.initial, [], 0)] # Same as parent class but with a third 'depth' value

    def search(self):
        depth = 0
        while True:
            if self.depth_limited_dfs(depth):
                return
            depth += 1

    def depth_limited_dfs(self, depth_limit):   # also known as Depth Limited Search (DLS)
        depth = 0
        local_explored = []
        
        while self.frontier:
            node, path, depth = self.frontier.pop()
            path = path + [node]
            local_explored.append(node)

            if self.problem.goal_test(node):
                self.result = node
                self.explored += [node]
                self.final_path = path
                return True

            if depth > depth_limit:     
                self.frontier = [(self.problem.initial, [], 0)] # Reset frontier to be ready for the next depth
                self.explored += local_explored                 # self.explored will hold the paths of all DLS iterations
                return False

            actions = [node for node in reversed(sorted(self.problem.get_actions(node).keys(), key=lambda x: x.node_id))]
            depth += 1
            for a in actions:
                if not a in local_explored:
                    self.frontier.append((a, path, depth))

            ################
            # self.print_state(node, actions) # <-- For debugging only
            ################
        return False
