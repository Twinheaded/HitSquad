import sys
import argparse
from src.file_parser import FileParser
from src.algorithms.dfs import DFS
from src.algorithms.bfs import BFS
from src.algorithms.gbfs import GBFS
from src.algorithms.a_star import AS
from src.algorithms.iddfs import IDDFS
from src.algorithms.bs import BS


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

    p = FileParser()
    p.parse(args.filename)

    problem = p.create_problem()

    method_obj = None

    match args.method.upper():
        case "DFS":
            method_obj = DFS(problem)
        case "BFS":
            method_obj = BFS(problem)
        case "GBFS":
            method_obj = GBFS(problem)
        case "AS" | "A*":
            method_obj = AS(problem)
        case "CUS1":
            method_obj = IDDFS(problem)
        case "CUS2":
            method_obj = BS(problem)
        case _:
            # Print '...(method) does not exist...' if the user enters a method that does not exist
            print(f"\nSearch method \'{sys.argv[2]}\' does not exist.\nType \'python search.py -h\' for a list of commands.\n")
            exit(0)

    # goal_reached, nodes_searched, result = method_obj.search()
    method_obj.search()
    print(f"{args.filename} {args.method}")
    print(f"{method_obj.result} {len(method_obj.explored)}")
    print(f"{method_obj.final_path}")

if __name__ == '__main__':
    main(sys.argv)
