from src.file_parser import FileParser

from src.site import Site
from src.link import Link
from src.traffic_problem import TrafficProblem
from src.ars_demo import ars_ml_algorithm_demo
from src.travel_time.travel_time_estimator import TravelTimeEstimator


from src.algorithms.search_method import SearchMethod
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

    print("\nINTERSECTIONS\n================")
    for i in problem.intersections:
        print(i)

    print("\nLINKS (filtered to just site 4043)\n================")
    for link in [l for l in problem.links if l.origin.scats_num == '4043']:
        print(link)

    print("\nTrafficProblem.get_actions('4043')\n================")
    for action in problem.get_actions('4043'):
        print(action)

    print("\nTrafficProblem.goal_test('4043')\n================")
    print(problem.goal_test('4043'))

    print("\nTrafficProblem.distance_heuristic(problem.get_site_by_scats('2000')\n================")
    print(problem.distance_heuristic(problem.get_site_by_scats('2000')))


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


    """
    Author: Jordan
    ===========================
    DEMONSTRATION OF ML-BASED ALGORITHM RECOMMENDATION SYSTEM
    ===========================
    """
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
    ars_ml_algorithm_demo(problem, fp.graph)

if __name__ == "__main__":
    ARS()

    # NOTE: Uncomment any of these to run its demo
    # data_processing_demo(problem)
    #search_method_demo(problem, 'DFS')
   
