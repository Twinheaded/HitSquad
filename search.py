import sys
import re
from collections import deque

from src.utils import *

from abstract_classes import *
from search_algorithms import *




def get_data(filename):
    wrong_format_error = "\nInput file is not written in the correct format.\n"

    with open(filename) as f:
        lines = f.read().splitlines()

    i = 0   # Represents the current index of 'lines'

    assert lines[i] == 'Nodes:', wrong_format_error
    i += 1

    node_id = 1                             # Represents the number the node was given. E.g. '3' in '3: (4,4)'
    node_pattern = r'^\d+: \(\d+,\d+\)$'    # RegEx for the text format, '#: (#,#)'

    while re.match(node_pattern, lines[i]) and int(lines[i][0]) == node_id:  # While the line contains ascending node IDs (1,2,3,...) and are in the correct format ('#: (#,#)')
        # TODO:
        # - Create new 'Node' objects for each input line.
        # - Follow the examples from the reference files (in 'READONLY_Resources') to make sure they are set up properly.

        node_id += 1
        i += 1

    assert lines[i] == "Edges:", wrong_format_error
    i += 1

    edge_pattern = r'^\(\d+,\d+\): \d+$'  # RegEx for the text format, '(#,#): #'
    while re.match(edge_pattern, lines[i]):
        # TODO:
        # - Figure out how to associate these edges with the existing nodes.
        i += 1

    assert lines[i] == "" and lines[i+1] == "Origin:" and lines[i+2].isnumeric(), wrong_format_error
    i += 3

    # TODO:
    # - Save the 'Origin:' value into a variable

    assert lines[i] == "Destinations:"
    i += 1

    destination_pattern = r'^\d(; \d)*$' # RegEx for the text format, '#' or '#; #; ... #'
    assert re.match(destination_pattern, lines[i]), wrong_format_error
    
    # TODO:
    # - Save the 'Destinations:' values into a variable






if __name__ == "__main__":

    # The following text is printed if the user inputs '-h', '--h', or a command with too little arguments
    help_string = (
"""
usage: search.py [-h] <filename> <method>

options:
    -h, --help      Show this help message and exit.

commands:
    DFS             Depth-first search
    BFS             Breadth-first search
    GBFS            Greedy best-first search
    AS              A* (A-star) search
    CUS1            Custom search algorithm #1
    CUS2            Custom search algorithm #2
"""
    )

    # ARGUMENT VALIDATION
    
    if len(sys.argv) < 2:           # Print help_string if the user only inputs 'search.py'
        print(help_string)
        exit(0)

    match sys.argv[1]:
        case "-h" | "--help":       # Print help_string if the user inputs '-h', '--help'
            print(help_string)
            exit(0)
        case _:
            if len(sys.argv) != 3:  # Print 'Invalid command...' if the user enters too many arguments
                print(f"\nInvalid command: \'{sys.argv[1]}\'\nType \'python search.py -h\' for a list of commands.\n")
                exit(0)

    # READ <filename> ARGUMENT
    filename = sys.argv[1]
    get_data(filename)

    # READ <method> ARGUMENT
    match sys.argv[2]:
        case "DFS":
            depth_first_search()
        case "BFS":
            breadth_first_search()
        case "GBFS":
            greedy_best_first_search()
        case "AS" | "A*":
            a_star_search()
        case "CUS1":
            custom_search_algorithm_1()
        case "CUS1":
            custom_search_algorithm_2()
        case _:
            # Print '...(method) does not exist...' if the user enters a method that does not exist
            print(f"\nSearch method \'{sys.argv[2]}\' does not exist.\nType \'python search.py -h\' for a list of commands.\n")
            exit(0)

