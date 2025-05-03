import numpy as np

class TBRGS():
    """
    The Traffic-Based Route Guidance Problem.
    Ported from the "Problem" class in 2A - only attribute names have been edited.he Traffic-Based 

    Contains all sites and connecting links.
    """

    def __init__(self, sites, origin, goal, edges):
        self.sites = sites      # [<Site>, <Site>, ...] - All sites in the problem
        self.origin = origin    # <Site> - first site of the search
        self.destination = destination        # <Site> - the final site of the search
        self.links = links      # {<Site>:{<Site>:<cost>, <Site>:<cost>, ...}, ...}
                          
    # Returns a set of states the agent can traverse to from site 's'. 
    def get_actions(self, s):
        return self.edges.setdefault(s, {})

    # Returns a bool: is site 's' the destination?
    def goal_test(self, s):
        return s == self.destination

    # (path_cost() in 2A) returns the travel time of traversing from site A to site B
    def travel_time(self, a, b):
        return self.edges[a][b] or np.inf

    # Computes the minimum Euclidian distance from site 's' to the destination
    def distance_heuristic(self, s):
        if s == self.destination:
            return 0
        min_dist = float('inf')
        dx = s.coordinates[0] - self.destination.coordinates[0]
        dy = s.coordinates[1] - self.destination.coordinates[1]
        dist = (dx**2 + dy**2)**0.5  # Euclidean distance
        if dist < min_dist:
            min_dist = dist
        return min_dist
