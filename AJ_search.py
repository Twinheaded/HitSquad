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
        node_id = int(metric[0])    # Numeric
        x = int(metric[4])          # Numeric
        y = int(metric[6])          # Numeric
        nodes[node_id] = Node(node_id,x,y)
        print(f"{nodes[node_id]} ({x},{y})")
        metric = f.readline().strip()

    graph = Graph()

    print('Edges:')
    metric = f.readline().strip()
    while metric:
        assert re.match(r'^\(\d+,\d+\): \d+$', metric)  # RegEx for the text format, '(#,#): #'

        s = nodes[int(metric[1])]          # state      - the 'from' address (Node)
        t = nodes[int(metric[3])]          # transition - the 'to' address (Node)
        c = int(metric[7])          # cost       - the expense of traversing (Numeric)
        print(f"{s} -> {t} cost: {c}")
        graph.connect(s, t, c)      # Adds an edge from s -> t with a cost of c
        metric = f.readline().strip()

    assert f.readline().strip() == 'Origin:', wrong_format_error
    origin = nodes[int(f.readline().strip())] # Origin (Node)
    print(f"Origin: {origin}")

    assert f.readline().strip() == 'Destinations:', wrong_format_error
    destinations = f.readline().strip() # Destinations
    assert re.match(r'^\d+(; \d+)*$', destinations), wrong_format_error # RegEx for '#' or '#; #; ... #'
    destinations = [nodes[int(i.lstrip())] for i in destinations.split(";")] 
    print(f"Destinations: {destinations}\n")

    return RouteFindingProblem(origin, destinations, graph)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename",
        default="tests/PathFinder_test.txt",
        help="Specify File Location")
    parser.add_argument(
        "method",
        default="BFS",
        help="Specify Searching Algorithm."
    )
    args = parser.parse_args()
    method = args.searchalgo
    method = "A*" if method == "AS" else method

    problem = File_Reader(args.file)

    result = {}

    match method:
        case "DFS":
            result = depth_first_search(problem)
        case "BFS":
            result = breadth_first_search(problem)
        case "GBFS":
            result = greedy_best_first_search(problem)
        case "AS" | "A*":
            method = "A*"
            result = a_star_search(problem)
        case "CUS1":
            result = custom_search_algorithm_1(problem)
        case "CUS2":
            result = custom_search_algorithm_2(problem)
        case _:
            # Print '...(method) does not exist...' if the user enters a method that does not exist
            print(f"\nSearch method \'{sys.argv[2]}\' does not exist.\nType \'python search.py -h\' for a list of commands.\n")
            exit(0)

    print("\nSOLUTION:", " -> ".join(map(str, result)), "\n")

if __name__ == '__main__':
    main(sys.argv)

