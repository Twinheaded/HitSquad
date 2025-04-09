import numpy as np

class Problem():
    """
    Contains all nodes and connecting edges.
    """

    def __init__(self, nodes, initial, goal, edges):
        self.nodes = nodes      # [<Node>, <Node>, ...] - All nodes in the problem
        self.initial = initial  # <Node> - first node of the search
        self.goal = goal        # [<Node>, <Node>, ...] - a list of goal states
        self.edges = edges      # {<Node>:{<Node>:<cost>, <Node>:<cost>, ...}, ...}
                          
    # Returns a set of states the agent can traverse to from node 'n'. 
    def get_actions(self, n):
        return self.edges.setdefault(n, {})

    # Checks if node 'n' is a goal state
    def goal_test(self, n):
        return n in self.goal

    # Returns the cost of traversing from state 's' to transition 't'
    def path_cost(self, s, t):
        return self.edges[s][t] or np.inf
