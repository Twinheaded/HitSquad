import csv
import os
import time
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from .algorithms.bfs import BFS
from .algorithms.dfs import DFS
from .algorithms.iddfs import IDDFS
from .algorithms.gbfs import GBFS
from .algorithms.a_star import AS
from .algorithms.bs import BS

from src.travel_time.travel_time_estimator import TravelTimeEstimator
from src.file_parser import FileParser

ALGORITHMS = {
    "BFS": BFS,       #working
    "DFS": DFS,       #working
    "IDDFS": IDDFS,   #working
    "GBFS": GBFS,     #working
    "ASTAR": AS,      #working
    "BS": BS          #working
}

def collect_benchmark_data(benchmark_file):
    X, y_runtime, y_cost = [], [], []
    with open(benchmark_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            features = [
                float(row['num_nodes']),
                float(row['num_edges']),
                float(row['avg_degree']),
                float(row['density'])
            ]
            X.append(features)
            y_runtime.append(row['best_runtime'])
            y_cost.append(row['best_cost'])
    return np.array(X), np.array(y_runtime), np.array(y_cost)

def extract_features_from_fileparser(graph):
    num_nodes = len(graph)
    num_edges = sum(len(neighbors) for neighbors in graph.values()) // 2
    avg_degree = (2 * num_edges) / num_nodes if num_nodes > 0 else 0
    density = (2 * num_edges) / (num_nodes * (num_nodes - 1)) if num_nodes > 1 else 0
    return [num_nodes, num_edges, avg_degree, density]

def train_and_evaluate(X, y, label):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(f"\n=== {label} ===")
    print(classification_report(y_test, y_pred))
    return clf

def predict_best_algorithm(graph, clf_runtime, clf_cost):
    features = np.array(extract_features_from_fileparser(graph)).reshape(1, -1)
    best_runtime = clf_runtime.predict(features)[0]
    best_cost = clf_cost.predict(features)[0]
    return best_runtime, best_cost

def collect_benchmark_data_from_fileparser():
    data_file = "Oct_2006_Boorondara_Traffic_Flow_Data.csv"
    output_csv = "src/data/algorithm_performance.csv"
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    fp = FileParser(data_file)
    fp.parse()

    flow_dict = fp.get_flow_dict()
    location_dict = fp.get_location_dict()
    estimator = TravelTimeEstimator(flow_dict, location_dict)

    origins = fp.sites          #[:5]         # First 5 sites for testing
    destinations = fp.sites     #[:5]    # First 5 sites for testing

    with open(output_csv, "w", newline="") as csvfile:
        fieldnames = ["origin", "destination", "num_nodes", "num_edges", "avg_degree", "density",
                      "best_runtime", "best_cost"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        total = len(origins) * len(destinations)
        count = 0
        for origin in origins:
            for dest in destinations:
                if origin == dest:
                    continue
                count += 1
                print(f"Processing {count}/{total}: {origin.scats_num} -> {dest.scats_num}")

                try:
                    problem = fp.create_problem(origin.scats_num, dest.scats_num)
                    problem.estimator = estimator

                    features = extract_features_from_fileparser(fp.graph)

                    results = {}
                    for name, Algo in ALGORITHMS.items():
                        try:
                            searchObj = Algo(problem)
                            start = time.time()
                            searchObj.search()
                            runtime = time.time() - start
                            cost = len(searchObj.final_path) if hasattr(searchObj, "final_path") and searchObj.final_path else float('inf')
                        except Exception as e:
                            print(f"{name} failed for ({origin.scats_num}->{dest.scats_num}): {e}")
                            runtime = float('inf')
                            cost = float('inf')
                        results[name] = {"runtime": runtime, "cost": cost}

                    best_runtime = min(results, key=lambda k: results[k]["runtime"])
                    best_cost = min(results, key=lambda k: results[k]["cost"])

                    row = {
                        "origin": origin.scats_num,
                        "destination": dest.scats_num,
                        "num_nodes": features[0],
                        "num_edges": features[1],
                        "avg_degree": features[2],
                        "density": features[3],
                        "best_runtime": best_runtime,
                        "best_cost": best_cost
                    }

                    print(row)
                    writer.writerow(row)

                except Exception as e:
                    print(f"Failed to process ({origin.scats_num} -> {dest.scats_num}): {e}")

    print("Number of sites:", len(fp.sites))

if __name__ == "__main__":
    collect_benchmark_data_from_fileparser()
    print("Benchmark data collection complete!")
    print("Data saved to: src/data/algorithm_performance.csv")
    print("You can now run the ARS ML algorithm demo.")
