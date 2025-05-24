import datetime
from src import FileParser, TrafficProblem, ALGORITHMS
from src.data_structures import Site, Link
# from src.ml_selector import train_and_evaluate, collect_benchmark_data, predict_best_algorithm

def data_processing_demo(problem):
    """
    Author: Jack
    ===========================================================
    DEMONSTRATION OF DATA PROCESSING (file parsing -> objects)
    ===========================================================
    This method shows how the data has been parsed and stored
    into objects for further analysis.
    """
    
    print("\nSITES\n================")
    print(problem.sites)

    # printed = False
    # print("\nINTERSECTIONS\n================")
    # for i in problem.intersections:
    #     print(i.flow_records)
    #     if printed:
    #         print(i)
    #     printed = True

    print("\nLINKS (filtered to just site 4043)\n================")
    for link in [l for l in problem.links if l.origin.scats_num == '4043']:
        print(link)

    print("\nproblem.get_actions(problem.get_site_by_scats('4043'))\n================")
    for action in problem.get_actions(problem.get_site_by_scats('4043')):
        print(action)

    print("\nproblem.goal_test(problem.get_site_by_scats('4043'))\n================")
    print(problem.goal_test(problem.get_site_by_scats('4043')))

    print("\nproblem.distance_heuristic(problem.get_site_by_scats('2000'))\n================")
    print(problem.distance_heuristic(problem.get_site_by_scats('2000')))

    print("\nproblem.get_flow_at_time(problem.get_site_by_scats('0970'), datetime.datetime(2006, 10, 1, 0, 0))\n================")
    print(problem.get_flow_at_time(problem.get_site_by_scats('0970'), datetime.datetime(2006, 10, 1, 0, 0)))

    print("\nproblem.travel_time(problem.get_site_by_scats('0970'), problem.get_site_by_scats('2000'))\n================")
    print(problem.travel_time(problem.get_site_by_scats('0970'), problem.get_site_by_scats('2000')))


def search_method_demo(problem, search_method):
    """
    Author: Jack
    ===================================
    DEMONSTRATION OF SEARCH ALGORITHMS
    ===================================
    """
    searchObj = ALGORITHMS[search_method](problem)

    searchObj.search()
    print()
    print("Search method:", searchObj.name)
    print("Result:", searchObj.result)
    print("Final path:", searchObj.final_path, "\n")
    print("Explored:", searchObj.explored)
    print("(", len(searchObj.explored), "intersections explored )\n")

def ars_ml_algorithm_demo(problem):
    """
    Author: Jordan
    ===========================
    ML DEMONSTRATION CODE
    ===========================
    """

    print("\nStarting Algorithm Recomendation System(ARS)...")
    benchmark_file = "2B/src/data/algorithm_performance.csv"
    X, y_runtime, y_cost = collect_benchmark_data(benchmark_file)

    if len(X) == 0:
       print("No data found in data directory or data could not be parsed. Please check your data files.")
       exit()

    clf_runtime = train_and_evaluate(X, y_runtime, "Best Runtime")
    clf_cost = train_and_evaluate(X, y_cost, "Best Cost")

    best_runtime, best_cost = predict_best_algorithm(problem.graph, clf_runtime, clf_cost)
    print(f"ML predicts best for runtime: {best_runtime}")
    print(f"ML predicts best for cost: {best_cost}")

    AlgorithmClass = ALGORITHMS[best_runtime]
    searchObj = AlgorithmClass(problem)
    searchObj.search()
    print("Result:", searchObj.result)


if __name__ == "__main__":
    fp = FileParser("Oct_2006_Boorondara_Traffic_Flow_Data.csv")
    fp.parse()
    problem = fp.create_problem('2000', '4043') # Arguments: origin, destination

    # NOTE: Uncomment any of these to run its demo
    data_processing_demo(problem)
    # search_method_demo(problem, 'DFS')
    # ars_ml_algorithm_demo(problem)
