from .search_method import SearchMethod

class BS(SearchMethod):
    name = "BS"

    def search(self):
        goal_test, get_actions = self.problem.goal_test, self.problem.get_actions # Methods
        origin = self.problem.initial
        #def bshe(graph, origin, destinations, coords):
        queue = deque([(origin, [origin], 0)])
        self.explored = []
        nodes_created = 1
        while queue:
            level_size = len(queue)
            level = []
            for _ in range(level_size):
                current, path, cost = queue.popleft()
            if current == goal_test:
                return current, nodes_created, path
            if current not in self.explored:
                self.explored.add(current)
                neighbors = self.problem.get_actions(current)
                for neighbor in sorted(neighbors.keys()):
                    nodes_created += 1
                    new_path = path + [neighbor]
                    h = heuristic(neighbor, goal_test, coords)
                    level.append((h, neighbor, new_path, cost + neighbors[neighbor]))
        level.sort(key=lambda x: (x[0], x[1]))
        for h, n, p, c in level:
            queue.append((n, p, c))
        return None, nodes_created, []

    # def heuristic(node, destinations, coords):
    #     if node in destinations:
    #         return 0
    #     x1, y1 = coords[node]
    #     min_dist = float('inf')
    #     for d in destinations:
    #         x2, y2 = coords[d]
    #         dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    #         if dist < min_dist:
    #             min_dist = dist
    #     return min_dist


        ################
        # self.print_state(node, get_actions(node)) # <-- For debugging only
        ################
