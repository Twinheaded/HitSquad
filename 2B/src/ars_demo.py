import pandas as pd
from sklearn.utils import resample

from src.ml_selector import (
    train_and_evaluate,
    collect_benchmark_data,
    predict_best_algorithm,
    run_all_algorithms
)

from src.algorithms.dfs import DFS
from src.algorithms.bfs import BFS
from src.algorithms.gbfs import GBFS
from src.algorithms.a_star import AS
from src.algorithms.iddfs import IDDFS
from src.algorithms.bs import BS

ALGORITHMS = {
    "DFS": DFS,
    "BFS": BFS,
    "GBFS": GBFS,
    "AS": AS,
    "IDDFS": IDDFS,
    "BS": BS
}

def ars_ml_algorithm_demo(problem, graph):
    """
    ML-based algorithm recommendation demo
    """
    print("\nStarting Algorithm Recomendation System (ARS)...")
    benchmark_file = "src/data/algorithm_performance.csv"
    X, y_runtime, y_cost = collect_benchmark_data(benchmark_file)

    if len(X) == 0:
        print("No data found. Check your benchmark file.")
        exit()

    # === Balance classes ===
    df = pd.read_csv(benchmark_file)

    df_runtime = df.groupby('best_runtime').apply(
        lambda x: resample(x, replace=True, n_samples=df['best_runtime'].value_counts().max(), random_state=42)
    ).reset_index(drop=True)

    df_cost = df.groupby('best_cost').apply(
        lambda x: resample(x, replace=True, n_samples=df['best_cost'].value_counts().max(), random_state=42)
    ).reset_index(drop=True)

    X_runtime = df_runtime[["num_nodes", "num_edges", "avg_degree", "density"]].values
    y_runtime = df_runtime["best_runtime"].values

    X_cost = df_cost[["num_nodes", "num_edges", "avg_degree", "density"]].values
    y_cost = df_cost["best_cost"].values

    clf_runtime = train_and_evaluate(X_runtime, y_runtime, "Best Runtime")
    clf_cost = train_and_evaluate(X_cost, y_cost, "Best Cost")

    # Run all algorithms
    run_all_algorithms(problem, ALGORITHMS)

    # ML predictions
    best_runtime, best_cost = predict_best_algorithm(graph, clf_runtime, clf_cost)

    # Execute best runtime
    print(f"\n=== Running ARS Algorithm for Best Runtime: {best_runtime} ===")
    AlgorithmClass = ALGORITHMS[best_runtime]
    searchObj = AlgorithmClass(problem)
    searchObj.search()
    print("Result:", getattr(searchObj, "result", None))
    print("Final path:", getattr(searchObj, "final_path", None))

    # Execute best cost
    if best_cost != best_runtime:
        print(f"\n=== Running ARS Algorithm for Best Cost: {best_cost} ===")
        AlgorithmClass = ALGORITHMS[best_cost]
        searchObj = AlgorithmClass(problem)
        searchObj.search()
        print("Result:", getattr(searchObj, "result", None))
        print("Final path:", getattr(searchObj, "final_path", None))
