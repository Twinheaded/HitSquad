import csv
import random
import time
import math
import os
from collections import defaultdict

from .traffic_problem import TrafficProblem

from .algorithms.bfs import BFS
from .algorithms.dfs import DFS
from .algorithms.iddfs import IDDFS
from .algorithms.gbfs import GBFS
from .algorithms.a_star import AS

# Algorithms dictionary
ALGORITHMS = {
    "BFS": BFS,
    "DFS": DFS,
    "IDDFS": IDDFS,
    "GBFS": GBFS,
    "ASTAR": AS
}

# Haversine formula to compute lat/lon distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# Load SCATS CSV and extract site info
def parse_scats_csv(file_path):
    scats_sites = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                site = row['SCATS Number'].strip()
                lat = float(row['NB_LATITUDE'])
                lon = float(row['NB_LONGITUDE'])
                volumes = [int(row[f"V{i:02d}"]) for i in range(96) if row.get(f"V{i:02d}")]
                if not volumes:
                    continue
                avg_vol = sum(volumes) / len(volumes)
                scats_sites[site] = {'lat': lat, 'lon': lon, 'volume': avg_vol}
            except:
                continue
    return scats_sites

# Build graph using k-nearest neighbors
def build_graph(scats_sites, k=3):
    graph = defaultdict(list)
    nodes = list(scats_sites.keys())

    for node in nodes:
        lat1, lon1 = scats_sites[node]['lat'], scats_sites[node]['lon']
        distances = []
        for other in nodes:
            if other == node:
                continue
            lat2, lon2 = scats_sites[other]['lat'], scats_sites[other]['lon']
            dist = haversine(lat1, lon1, lat2, lon2)
            distances.append((dist, other))
        distances.sort()
        for _, neighbor in distances[:k]:
            graph[node].append(neighbor)  # Use unweighted graph
    return graph

# Extract graph-level features
def extract_features(graph):
    num_nodes = len(graph)
    num_edges = sum(len(neighbors) for neighbors in graph.values())
    avg_degree = num_edges / num_nodes if num_nodes else 0
    density = num_edges / (num_nodes * (num_nodes - 1)) if num_nodes > 1 else 0
    return num_nodes, num_edges, avg_degree, density

# Run and time a search algorithm
def run_algorithm(AlgorithmClass, graph, start, goal):
    # Use SCATS numbers as both sites and intersections for now
    sites = list(graph.keys())
    intersections = sites
    origin = start
    destination = goal
    # Build links as tuples (origin, destination)
    links = []
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            links.append((node, neighbor))
    problem = TrafficProblem(sites, intersections, origin, destination, links)
    algo = AlgorithmClass(problem)
    start_time = time.time()
    path = algo.search(start, goal)
    end_time = time.time()
    runtime = end_time - start_time
    # If you don't have a get_cost method, just use path length as cost
    cost = len(path) if path else float('inf')
    return runtime, cost

# Main function to collect performance data
def collect_data(scats_csv, output_file="algorithm_performance.csv"):
    print(f"[INFO] Loading SCATS data from: {scats_csv}")
    scats = parse_scats_csv(scats_csv)
    print(f"[INFO] Loaded {len(scats)} SCATS sites.")

    graph = build_graph(scats)
    print(f"[INFO] Graph contains {len(graph)} nodes.")

    num_nodes, num_edges, avg_degree, density = extract_features(graph)

    if len(graph) < 2:
        print("[ERROR] Not enough nodes to run pathfinding.")
        return

    start, goal = random.sample(list(graph.keys()), 2)
    print(f"[INFO] Start: {start}, Goal: {goal}")

    write_header = not os.path.exists(output_file)

    with open(output_file, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'graph_file', 'algorithm', 'runtime', 'cost',
            'num_nodes', 'num_edges', 'avg_degree', 'density',
            'start', 'goal'
        ])
        if write_header:
            writer.writeheader()

        for name, AlgorithmClass in ALGORITHMS.items():
            try:
                print(f"→ Running {name}...")
                runtime, cost = run_algorithm(AlgorithmClass, graph, start, goal)
                writer.writerow({
                    'graph_file': os.path.basename(scats_csv),
                    'algorithm': name,
                    'runtime': runtime,
                    'cost': cost,
                    'num_nodes': num_nodes,
                    'num_edges': num_edges,
                    'avg_degree': avg_degree,
                    'density': density,
                    'start': start,
                    'goal': goal
                })
            except Exception as e:
                print(f"[ERROR] {name} failed: {e}")

if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    for file in os.listdir(data_dir):
        if file.endswith(".csv"):
            collect_data(os.path.join(data_dir, file))
