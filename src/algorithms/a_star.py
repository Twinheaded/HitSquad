from .search_method import SearchMethod

class AS(SearchMethod):
    def search(self):
        goal_test, get_actions = self.problem.goal_test, self.problem.get_actions # Methods
        h = self.distance_heuristic

        ## TODO: Convert to OOP

        ################
        self.print_state(node, get_actions(node)) # <-- For debugging only
        ################
        return None


# class GBFS(SearchMethod):
#     def search(self):
#         goal_test, get_actions = self.problem.goal_test, self.problem.get_actions # Methods
#         h = self.distance_heuristic

#         while self.frontier:
#             node, path = self.frontier.pop()          # state - the current node
#             if goal_test(node):
#                 final_path = path + [node]
#                 return node, len(self.explored), final_path
#             self.explored.append(node)
#             ## A list of connected nodes (actions) sorted by the shortest distance to the nearest destination
#             actions = [node for node in sorted(get_actions(node).keys(), key=lambda x: h(x), reverse=True)]
#             for a in actions:
#                 if not a in self.explored:
#                     self.frontier.append((a, path + [node]))
#             ################
#             self.print_state(node, get_actions(node)) # <-- For debugging only
#             ################
#         return None
