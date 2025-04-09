import sys
import heapq
from collections import deque

def parse_file(filename):
    coords = {}
    graph = {}
    origin = None
    destinations = []
    with open(filename, 'r') as f:
        section = None
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line == "Nodes:":
                section = 'nodes'
            elif line == "Edges:":
                section = 'edges'
            elif line.startswith("Origin:"):    
                section = 'origin'
                parts = line.split(':')
                if len(parts) > 1 and parts[1].strip():  # If value is on the same line
                    origin = int(parts[1].strip())
                else:  # Otherwise, read the next line for the value
                    origin = int(next(f).strip())
            elif line.startswith("Destinations:"):
                section = 'destinations'
                parts = line.split(':')
                if len(parts) > 1 and parts[1].strip():  # If values are on the same line
                    dests = parts[1].strip().split(';')
                else:  # Otherwise, read the next line for the values
                    dests = next(f).strip().split(';')
                destinations = [int(d.strip()) for d in dests if d.strip()]
            else:
                if section == 'nodes':
                    parts = line.split(':')
                    node = int(parts[0].strip())
                    coord_str = parts[1].strip().strip('()')
                    x, y = map(int, coord_str.split(','))
                    coords[node] = (x, y)
                    graph[node] = {}
                elif section == 'edges':
                    edge_part, cost_part = line.split(':')
                    from_to = edge_part.strip().strip('()').split(',')
                    from_node = int(from_to[0])
                    to_node = int(from_to[1])
                    cost = int(cost_part.strip())
                    if from_node not in graph:
                        graph[from_node] = {}
                    graph[from_node][to_node] = cost
    return graph, origin, destinations, coords

def heuristic(node, destinations, coords):
    if node in destinations:
        return 0
    x1, y1 = coords[node]
    min_dist = float('inf')
    for d in destinations:
        x2, y2 = coords[d]
        dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        if dist < min_dist:
            min_dist = dist
    return min_dist

def dfs(graph, origin, destinations):
    stack = [(origin, [origin], 0)]
    visited = set()
    nodes_created = 1
    while stack:
        current, path, cost = stack.pop()
        if current in destinations:
            return current, nodes_created, path
        if current not in visited:
            visited.add(current)
            neighbors = sorted(graph.get(current, {}).keys(), reverse=True)
            for neighbor in neighbors:
                nodes_created += 1
                new_path = path + [neighbor]
                stack.append((neighbor, new_path, cost + graph[current][neighbor]))
    return None, nodes_created, []

def bfs(graph, origin, destinations):
    queue = deque([(origin, [origin], 0)])
    visited = set()
    nodes_created = 1
    while queue:
        current, path, cost = queue.popleft()
        if current in destinations:
            return current, nodes_created, path
        if current not in visited:
            visited.add(current)
            neighbors = sorted(graph.get(current, {}).keys())
            for neighbor in neighbors:
                nodes_created += 1
                new_path = path + [neighbor]
                queue.append((neighbor, new_path, cost + graph[current][neighbor]))
    return None, nodes_created, []

def gbfs(graph, origin, destinations, coords):
    pq = []
    heapq.heappush(pq, (heuristic(origin, destinations, coords), origin, [origin], 0))
    visited = set()
    nodes_created = 1
    while pq:
        h, current, path, cost = heapq.heappop(pq)
        if current in destinations:
            return current, nodes_created, path
        if current not in visited:
            visited.add(current)
            neighbors = sorted(graph.get(current, {}).items(), key=lambda x: x[0])
            for neighbor, edge_cost in neighbors:
                nodes_created += 1
                new_path = path + [neighbor]
                new_h = heuristic(neighbor, destinations, coords)
                heapq.heappush(pq, (new_h, neighbor, new_path, cost + edge_cost))
    return None, nodes_created, []

def astar(graph, origin, destinations, coords):
    pq = []
    initial_h = heuristic(origin, destinations, coords)
    heapq.heappush(pq, (initial_h, 0, origin, [origin]))
    visited = set()
    nodes_created = 1
    while pq:
        f, g, current, path = heapq.heappop(pq)
        if current in destinations:
            return current, nodes_created, path
        if current not in visited:
            visited.add(current)
            neighbors = sorted(graph.get(current, {}).items(), key=lambda x: x[0])
            for neighbor, edge_cost in neighbors:
                nodes_created += 1
                new_g = g + edge_cost
                new_h = heuristic(neighbor, destinations, coords)
                new_f = new_g + new_h
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))
    return None, nodes_created, []

def iddfs(graph, origin, destinations):
    depth = 0
    total_nodes = 0
    while True:
        result, nodes_created, path = depth_limited_dfs(graph, origin, destinations, depth)
        total_nodes += nodes_created
        if result is not None:
            return result, total_nodes, path
        depth += 1

def depth_limited_dfs(graph, origin, destinations, depth_limit):
    stack = [(origin, [origin], 0, 0)]
    visited = set()
    nodes_created = 1
    while stack:
        current, path, cost, depth = stack.pop()
        if current in destinations:
            return current, nodes_created, path
        if depth < depth_limit and current not in visited:
            visited.add(current)
            neighbors = sorted(graph.get(current, {}).keys(), reverse=True)
            for neighbor in neighbors:
                nodes_created += 1
                new_path = path + [neighbor]
                stack.append((neighbor, new_path, cost + graph[current][neighbor], depth + 1))
    return None, nodes_created, []

def bshe(graph, origin, destinations, coords):
    queue = deque([(origin, [origin], 0)])
    visited = set()
    nodes_created = 1
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            current, path, cost = queue.popleft()
            if current in destinations:
                return current, nodes_created, path
            if current not in visited:
                visited.add(current)
                neighbors = graph.get(current, {})
                for neighbor in sorted(neighbors.keys()):
                    nodes_created += 1
                    new_path = path + [neighbor]
                    h = heuristic(neighbor, destinations, coords)
                    level.append((h, neighbor, new_path, cost + neighbors[neighbor]))
        level.sort(key=lambda x: (x[0], x[1]))
        for h, n, p, c in level:
            queue.append((n, p, c))
    return None, nodes_created, []

def main():
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        sys.exit(1)
    
    filename = sys.argv[1]
    method = sys.argv[2].upper()
    
    graph, origin, destinations, coords = parse_file(filename)

    if method == "DFS":
        result, nodes_created, path = dfs(graph, origin, destinations)
    elif method == "BFS":
        result, nodes_created, path = bfs(graph, origin, destinations)
    elif method == "GBFS":
        result, nodes_created, path = gbfs(graph, origin, destinations, coords)
    elif method == "AS":
        result, nodes_created, path = astar(graph, origin, destinations, coords)
    elif method == "CUS1":
        result, nodes_created, path = iddfs(graph, origin, destinations)
    elif method == "CUS2":
        result, nodes_created, path = bshe(graph, origin, destinations, coords)
    else:
        print("Invalid method")
        sys.exit(1)
    
    if result is None:
        print("No path found")
    else:
        print(f"{filename} {method}")
        print(f"{coords[result]} {nodes_created}")
        print(", ".join(map(str, path)))

if __name__ == "__main__":
    main()