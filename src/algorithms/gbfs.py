from .search_method import SearchMethod

# Philip / Jack
# ============================================================
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


# Jordan
# ============================================================
import heapq;
class GBFS(SearchMethod):
    ###Greedy Best-First Search (GBFS) using Euclidean distance heuristic.###
    
    # > These are defined in search_algorithm.py (parent class) - Jack
    # ------------------------------------------------------------
    # def __init__(self, problem): 
    #     self.problem = problem 
    #     self.frontier = []  
    #     self.explored = set()  
    #     self.final_paths = {}
    
    # > This has now been added to search_algorithm.py - Jack
    # -------------------------------------------------------------
    # def heuristic(self, node):
    #     ###Computes the minimum Euclidean distance from node to any goal.###
    #     min_dist = float('inf')
    #     for goal in self.problem.goal:
    #         dx = node.x - goal.x
    #         dy = node.y - goal.y
    #         dist = math.sqrt(dx**2 + dy**2)  # Euclidean distance
    #         if dist < min_dist:
    #             min_dist = dist
    #     return min_dist
    
    def search(self):
        ###Runs GBFS and returns the paths to all goals.###
        origin = self.problem.initial
        heapq.heappush(self.frontier, (self.heuristic(origin), [origin]))
        
        while self.frontier:
            _, path = heapq.heappop(self.frontier)
            node = path[-1]
            
            if self.problem.goal_test(node):
                self.final_paths[node] = path
                if len(self.final_paths) == len(self.problem.goal):
                    return self.final_paths
            
            if node not in self.explored:
                self.explored.add(node)
                for neighbor in self.problem.actions(node):
                    if neighbor not in self.explored:
                        new_path = path + [neighbor]
                        heapq.heappush(
                            self.frontier,
                            (self._euclidean_heuristic(neighbor), new_path)
                        )
        
        return self.final_paths
