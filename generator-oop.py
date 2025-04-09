import pygame
import random
import heapq
from collections import deque, defaultdict
from math import sqrt

from src.file_parser import FileParser
from src.algorithms.dfs import DFS
from src.algorithms.bfs import BFS
from src.algorithms.gbfs import GBFS
from src.algorithms.a_star import AS
from src.algorithms.iddfs import IDDFS
from src.algorithms.bs import BS

from src.problem import Problem
from src.node import Node

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
    def generate_random(num_nodes=10, edge_density=0.1):
        nodes = []
        for node_id in range(1, num_nodes + 1):
            while True:
                x = random.randint(MARGIN, W-MARGIN)
                y = random.randint(MARGIN, H-MARGIN)
                if all(sqrt((x-px)**2 + (y-py)**2) > 50 for px, py in [n.coordinates for n in nodes]):
                    nodes.append(Node(node_id, (x,y)))
                    break

        edges = {}

        possible_actions = [(n1, n2) for n1 in nodes for n2 in nodes if n1 != n2]

        random.shuffle(possible_actions)

        for n1,n2 in possible_actions[:int(edge_density*len(possible_actions))]:
            cost = random.randint(1, 10)
            if n1 in edges.keys():
                edges[n1].update({n2:cost})
            else:
                edges[n1] = {n2:cost}


        initial = random.choice(list(nodes))
        goal = random.sample([n for n in nodes if n != initial], min(3, num_nodes-1))
        
        problem = Problem(nodes, initial, goal, edges)
        return problem

    @staticmethod
    def load_from_file(filename):
        p = FileParser()
        p.parse(filename)
        problem = p.create_problem()
        return problem
        
def draw_graph(problem, path=None, explored=None, algorithm="BFS"): # Draw graph on screen

    nodes, initial, goals, edges = problem.nodes, problem.initial, problem.goal, problem.edges

    screen.fill(WHITE)
    
    # Draws edges
    for node in edges:
        for action, cost in edges[node].items():
            color = GRAY
            edge_width_modifier = 0

            if node in path and action in path and path.index(action)-path.index(node) == 1:
                color = GREEN
                edge_width_modifier = 2
                
            pygame.draw.line(screen, color, node.coordinates, action.coordinates, EDGE_WIDTH + edge_width_modifier)
            mid = ((node.coordinates[0]+action.coordinates[0])//2, (node.coordinates[1]+action.coordinates[1])//2)
            screen.blit(FONT.render(str(cost), True, BLACK), (mid[0]-5, mid[1]-5))
    
    # # Draws explored nodes
    for node in explored:
        pygame.draw.circle(screen, BLUE, node.coordinates, NODE_RADIUS+2)
    
    # # Draws nodes
    for node in nodes:
        pos = node.coordinates
        color = GRAY

        if node == initial:
            color = GREEN
            goal_text = FONT.render("ORIGIN", True, GREEN)
            pos_below = (pos[0], pos[1] + 20)
            screen.blit(goal_text, goal_text.get_rect(center = pos_below))
        if node in goals:
            color = RED
            goal_text = FONT.render("GOAL", True, RED)
            pos_below = (pos[0], pos[1] + 20)
            screen.blit(goal_text, goal_text.get_rect(center = pos_below))

        pygame.draw.circle(screen, color, pos, NODE_RADIUS)
        id_text = FONT.render(str(node), True, WHITE)
        screen.blit(id_text, id_text.get_rect(center = pos))
    
    # # Draws info
    algo_text = f"Algorithm: {algorithm} (1:BFS 2:DFS 3:GBFS 4:A* 5:IDDFS 6:BS) | R: New Graph"
    screen.blit(FONT.render(algo_text, True, BLACK), (10, 10))
    
    if path:
        path_text = f"Path: ({','.join(map(str, path))}) (Length: {len(path)-1})"
    else:
        path_text = "No path found"

    screen.blit(LARGE_FONT.render(path_text, True, BLACK), (10, H-30))


def create_search_algorithm(key, problem):
    method_obj = None
    match key:
        case "BFS":
            method_obj = BFS(problem)
        case "DFS":
            method_obj = DFS(problem)
        case "GBFS":
            method_obj = GBFS(problem)
        case "AS":
            method_obj = AS(problem)
        case "IDDFS":
            method_obj = IDDFS(problem)
        case "BS":
            method_obj = BS(problem)
        case _:
            method_obj = None
    return method_obj

def main():
    problem = GraphGenerator.generate_random()

    algorithms = {
        "1": "BFS",
        "2": "DFS",
        "3": "GBFS",
        "4": "AS",
        "5": "IDDFS",
        "6": "BS",
    }

    current_algo = algorithms["2"]

    algo_obj = create_search_algorithm(current_algo, problem)
    algo_obj.search()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_r:  # New graph
                    problem = GraphGenerator.generate_random()
                    algo_obj = create_search_algorithm(current_algo, problem)
                    algo_obj.search()
                elif event.unicode in algorithms:
                    algo_obj = create_search_algorithm(algorithms[event.unicode], problem)
                    algo_obj.search()

        print(algo_obj.final_path, problem.initial, algo_obj.result)

        draw_graph(problem, algo_obj.final_path, algo_obj.explored, algo_obj.name) # Draws graph
        pygame.display.flip() # Updates screen
    
    pygame.quit()

if __name__ == "__main__":
    main()
