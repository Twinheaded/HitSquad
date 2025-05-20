import os
import csv
import glob
import numpy as np
from collections import defaultdict
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from .algorithms.bfs import BFS
from .algorithms.dfs import DFS
from .algorithms.iddfs import IDDFS
from .algorithms.gbfs import GBFS
from .algorithms.a_star import AS

from .collect_data import parse_scats_csv, build_graph, extract_features, run_algorithm

ALGORITHMS = {
    "BFS": BFS,
    "DFS": DFS,
    "IDDFS": IDDFS,
    "GBFS": GBFS,
    "ASTAR": AS
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
            y_runtime.append(row['algorithm'])  # or use row['algorithm'] if you want to predict best overall
            y_cost.append(row['algorithm'])     # (if you have separate cost/runtimes, adjust accordingly)
    return np.array(X), np.array(y_runtime), np.array(y_cost)

def train_and_evaluate(X, y, label):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(f"\n=== {label} ===")
    print(classification_report(y_test, y_pred))
    return clf

def predict_best_algorithm(graph, clf_runtime, clf_cost):
    features = np.array(extract_features(graph)).reshape(1, -1)
    best_runtime = clf_runtime.predict(features)[0]
    best_cost = clf_cost.predict(features)[0]
    return best_runtime, best_cost

if __name__ == "__main__":
    benchmark_file = "2B/src/data/algorithm_performance.csv"
    X, y_runtime, y_cost = collect_benchmark_data(benchmark_file)
    clf_runtime = train_and_evaluate(X, y_runtime, "Best Runtime")
    clf_cost = train_and_evaluate(X, y_cost, "Best Cost")
    # Example prediction for a new file
    test_file = "2B/src/data/Oct_2006_Boorondara_Traffic_Flow_Data.csv"
    scats = parse_scats_csv(test_file)
    graph = build_graph(scats)
    features = np.array(extract_features(graph)).reshape(1, -1)
    print("Predicted best for runtime:", clf_runtime.predict(features)[0])
    print("Predicted best for cost:", clf_cost.predict(features)[0])