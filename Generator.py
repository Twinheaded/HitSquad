import pygame
import random
import heapq
from collections import deque, defaultdict
from math import sqrt

# Setup
pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Graph Generator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Settings
NODE_RADIUS = 10
EDGE_WIDTH = 2
MARGIN = 50
FONT = pygame.font.SysFont('Arial', 16)
LARGE_FONT = pygame.font.SysFont('Arial', 24)

class GraphGenerator:
    @staticmethod
    def generate_random(num_nodes=10, edge_density=0.3):
        nodes = {}
        for node_id in range(1, num_nodes + 1):
            while True:
                x = random.randint(MARGIN, W-MARGIN)
                y = random.randint(MARGIN, H-MARGIN)
                if all(sqrt((x-px)**2 + (y-py)**2) > 50 for px, py in nodes.values()):
                    nodes[node_id] = (x, y)
                    break

        edges = []
        possible = [(i,j) for i in nodes for j in nodes if i < j]
        random.shuffle(possible)
        
        for i,j in possible[:int(edge_density*len(possible))]:
            cost = random.randint(1, 10)
            edges.extend([(i,j,cost), (j,i,cost)])  # Bidirectional

        start = random.choice(list(nodes))
        goals = random.sample([n for n in nodes if n != start], min(3, num_nodes-1))
        
        return nodes, edges, start, goals

class Problem:
    def __init__(self, nodes, edges, start, goals): 
        self.nodes = nodes
        self.edges = edges
        self.start = start
        self.goals = goals
        self.graph = defaultdict(list) # Adjacency list
        for i,j,_ in edges:
            self.graph[i].append(j) # Bidirectional
    
    def initial_state(self):
        return self.start
    
    def is_goal(self, state):
        return state in self.goals
    
    def get_actions(self, state):
        return self.graph.get(state, [])
    
    def get_heuristic(self, state):
        if not self.goals:
            return 0
        x1, y1 = self.nodes[state]
        min_distance = float('inf')
        for goal in self.goals:
            x2, y2 = self.nodes[goal]
            distance = sqrt((x1-x2)**2 + (y1-y2)**2) # Euclidean distance
            if distance < min_distance:
                min_distance = distance
        return min_distance
    
    def get_cost(self, from_state, to_state):
        for start, end, cost in self.edges:
            if start == from_state and end == to_state:
                return cost
        return 1  # Default cost

# Search algorithm implementations
def breadth_first_search(problem):
    frontier = deque([problem.initial_state()])
    explored = set()
    parent = {}
    
    while frontier:
        state = frontier.popleft()
        if problem.is_goal(state):
            # Reconstruct path
            path = [state]
            while state in parent:
                state = parent[state]
                path.append(state)
            return list(reversed(path))
        
        if state not in explored:
            explored.add(state)
            for neighbor in problem.get_actions(state):
                if neighbor not in explored and neighbor not in frontier:
                    parent[neighbor] = state
                    frontier.append(neighbor)
    return None

def depth_first_search(problem):
    frontier = [problem.initial_state()]
    explored = set()
    parent = {}
    
    while frontier:
        state = frontier.pop()
        if problem.is_goal(state):
            # Reconstruct path
            path = [state]
            while state in parent:
                state = parent[state]
                path.append(state)
            return list(reversed(path))
        
        if state not in explored:
            explored.add(state)
            for neighbor in reversed(problem.get_actions(state)):  # For left-right order
                if neighbor not in explored:
                    parent[neighbor] = state
                    frontier.append(neighbor)
    return None

def greedy_best_first_search(problem):
    frontier = []
    heapq.heappush(frontier, (0, problem.initial_state()))
    explored = set()
    parent = {}
    
    while frontier:
        _, state = heapq.heappop(frontier)
        if problem.is_goal(state):
            # Reconstruct path
            path = [state]
            while state in parent:
                state = parent[state]
                path.append(state)
            return list(reversed(path))
        
        if state not in explored:
            explored.add(state)
            for neighbor in problem.get_actions(state):
                if neighbor not in explored:
                    parent[neighbor] = state
                    heapq.heappush(frontier, (problem.get_heuristic(neighbor), neighbor))
    return None

def a_star_search(problem):
    frontier = []
    heapq.heappush(frontier, (0, 0, problem.initial_state()))  # (priority, cost, state)
    explored = set()
    parent = {}
    cost_so_far = {problem.initial_state(): 0}
    
    while frontier:
        _, cost, state = heapq.heappop(frontier)
        if problem.is_goal(state): # Reconstruct path
            path = [state]
            while state in parent:
                state = parent[state]
                path.append(state)
            return list(reversed(path))
        
        if state not in explored:
            explored.add(state)
            for neighbor in problem.get_actions(state):
                new_cost = cost + problem.get_cost(state, neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + problem.get_heuristic(neighbor)
                    heapq.heappush(frontier, (priority, new_cost, neighbor))
                    parent[neighbor] = state
    return None

def iterative_deepening_dfs(problem):
    def dls(node, depth, visited, path):
        if problem.is_goal(node):
            return path + [node]
        if depth <= 0:
            return None
        
        visited.add(node)
        for neighbor in problem.get_actions(node):
            if neighbor not in visited:
                result = dls(neighbor, depth-1, visited.copy(), path + [node])
                if result is not None:
                    return result
        return None
    
    depth = 0
    while True:
        visited = set()
        result = dls(problem.initial_state(), depth, visited, [])
        if result is not None:
            return result
        depth += 1 # Increment depth
        if depth > len(problem.nodes) * 2: # Depth limit
            return None

def bidirectional_search(problem):
    if not problem.goals:
        return None
    
    forward_frontier = deque([problem.initial_state()]) 
    forward_visited = {problem.initial_state(): None}
    
    backward_frontier = deque()
    backward_visited = {}
    for goal in problem.goals:
        backward_frontier.append(goal)
        backward_visited[goal] = None
    
    intersection = None
    
    while forward_frontier and backward_frontier: # While both frontiers are not empty
        current_forward = forward_frontier.popleft()
        if current_forward in backward_visited:
            intersection = current_forward
            break
            
        for neighbor in problem.get_actions(current_forward):
            if neighbor not in forward_visited:
                forward_visited[neighbor] = current_forward
                forward_frontier.append(neighbor)
        
        current_backward = backward_frontier.popleft() # Left-right order
        if current_backward in forward_visited:
            intersection = current_backward
            break
            
        for neighbor in problem.get_actions(current_backward):
            if neighbor not in backward_visited:
                backward_visited[neighbor] = current_backward
                backward_frontier.append(neighbor)
    
    if not intersection:
        return None
    
    path = [intersection] # Intersection is in both frontiers

    # Forward path
    node = intersection
    while node in forward_visited and forward_visited[node] is not None:
        node = forward_visited[node]
        path.insert(0, node)
    
    # Backward path
    node = intersection
    while node in backward_visited and backward_visited[node] is not None:
        node = backward_visited[node]
        path.append(node)
    
    return path

def draw_graph(nodes, edges, start, goals, path=None, explored=None, algorithm="BFS"): # Draw graph on screen
    screen.fill(WHITE)
    
    # Draws edges
    for i,j,c in edges:
        color = YELLOW if path and i in path and j in path and abs(path.index(i)-path.index(j))==1 else GRAY
        pygame.draw.line(screen, color, nodes[i], nodes[j], EDGE_WIDTH)
        mid = ((nodes[i][0]+nodes[j][0])//2, (nodes[i][1]+nodes[j][1])//2)
        screen.blit(FONT.render(str(c), True, BLACK), (mid[0]-5, mid[1]-5))
    
    # Draws explored nodes
    if explored:
        for node in explored:
            pygame.draw.circle(screen, PURPLE, nodes[node], NODE_RADIUS+2)
    
    # Draws nodes
    for node, pos in nodes.items():
        color = GREEN if node == start else RED if node in goals else BLUE
        pygame.draw.circle(screen, color, pos, NODE_RADIUS)
        screen.blit(FONT.render(str(node), True, WHITE), (pos[0]-5, pos[1]-5))
    
    # Draws info
    algo_text = f"Algorithm: {algorithm} (1:BFS 2:DFS 3:GBFS 4:A* 5:IDDFS 6:BS) | R: New Graph"
    screen.blit(FONT.render(algo_text, True, BLACK), (10, 10))
    
    if path:
        path_text = f"Path: ({','.join(map(str, path))}) (Length: {len(path)-1})"
        screen.blit(LARGE_FONT.render(path_text, True, BLACK), (10, H-30))

def main():
    nodes, edges, start, goals = GraphGenerator.generate_random()
    problem = Problem(nodes, edges, start, goals)
    
    algorithms = {
        "1": ("BFS", breadth_first_search),
        "2": ("DFS", depth_first_search),
        "3": ("GBFS", greedy_best_first_search),
        "4": ("A*", a_star_search),
        "5": ("IDDFS", iterative_deepening_dfs),
        "6": ("BS", bidirectional_search)
    }
    current_algo = "1"
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # New graph
                    nodes, edges, start, goals = GraphGenerator.generate_random()
                    problem = Problem(nodes, edges, start, goals)
                elif event.unicode in algorithms:
                    current_algo = event.unicode
        
        # Runs algorithm
        algo_name, algo_func = algorithms[current_algo]
        path = algo_func(problem)
        explored = None # For GBFS and A*
        
        draw_graph(nodes, edges, start, goals, path, explored, algo_name) # Draws graph
        pygame.display.flip() # Updates screen
    
    pygame.quit()

if __name__ == "__main__":
    main()