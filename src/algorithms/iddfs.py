from .search_method import SearchMethod

class IDDFS(SearchMethod):
    name = "IDDFS"

    def __init__(self, problem):
        super().__init__(problem)
        self.frontier = [(self.problem.initial, [], 0)] # Same as parent class but with a third 'depth' value

    def search(self):
        depth = 0
        while True:
            print("DEPTH:", depth)
            print(self.explored)
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





# from .search_method import SearchMethod

# from .search_method import SearchMethod

# class IDDFS(SearchMethod):
#     name = "IDDFS"

#     def search(self):
#         origin = self.problem.initial
#         destinations = self.problem.goal

#         def depth_limited_dfs(node, depth_limit):
#             stack = [(node, [node], 0)]  # (current_node, path, current_depth) 
#             nodes_created = 1

#             while stack:
#                 current, path, depth = stack.pop()

#                 if current in destinations:
#                     return current, nodes_created, path

#                 if depth < depth_limit and current not in self.explored:
#                     self.explored.add(current)
#                     neighbors = self.problem.get_actions(current).keys()
#                     self.print_state(current, neighbors)

#                     for neighbor in sorted(neighbors, key=lambda n: n.node_id):
#                         if neighbor not in self.explored:
#                             nodes_created += 1
#                             new_path = path + [neighbor]
#                             stack.append((neighbor, new_path, depth + 1))

#             return None, nodes_created, []

#         def iddfs(origin, destinations):
#             depth = 0
#             total_nodes_created = 0
#             while True:
#                 result, nodes_created, path = depth_limited_dfs(origin, depth)
#                 total_nodes_created += nodes_created
#                 if result:
#                     return result, total_nodes_created, path
#                 depth += 1

#         result, total_nodes, path = iddfs(origin, destinations)

#         if result:
#             self.result = result
#             self.final_path = path
#             print(f"Found path: {path} | Nodes Created: {total_nodes}")
#             return result
#         else:
#             self.result = None
#             self.final_path = []
#             print("No path found.")
#             return None

#         ################
#         # self.print_state(node, get_actions(node)) # <-- For debugging only
#         ################
