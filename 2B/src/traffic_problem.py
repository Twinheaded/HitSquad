from .site import Site
from .link import Link
import numpy as np
import datetime

class TrafficProblem():
    def __init__(self, sites, intersections, origin, destination, links, time=datetime.time(0,0), estimator=None):
        self.sites = sites
        self.intersections = intersections
        self.origin = origin
        self.destination = destination
        self.links = links
        self.time = time
        self.estimator = estimator  # TravelTimeEstimator instance

    def get_actions(self, s):
        actions = []
        for l in self.links:
            if l.origin.scats_num == s:
                actions.append(l.destination)
        return actions

    def goal_test(self, s):
        return s == self.destination

    def travel_time(self, a, b):
        """
        Calculate travel time from Site a to Site b using the estimator.
        """
        if self.estimator is None:
            raise Exception("No estimator assigned to TrafficProblem.")
        return self.estimator.travel_time(a, b, self.time)

    def distance_heuristic(self, s):
        dx = s.coordinates[0] - self.destination.coordinates[0]
        dy = s.coordinates[1] - self.destination.coordinates[1]
        return (dx**2 + dy**2)**0.5
