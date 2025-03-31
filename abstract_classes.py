from src.utils import *

class Node:
    def __init__(self, state):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.depth = 0

    def __repr__(self):
        return "<Node {}>".format(self.state)

    # This will be used for eliminating repeated states (e.g., in GBFS and A* search methods)
    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)

    
class RouteGraph:
    """Stores the paths between the Nodes (Edges) and their associated cost of traversal

    Typical use:
        routeGraph = RouteGraph()
        routeGraph.connect(node1, node2, 5)
        routeGraph.connect(node1, node3, 1)
        print(routeGraph.get(node1))

    Attributes:
        graph_dict: The mapping of each Node to its Edges. E.g., {<Node 1>: {<Node 2>: 5, <Node 3>: 1}}
    """

    def __init__(self):
        self.graph_dict = {}

    def connect(self, A, B, cost):
        """Add a one-directional link from A to B and attach the cost of traversing from A to B"""
        self.graph_dict.setdefault(A, {})[B] = cost

    def get(self, a, b=None):
        """Return a link cost or a dict of {node: cost} entries.
        .get(a,b) returns the cost or None;
        .get(a) returns a dict of {node: cost} entries, possibly {}."""
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            for key in links:
                if key is b:
                    return links[b]
            raise Exception(f"Connection referenced that does not exist\nOption {a} -> {b}")

    def nodes(self):
        """Return a list of nodes in the graph."""
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)


class RouteFindingProblem(Problem):
    """
    The problem of searching a RouteGraph to traverse from a given Node to any one of the listed destination Nodes

    Attributes:
        graph_dict: The mapping of each Node to its Edges. E.g., {<Node 1>: {<Node 2>: 5, <Node 3>: 1}}
        initial: A Node from which the search begins.
        goal: A list of Nodes that the search will terminate at. E.g., [node1, node2]
        graph: A RouteGraph which stores all of the Edges that connect the Nodes
    """

    def __init__(self, initial, goal, graph):
        self.initial = initial
        self.goal = goal
        self.graph = graph

    def actions(self, A):
        """The current node can traverse to any other node as long as it is connected by an edge (in the correct
        direction)"""
        return list(self.graph.get(A).keys())

    def result(self, state, action):
        """The result of going to a neighbor is just that neighbor."""
        return action

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return is_in(state, self.goal)

    def path_cost(self, A, B, cost_so_far=0):
        return cost_so_far + (self.graph.get(A, B) or np.inf)

    def find_min_edge(self):
        """Find minimum value of edges."""
        m = np.inf
        for d in self.graph.graph_dict.values():
            local_min = min(d.values())
            m = min(m, local_min)

        return m

    # def h(self, node):
    #     # TODO: Implement an appropriate heuristic
