import os
import sys
import argparse
import search_algorithms
from search_algorithms import breadth_first_search
print(dir(search_algorithms))


def File_Reader(file):

    f = open(file, "r")
    print(f.readline())
    metric = f.readline().strip()
    nodes = {} # Nodes

    while metric != "Edges:":
        print(metric)
        num = (metric[0]) #Strings
        x = int(metric[4])  #Numeric
        y = int(metric[6])  #Numeric
        nodes[num] = (x,y)
        metric = f.readline().strip()

    metric = f.readline().strip()

    edges = {} #Edges
    graph = {} #Graph

    while metric:
        #print(metric)
        start = metric[1] #Strings
        stop = metric[3] #Strings
        val = int(metric[7]) #Numeric
        if start in graph:
            graph[start].append(stop)
        else:
            graph[start] = [stop]
        edges[(start,stop)] = val
        metric = f.readline().strip()

    f.readline()
    origin = f.readline().strip() #Origin
    f.readline()
    destination = f.readline().strip() #Destinations
    destination = [i.lstrip() for i in destination.split(";")] 
    #print(destination)
    #print(graph)

    return nodes, edges, graph, origin, destination

def CostFinder (node1, node2):
    try:
        key = (str(node1), str(node2))
        cost = edges[key]
        return cost
    except:
        return "Path Not Viable"


    

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        default="tests/PathFinder_test.txt",
        help="Specify File Location")
    parser.add_argument(
        "--searchalgo",
        default="BFS",
        help="Specific Scat Value."
    )
    args = parser.parse_args()

    
    nodes, edges, graph, origin, destination = File_Reader(args.file)
    #print(destination)
    finalpaths = breadth_first_search(origin, destination, graph)
    print(finalpaths)

if __name__ == '__main__':
    main(sys.argv)

