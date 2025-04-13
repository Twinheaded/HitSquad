from .search_method import SearchMethod

class BS(SearchMethod):
    name = "BS"

    def search(self, beam_width=2):
        h = self.problem.distance_heuristic

        while self.frontier:
            node, path = self.frontier.pop()          # state - the current node
            path = path + [node]
            self.explored.append(node)

            if self.problem.goal_test(node):
                self.result = node
                self.final_path = path
                return

            ## A list of connected nodes (actions) sorted by the shortest distance to the nearest destination
            actions_sorted_by_id = [a for a in sorted(self.problem.get_actions(node).keys(), key=lambda x: x.node_id, reverse=True)]
            actions = [a for a in sorted(actions_sorted_by_id, key=lambda x: h(x), reverse=True)]
            print(actions)
            for a in actions[:beam_width]:
                if not a in self.explored:
                    self.frontier.append((a, path))

            ################
            self.print_state(node, actions) # <-- For debugging only
            ################









#from .search_method import SearchMethod

#class BS(SearchMethod):
#    name = "BS"

#    def search(self):
#        goal_test, get_actions = self.problem.goal_test, self.problem.get_actions # Methods
#        origin = self.problem.initial
#        #def bshe(graph, origin, destinations, coords):
#        queue = deque([(origin, [origin], 0)])
#        self.explored = []
#        nodes_created = 1
#        while queue:
#            level_size = len(queue)
#            level = []
#            for _ in range(level_size):
#                current, path, cost = queue.popleft()
#            if current == goal_test:
#                return current, nodes_created, path
#            if current not in self.explored:
#                self.explored.add(current)
#                neighbors = self.problem.get_actions(current)
#                for neighbor in sorted(neighbors.keys()):
#                    nodes_created += 1
#                    new_path = path + [neighbor]
#                    h = heuristic(neighbor, goal_test, coords)
#                    level.append((h, neighbor, new_path, cost + neighbors[neighbor]))
#        level.sort(key=lambda x: (x[0], x[1]))
#        for h, n, p, c in level:
#            queue.append((n, p, c))
#        return None, nodes_created, []

#        ################
#        # self.print_state(node, get_actions(node)) # <-- For debugging only
#        ################
