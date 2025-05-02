import sys
import heapq
from collections import deque

from jack_classes import *
from AJ_search import File_Reader
from search_algorithms import print_step


def distance_heuristic(node, destinations):
    if node in destinations:
        return 0
    x1, y1 = node.x, node.y
    min_dist = float('inf')
    for d in destinations:
        x2, y2 = d.x, d.y
        dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        if dist < min_dist:
            min_dist = dist
    return min_dist

# def dfs(graph, origin, destinations):
#     stack = [(origin, [origin], 0)]
#     visited = set()
#     nodes_created = 1
#     while stack:
#         current, path, cost = stack.pop()
#         if current in destinations:
#             return current, nodes_created, path
#         if current not in visited:
#             visited.add(current)
#             neighbors = sorted(graph.get(current, {}).keys(), reverse=True)
#             for neighbor in neighbors:
#                 nodes_created += 1
#                 new_path = path + [neighbor]
#                 stack.append((neighbor, new_path, cost + graph[current][neighbor]))
#     return None, nodes_created, []

# def bfs(graph, origin, destinations):
#     queue = deque([(origin, [origin], 0)])
#     visited = set()
#     nodes_created = 1
#     while queue:
#         current, path, cost = queue.popleft()
#         if current in destinations:
#             return current, nodes_created, path
#         if current not in visited:
#             visited.add(current)
#             neighbors = sorted(graph.get(current, {}).keys())
#             for neighbor in neighbors:
#                 nodes_created += 1
#                 new_path = path + [neighbor]
#                 queue.append((neighbor, new_path, cost + graph[current][neighbor]))
#     return None, nodes_created, []

#################################################################

def gbfs(problem):
    h = lambda x: distance_heuristic(x, problem.goal)
    frontier = [(problem.initial, [])]    # The first Node (origin)
    explored = []
    while frontier:
        s = frontier.pop()          # state - the current node
        node = s[0]
        path = s[1]
        if problem.goal_test(node):
            return path + [node]   # returns the full path
        explored.append(node)

        ## A list of connected nodes (actions) sorted by the shortest distance to the nearest destination
        actions = [node for node in sorted(problem.actions(node).keys(), key=lambda x: h(x), reverse=True)]
        action_details = []
        for a in actions:
            action_details.append(f"{a} cost: {problem.path_cost(node, a)}, distance: {h(a)}")
            if not a in explored:
                frontier.append((a, path + [node]))
        print_step(s, explored, action_details, frontier)
    return None

#################################################################

# def astar(graph, origin, destinations, coords):
#     pq = []
#     initial_h = heuristic(origin, destinations, coords)
#     heapq.heappush(pq, (initial_h, 0, origin, [origin]))
#     visited = set()
#     nodes_created = 1
#     while pq:
#         f, g, current, path = heapq.heappop(pq)
#         if current in destinations:
#             return current, nodes_created, path
#         if current not in visited:
#             visited.add(current)
#             neighbors = sorted(graph.get(current, {}).items(), key=lambda x: x[0])
#             for neighbor, edge_cost in neighbors:
#                 nodes_created += 1
#                 new_g = g + edge_cost
#                 new_h = heuristic(neighbor, destinations, coords)
#                 new_f = new_g + new_h
#                 heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))
#     return None, nodes_created, []

# def iddfs(graph, origin, destinations):
#     depth = 0
#     total_nodes = 0
#     while True:
#         result, nodes_created, path = depth_limited_dfs(graph, origin, destinations, depth)
#         total_nodes += nodes_created
#         if result is not None:
#             return result, total_nodes, path
#         depth += 1

# def depth_limited_dfs(graph, origin, destinations, depth_limit):
#     stack = [(origin, [origin], 0, 0)]
#     visited = set()
#     nodes_created = 1
#     while stack:
#         current, path, cost, depth = stack.pop()
#         if current in destinations:
#             return current, nodes_created, path
#         if depth < depth_limit and current not in visited:
#             visited.add(current)
#             neighbors = sorted(graph.get(current, {}).keys(), reverse=True)
#             for neighbor in neighbors:
#                 nodes_created += 1
#                 new_path = path + [neighbor]
#                 stack.append((neighbor, new_path, cost + graph[current][neighbor], depth + 1))
#     return None, nodes_created, []

# def bshe(graph, origin, destinations, coords):
#     queue = deque([(origin, [origin], 0)])
#     visited = set()
#     nodes_created = 1
#     while queue:
#         level_size = len(queue)
#         level = []
#         for _ in range(level_size):
#             current, path, cost = queue.popleft()
#             if current in destinations:
#                 return current, nodes_created, path
#             if current not in visited:
#                 visited.add(current)
#                 neighbors = graph.get(current, {})
#                 for neighbor in sorted(neighbors.keys()):
#                     nodes_created += 1
#                     new_path = path + [neighbor]
#                     h = heuristic(neighbor, destinations, coords)
#                     level.append((h, neighbor, new_path, cost + neighbors[neighbor]))
#         level.sort(key=lambda x: (x[0], x[1]))
#         for h, n, p, c in level:
#             queue.append((n, p, c))
#     return None, nodes_created, []

def main():
    ## Removed input validation for demonstration purposes
    problem = File_Reader(sys.argv[1])

    match sys.argv[2]:
        # case "DFS":
        #     result = depth_first_search(problem)
        # case "BFS":
        #     result = breadth_first_search(problem)
        case "GBFS":
            result = gbfs(problem)
        # case "AS" | "A*":
        #     result = a_star_search(problem)
        # case "CUS1":
        #     result = custom_search_algorithm_1(problem)
        # case "CUS2":
        #     result = custom_search_algorithm_2(problem)
        case _:
            result = ""
        
    print("SOLUTION:", " -> ".join(map(str, result)), "\n")

if __name__ == "__main__":
    main()
