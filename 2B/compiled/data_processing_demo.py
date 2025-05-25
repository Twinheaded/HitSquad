import datetime
from src import FileParser, TrafficProblem, ALGORITHMS
from src.data_structures import Site, Link
# from src.ml_selector import train_and_evaluate, collect_benchmark_data, predict_best_algorithm

# Author: Jack
# ===========================================================
# DEMONSTRATION OF DATA PROCESSING (file parsing -> objects)
# ===========================================================
# These methods show how the data has been parsed and stored
# into objects for further analysis.

def print_sites(problem):
    print("\nSITES\n================")
    print(problem.sites)

def print_intersections(problem):
    printed = False
    print("\nINTERSECTIONS (including the flow records of one intersection)\n================")
    for i in problem.intersections:
        print(i.flow_records)
        if printed:
            print(i)
        printed = True

def print_links(problem, site):
    print("\nLINKS (filtered to just site {site})\n================")
    for link in [l for l in problem.links if l.origin.scats_num == f'{site}']:
        print(link)

def print_actions(problem, site):
    print(f"\nproblem.get_actions(problem.get_site_by_scats('{site}'))\n================")
    for action in problem.get_actions(problem.get_site_by_scats(f'{site}')):
        print(action)

def print_goal_test(problem, site):
    print(f"\nproblem.goal_test(problem.get_site_by_scats('{site}'))\n================")
    print(problem.goal_test(problem.get_site_by_scats(f'{site}')))

def print_heuristic(problem, site):
    print(f"\nproblem.distance_heuristic(problem.get_site_by_scats('{site}'))\n================")
    print(problem.distance_heuristic(problem.get_site_by_scats(f'{site}')))

def print_flow_at_time(problem, site, time=datetime.datetime(2006, 10, 1, 0, 0)):
    print(f"\nproblem.get_flow_at_time(problem.get_site_by_scats('{site}'), {time})\n================")
    print(problem.get_flow_at_time(problem.get_site_by_scats(f'{site}'), time))

def print_travel_time(problem, site1, site2):
    print(f"\nproblem.travel_time(problem.get_site_by_scats('{site1}'), problem.get_site_by_scats('{site2}'))\n================")
    print(problem.travel_time(problem.get_site_by_scats(f'{site1}'), problem.get_site_by_scats(f'{site2}')))

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


# Author: Jordan
# ===========================
# DEMONSTRATION OF ML-BASED ALGORITHM RECOMMENDATION SYSTEM
# ===========================
def ARS():
    # Load and parse dataset
    fp = FileParser("Oct_2006_Boorondara_Traffic_Flow_Data.csv")
    fp.parse()

    # Set up travel time estimator
    flow_dict = fp.get_flow_dict()
    location_dict = fp.get_location_dict()
    estimator = TravelTimeEstimator(flow_dict, location_dict)

    # Create the problem instance
    problem = fp.create_problem('0970', '4040')
    problem.estimator = estimator

    # NOTE: Uncomment the following line to collect benchmark data
    # ars_ml_algorithm_demo(problem, fp.graph)

if __name__ == "__main__":
    fp = FileParser("Oct_2006_Boorondara_Traffic_Flow_Data.csv")
    fp.parse()
    problem = fp.create_problem('2000', '4043') # Arguments: origin, destination

    # NOTE: Uncomment any of these to run its demo
    print_sites(problem)
    print_intersections(problem)
    print_links(problem, '4043')
    print_actions(problem, '4043')
    print_goal_test(problem, '4043')
    print_heuristic(problem, '2000')
    print_flow_at_time(problem, '2000', datetime.datetime(2006, 10, 1, 0, 0))
    print_travel_time(problem, '0970', '2000')

    # ars_ml_algorithm_demo(problem)

