from .data_structures import TrafficProblem, Site, Intersection, Link
from .search_methods import SearchMethod, DFS, BFS, GBFS, AS, IDDFS, BS

ALGORITHMS = {
    "DFS": DFS,
    "BFS": BFS,
    "GBFS": GBFS,
    "AS": AS,
    "IDDFS": IDDFS,
    "BS": BS
}
