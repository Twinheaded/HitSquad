from .site import Site
from .link import Link
import numpy as np

class TrafficProblem():
    """
    The Traffic-Based Route Guidance Problem.
    Ported from the "Problem" class in 2A - only attribute names have been edited.

    Contains all sites and connecting links.
    """

    def __init__(self, sites, origin, destination, links):
        self.sites = sites      # [<Site>, <Site>, ...] - All sites in the problem
        self.origin = origin    # <Site> - first site of the search
        self.destination = destination        # <Site> - the final site of the search
        self.links = links      # [<Link>, <Link>, ...]
                          
    # Returns a set of states the agent can traverse to from site 's'. 
    def get_actions(self, s):
        actions = {}
        for link in self.links:
            if link.origin == s:
                actions[link.destination] = link.travel_time
        return actions
        # return self.links.setdefault(s, {})

    # Returns a bool: is site 's' the destination?
    def goal_test(self, s):
        return s == self.destination

    # (path_cost() in 2A) returns the travel time of traversing from site A to site B
    def travel_time(self, a, b):
        for link in self.links:
            if link.origin == a and link.destination == b:
                return link.travel_time
        return np.inf

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
