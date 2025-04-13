from .search_method import SearchMethod

from .search_method import SearchMethod

class IDDFS(SearchMethod):
    name = "IDDFS"

    def search(self):
        origin = self.problem.initial
        destinations = self.problem.goal

        def depth_limited_dfs(node, depth_limit):
            stack = [(node, [node], 0)]  # (current_node, path, current_depth) 
            nodes_created = 1

            while stack:
                current, path, depth = stack.pop()

                if current in destinations:
                    return current, nodes_created, path

                if depth < depth_limit and current not in self.explored:
                    self.explored.add(current)
                    neighbors = self.problem.get_actions(current).keys()
                    self.print_state(current, neighbors)

                    for neighbor in sorted(neighbors, key=lambda n: n.node_id):
                        if neighbor not in self.explored:
                            nodes_created += 1
                            new_path = path + [neighbor]
                            stack.append((neighbor, new_path, depth + 1))

            return None, nodes_created, []

        def iddfs(origin, destinations):
            depth = 0
            total_nodes_created = 0
            while True:
                result, nodes_created, path = depth_limited_dfs(origin, depth)
                total_nodes_created += nodes_created
                if result:
                    return result, total_nodes_created, path
                depth += 1

        result, total_nodes, path = iddfs(origin, destinations)

        if result:
            self.result = result
            self.final_path = path
            print(f"Found path: {path} | Nodes Created: {total_nodes}")
            return result
        else:
            self.result = None
            self.final_path = []
            print("No path found.")
            return None




        ################
        # self.print_state(node, get_actions(node)) # <-- For debugging only
        ################
