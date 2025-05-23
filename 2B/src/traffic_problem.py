from .site import Site
from .link import Link
from src.travel_time.traffic_utils import haversine_distance
import numpy as np
import datetime

class TrafficProblem():
    def __init__(self, sites, intersections, origin, destination, links, time=datetime.time(0,0), estimator=None):
        self.sites = sites
        self.intersections = intersections
        self.origin = origin  # Site object
        self.destination = destination  # Site object
        self.links = links
        self.time = time
        self.estimator = estimator

        self.initial = origin
        self.goal = destination

    def get_actions(self, s):
        actions = []
        for l in self.links:
            if hasattr(s, "scats_num") and l.origin.scats_num == s.scats_num:
                site = self.get_site_by_intersection(l.destination.scats_num)
                if site is not None:
                    actions.append(site)
        return actions

    def goal_test(self, s):
        return s == self.destination

    def travel_time(self, a, b):
        if self.estimator is None:
            raise Exception("No estimator assigned to TrafficProblem.")
        return self.estimator.travel_time(a, b, self.time)

    def distance_heuristic(self, s):
        """
        Computes the Haversine distance between the first intersection of s and destination.
        Falls back to (0,0) if coordinates are unavailable.
        """
        try:
            if not s.intersections or not self.destination.intersections:
                return float('inf')
            return haversine_distance(
                s.intersections[0].coordinates[0], s.intersections[0].coordinates[1],
                self.destination.intersections[0].coordinates[0], self.destination.intersections[0].coordinates[1]
            )
        except Exception:
            return float('inf')

    def get_site_by_intersection(self, scats_num):
        return next((site for site in self.sites if site.scats_num == scats_num), None)
