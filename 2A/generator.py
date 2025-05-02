import sys
import argparse
import pygame
import random
import heapq
import numpy as np

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
X_MARGIN = 200
Y_MARGIN = 100
FONT = pygame.font.SysFont('Arial', 16)
LARGE_FONT = pygame.font.SysFont('Arial', 24)

class GraphGenerator:
    @staticmethod
    def generate_random(num_of_nodes=6, num_of_edges=4, graph_range=(10,10)):
        assert num_of_edges <= (num_of_nodes - 1) * num_of_nodes
        # graph_range - the distance from (0,0) that the nodes will be generated to.
        #   format: (x: 0 to [int], y: 0 to [int])

        nodes = []
        for node_id in range(1, num_of_nodes + 1):
            while True:
                x = random.randint(0, graph_range[0])
                y = random.randint(0, graph_range[1]) 
                closest_node_distance = min([((x-n.coordinates[0])**2 + (y-n.coordinates[1])**2)**0.5 for n in nodes], default=np.inf)

                if not (x, y) in [n.coordinates for n in nodes]:
                    nodes.append(Node(node_id, (x,y)))
                    break
        edges = {}
        possible_actions = [(n1, n2) for n1 in nodes for n2 in nodes if n1 != n2]
        random.shuffle(possible_actions)
        # for n1,n2 in possible_actions[:int(edge_density*len(possible_actions))]:
        for n1,n2 in possible_actions[:num_of_edges]:
            cost = random.randint(1, 10)
            if n1 in edges.keys():
                edges[n1].update({n2:cost})
            else:
                edges[n1] = {n2:cost}
        initial = random.choice(list(nodes))
        goal = random.sample([n for n in nodes if n != initial], min(3, num_of_nodes-1))
        problem = Problem(nodes, initial, goal, edges)
        return problem

    @staticmethod
    def load_from_file(filename):
        p = FileParser()
        p.parse(filename)
        problem = p.create_problem()
        return problem
        
    def draw_graph(problem, path=None, explored=None, method=DFS.name): # Draw graph on screen
        nodes, initial, goals, edges = problem.nodes, problem.initial, problem.goal, problem.edges
        screen.fill(WHITE)
        x_range = (np.inf, -np.inf) # (lowest x-value on the graph, highest x-value on the graph)
        y_range = (np.inf, -np.inf) # (lowest y-value on the graph, highest y-value on the graph)
        
        # Calculate x and y ranges
        for node in nodes:
            nx, ny = node.coordinates
            x_range = (min(x_range[0], nx), max(x_range[1], nx))
            y_range = (min(y_range[0], ny), max(y_range[1], ny))

        # Return the ratio of display size to graph size: (x-multiplier, y-multiplier)
        zoom_multiplier = (abs(W - X_MARGIN*2) / abs(x_range[1] - x_range[0]),
                           abs(H - Y_MARGIN*2) / abs(y_range[1] - y_range[0]))

        # Return the pixel coordinates of the node after fitting to screen
        X_OFFSET = 50
        Y_OFFSET = 20
        zoom = lambda n: (
                X_MARGIN + X_OFFSET + abs(n.coordinates[0] - x_range[0]) * zoom_multiplier[0],
                H - (Y_MARGIN + Y_OFFSET + abs(n.coordinates[1] - y_range[0]) * zoom_multiplier[1])
            )

        # Returns True or False if the mouse is over the current node
        hovering_over_node = lambda n: (
                    pygame.Rect((zoom(n)[0] - NODE_RADIUS, zoom(n)[1] - NODE_RADIUS), (NODE_RADIUS*2, NODE_RADIUS*2)).collidepoint(pygame.mouse.get_pos())
                )

        # For text just underneath the node
        pos_under = lambda pos: (pos[0], pos[1] + 20)
        
        # Draws explored nodes
        for node in explored:
            explored_color = ORANGE
            if node in path:
                explored_color = GREEN

            pygame.draw.circle(screen, explored_color, zoom(node), NODE_RADIUS+2)

        # Returns True or False if the search has reached a dead end on this edge
        dead_end = lambda node, action: (
                node in explored
                and action in explored
                and not node in goals
                and not action in path
            )

        # Returns True or False if the edge belongs to the solution
        solution_edge = lambda node, action: (
                node in path
                and action in path
                and path.index(action)-path.index(node) == 1
            )

        # Returns (x,y) for the midpoint between a node and an action node
        edge_midpoint = lambda n_pos, a_pos: ((n_pos[0]+a_pos[0])//2, (n_pos[1]+a_pos[1])//2)

        # Draw the edges connecting the nodes
        for node in edges:
            for action, cost in edges[node].items():
                color = GRAY
                edge_width_modifier = 0
                n_pos = zoom(node)
                a_pos = zoom(action)
                edge_in_path = False
                if dead_end(node, action):
                    color = ORANGE
                    edge_width_modifier = 0
                if solution_edge(node, action):
                    edge_in_path = True
                    color = GREEN
                    edge_width_modifier = 2
                pygame.draw.line(screen, color, n_pos, a_pos, EDGE_WIDTH + edge_width_modifier)

        # Draw the cost and h(x) information for edges
        for node in edges:
            for action, cost in edges[node].items():
                mid = edge_midpoint(zoom(node), zoom(action))
                if solution_edge(node, action) or hovering_over_node(node):
                    h = problem.distance_heuristic(action)
                    if method == GBFS.name or method == BS.name:
                        heuristic_text = FONT.render(f"h(x): {h:.2f}", True, BLACK)
                        text_centered = heuristic_text.get_rect(center = mid)
                        screen.blit(heuristic_text, (text_centered[0], text_centered[1]-15))
                    if method == AS.name:
                        AS_text = FONT.render(f"c+h(x): {cost + h:.2f}", True, BLACK)
                        text_centered = AS_text.get_rect(center = mid)
                        screen.blit(AS_text, (text_centered[0], text_centered[1]-15))
                    cost_text = FONT.render(f"{cost}", True, BLACK)
                    screen.blit(cost_text, cost_text.get_rect(center = mid))

        # Draw the nodes
        for node in nodes:
            pos = zoom(node)
            color = GRAY
            if node == initial:
                color = GREEN
                goal_text = FONT.render("ORIGIN", True, GREEN)
                screen.blit(goal_text, goal_text.get_rect(center = pos_under(pos)))
            if node in goals:
                color = BLACK
                goal_text = FONT.render("GOAL", True, BLACK)
                screen.blit(goal_text, goal_text.get_rect(center = pos_under(pos)))
            pygame.draw.circle(screen, color, pos, NODE_RADIUS)
            id_text = FONT.render(str(node), True, WHITE)
            screen.blit(id_text, id_text.get_rect(center = pos))

            if hovering_over_node(node):
                coords_text_pos = (pos[0], pos[1] - 25)
                coords_text = FONT.render(str(node.coordinates), True, BLACK)
                screen.blit(coords_text, coords_text.get_rect(center = coords_text_pos))
        
        # Draw text in side panel
        method_text = f"Method: {method}"
        screen.blit(LARGE_FONT.render(method_text, True, BLACK), (10, 10))
        method_options = [DFS, BFS, GBFS, AS, IDDFS, BS]
        for i in range(len(method_options)):
            method_color = BLACK
            if method_options[i].name == method:
                method_color = RED
            screen.blit(FONT.render(f"{i+1}: {method_options[i].name}", True, method_color), (10, 50 + i*20))
        if explored:
            path_text = f"Explored {len(explored)} node{'' if len(explored) == 1 else 's'}: {' → '.join(map(str, explored))}"
            screen.blit(FONT.render(path_text, True, BLACK), (10, H-65))
        if path:
            path_text = f"Final path: [{', '.join(map(str, path))}] (Edges: {len(path)-1})"
        else:
            path_text = "No path found"
        screen.blit(LARGE_FONT.render(path_text, True, BLACK), (10, H-40))

        screen.blit(FONT.render("Number of nodes", True, BLACK), (10, 200))
        screen.blit(FONT.render(str(len(nodes)), True, BLACK), (10, 220))
        screen.blit(FONT.render("Numbers of edges", True, BLACK), (10, 250))
        screen.blit(FONT.render(str(sum([len(n) for n in edges.values()])), True, BLACK), (10, 270))

        new_graph_text = 370
        pygame.draw.rect(screen, GRAY, [0,new_graph_text-10, 155,150], 2)
        screen.blit(FONT.render("N: New Graph", True, BLACK), (10, new_graph_text))
        screen.blit(FONT.render("New graph with...", True, BLACK), (10, new_graph_text + 30))
        screen.blit(FONT.render("▲: One more node", True, BLACK), (10, new_graph_text + 50))
        screen.blit(FONT.render("▼: One less node", True, BLACK), (10, new_graph_text + 70))
        screen.blit(FONT.render("►: Higher % of edges", True, BLACK), (10, new_graph_text + 90))
        screen.blit(FONT.render("◄: Lower % of edges", True, BLACK), (10, new_graph_text + 110))


def create_search_method(key, problem):
    method_obj = None
    match key:
        case BFS.name:
            method_obj = BFS(problem)
        case DFS.name:
            method_obj = DFS(problem)
        case GBFS.name:
            method_obj = GBFS(problem)
        case AS.name | "A*":
            method_obj = AS(problem)
        case IDDFS.name | "CUS1":
            method_obj = IDDFS(problem)
        case BS.name | "CUS2":
            method_obj = BS(problem)
        case _:
            print(f"\nSearch method \'{key}\' does not exist.\nType \'python generator.py -h\' for a list of commands.\n")
            method_obj = None
    return method_obj

def parse_from_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename",
        nargs="?",
        default="PathFinder-test.txt",
        help="Specify file location")
    parser.add_argument(
        "method",
        nargs="?",
        default="DFS",
        help="Specify searching algorithm."
    )
    args = parser.parse_args()

    problem = GraphGenerator.load_from_file(args.filename)
    method_obj = create_search_method(args.method, problem)
    return problem, method_obj

def main(argv):
    num_of_nodes = 10
    num_of_edges = 20

    problem, method_obj = parse_from_args(argv)

    methods = {
        "1": DFS.name,
        "2": BFS.name,
        "3": GBFS.name,
        "4": AS.name,
        "5": IDDFS.name,
        "6": BS.name,
    }

    if method_obj:
        current_method = methods[next(key for key in methods if methods[key] == method_obj.name)]
        method_obj.search()
        
        new_graph_inputs = [pygame.K_n, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    if event.key in new_graph_inputs:  # New graph
                        match event.key:
                            case pygame.K_UP:
                                num_of_nodes += 1
                            case pygame.K_DOWN:
                                num_of_nodes = max(num_of_nodes - 1, 3)
                                num_of_edges = min(num_of_edges, (num_of_nodes - 1) * num_of_nodes)
                            case pygame.K_LEFT:
                                num_of_edges = max(num_of_edges - 1, 0)
                            case pygame.K_RIGHT:
                                num_of_edges = min(num_of_edges + 1, (num_of_nodes - 1) * num_of_nodes)
                        problem = GraphGenerator.generate_random(num_of_nodes, num_of_edges)
                        method_obj = create_search_method(current_method, problem)
                        method_obj.search()
                    elif event.unicode in methods:
                        current_method = methods[event.unicode]
                        method_obj = create_search_method(current_method, problem)
                        method_obj.search()

            GraphGenerator.draw_graph(problem, method_obj.final_path, method_obj.explored, method_obj.name) # Draws graph
            pygame.display.flip() # Updates screen
        
        pygame.quit()

if __name__ == "__main__":
    main(sys.argv)
