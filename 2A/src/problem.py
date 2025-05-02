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

    def distance_heuristic(self, node):
        ###Computes the minimum Euclidean distance from node to any goal.###
        if node in self.goal:
            return 0
        min_dist = float('inf')
        for goal in self.goal:
            dx = node.coordinates[0] - goal.coordinates[0]
            dy = node.coordinates[1] - goal.coordinates[1]
            dist = (dx**2 + dy**2)**0.5  # Euclidean distance
            if dist < min_dist:
                min_dist = dist
        return min_dist
