import os
import sys
import argparse
import re
from jack_classes import *
from search_algorithms import * 

def File_Reader(file):

    wrong_format_error = "\nInput file is not written in the correct format.\n"
    nodes = {} # Nodes

    f = open(file, "r")

    assert f.readline().strip() == 'Nodes:', wrong_format_error
    print('Nodes:')

    metric = f.readline().strip()
    while metric != "Edges:":
        assert re.match(r'^\d+: \(\d+,\d+\)$', metric), wrong_format_error # RegEx for '#: (#,#)'
        print(metric)
        node_id = int(metric[0])    # Numeric
        x = int(metric[4])          # Numeric
        y = int(metric[6])          # Numeric
        nodes[node_id] = Node(node_id,x,y)
        metric = f.readline().strip()

    graph = Graph()

    metric = f.readline().strip()
    while metric:
        s = nodes[int(metric[1])]   # state      - the 'from' address (Node)
        t = nodes[int(metric[3])]   # transition - the 'to' address (Node)
        c = int(metric[7])          # cost       - the expense of traversing (Numeric)
        graph.connect(s, t, c)      # Adds an edge from s -> t with a cost of c
        metric = f.readline().strip()

    assert f.readline().strip() == 'Origin:', wrong_format_error
    origin = nodes[int(f.readline().strip())] # Origin (Node)

    assert f.readline().strip() == 'Destinations:', wrong_format_error
    destinations = f.readline().strip() # Destinations
    assert re.match(r'^\d+(; \d+)*$', destinations), wrong_format_error # RegEx for '#' or '#; #; ... #'
    destinations = [nodes[int(i.lstrip())] for i in destinations.split(";")] 

    return RouteFindingProblem(origin, destinations, graph)

# This is won't be needed, since the Problem.path_cost() method handles it 
############################################################################
# def CostFinder (node1, node2):
#     try:
#         key = (str(node1), str(node2))
#         cost = edges[key]
#         return cost
#     except:
#         return "Path Not Viable"

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        default="tests/PathFinder_test.txt",
        help="Specify File Location")
    parser.add_argument(
        "--searchalgo",
        default="BFS",
        help="Specify Searching Algorithm."
    )
    args = parser.parse_args()

    problem = File_Reader(args.file)

    result = {}

    match args.searchalgo:
        case "DFS":
            result = depth_first_search(problem)
        case "BFS":
            result = breadth_first_search(problem)
        case "GBFS":
            result = greedy_best_first_search(problem)
        case "AS" | "A*":
            result = a_star_search(problem)
        case "CUS1":
            result = custom_search_algorithm_1(problem)
        case "CUS2":
            result = custom_search_algorithm_2(problem)
        case _:
            # Print '...(method) does not exist...' if the user enters a method that does not exist
            print(f"\nSearch method \'{sys.argv[2]}\' does not exist.\nType \'python search.py -h\' for a list of commands.\n")
            exit(0)

    print(result)

if __name__ == '__main__':
    main(sys.argv)

