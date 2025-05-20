from src.file_parser import FileParser

from src.site import Site
from src.link import Link
from src.traffic_problem import TrafficProblem
from src.ml_selector import train_and_evaluate, collect_benchmark_data, predict_best_algorithm


from src.algorithms.search_method import SearchMethod
from src.algorithms.bfs import BFS
from src.algorithms.a_star import AS
from src.algorithms.bs import BS
from src.algorithms.dfs import DFS
from src.algorithms.gbfs import GBFS
from src.algorithms.iddfs import IDDFS


ALGORITHMS = {
    "BFS": BFS,
    "DFS": DFS,
    "IDDFS": IDDFS,
    "GBFS": GBFS,
    "ASTAR": AS
}



if __name__ == "__main__":
    fp = FileParser("Oct_2006_Boorondara_Traffic_Flow_Data.csv")
    fp.parse()

    problem = fp.create_problem('2000', '4043') # Arguments: origin, destination

    # print("\nSITES\n================")
    # print(problem.sites)

    # print("\nINTERSECTIONS\n================")
    # for i in problem.intersections:
    #     print(i)

    # print("\nLINKS (filtered to just site 4043)\n================")
    # for link in [l for l in problem.links if l.origin.scats_num == '4043']:
    #     print(link)

    # print("\nTrafficProblem.get_actions('4043')\n================")
    # for action in problem.get_actions('4043'):
    #     print(action)

    # print("\nTrafficProblem.goal_test('4043')\n================")
    # print(problem.goal_test('4043'))

    # print("\nTrafficProblem.distance_heuristic(problem.get_site_by_scats('2000')\n================")
    # print(problem.distance_heuristic(problem.get_site_by_scats('2000')))

    # ===========================
    # ML DEMONSTRATION CODE
    # ===========================

    # print("\nStarting Algorithm Recomendation System(ARS)...")
    # benchmark_file = "2B/src/data/algorithm_performance.csv"
    # X, y_runtime, y_cost = collect_benchmark_data(benchmark_file)

    # if len(X) == 0:
    #    print("No data found in data directory or data could not be parsed. Please check your data files.")
    #    exit()

    # clf_runtime = train_and_evaluate(X, y_runtime, "Best Runtime")
    # clf_cost = train_and_evaluate(X, y_cost, "Best Cost")

    # best_runtime, best_cost = predict_best_algorithm(problem.graph, clf_runtime, clf_cost)
    # print(f"ML predicts best for runtime: {best_runtime}")
    # print(f"ML predicts best for cost: {best_cost}")

    # AlgorithmClass = ALGORITHMS[best_runtime]
    # searchObj = AlgorithmClass(problem)
    # searchObj.search()
    # print("Result:", searchObj.result)

    # ===========================
    # TODO: Make this code work:
    i = 1
    match i:
        case 1: 
            searchObj = DFS(problem)
        case 2:
            searchObj = BFS(problem)
        case 3:
            searchObj = GBFS(problem)
        case 4:
            searchObj = AS(problem)
        case 5:
            searchObj = IDDFS(problem)
        case 6:
            searchObj = BS(problem)
    searchObj.search()
    print(searchObj.result)
    print(searchObj.final_path)
    print(len(searchObj.final_path))
