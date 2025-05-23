from .site import Site
from .link import Link
from src.traffic_utils import flow_to_speed, haversine_distance
import numpy as np
import datetime

class TrafficProblem():
    """
    The Traffic-Based Route Guidance Problem.

    Contains all sites, intersections, and connecting links.
    An origin and destination site are set upon initialisation.
    """
    def __init__(self, sites, intersections, origin, destination, links, time=datetime.time(0,0), estimator=None):
        self.sites = sites # [<Site>, <Site>, ...] - All sites in the problem
        self.intersections = intersections # [<Intersection>, <Intersection>, ...] - All intersections in the problem
        self.origin = next(s for s in self.sites if s.scats_num == origin)    # <Site> - first site of the search
        self.destination = next(s for s in self.sites if s.scats_num == destination)        # <Site> - the final site of the search
        self.links = links # [<Link>, <Link>, ...]
        self.time = time # the current time
        self.estimator = estimator  # TravelTimeEstimator instance
  
    def get_actions(self, s):
        actions = []
        for l in self.links:
            if l.origin.scats_num == s.scats_num:
                actions.append(self.get_site_by_intersection(l.destination))
        return actions

    # Returns a bool: is site 's' the destination?
    def goal_test(self, s):
        return s == self.destination

    # Returns the travel time of traversing from site 'a' to site 'b'
    def travel_time(self, a, b):
        """
        Calculate travel time from Site a to Site b using the estimator.
        """
        if self.estimator is None:
            raise Exception("No estimator assigned to TrafficProblem.")
        return self.estimator.travel_time(a, b, self.time)

    # Computes the  distance of the closest intersections between site 's' and the destination
    def distance_heuristic(self, s):
        """
        Computes the Haversine (great-circle) distance, in km, of the closest intersections between site 's' and the destination
        """
        if self.goal_test(s):
            return 0

        min_dist = float('inf')
        for site_i in s.intersections: # Intersections of site 's'
            for dest_i in self.destination.intersections: # Intersections of the destination site
                dist = haversine_distance(site_i.coordinates[0], site_i.coordinates[1], dest_i.coordinates[0], dest_i.coordinates[1])
                if dist < min_dist:
                    min_dist = dist
        return min_dist

    def get_site_by_scats(self, scats_num):
        for site in self.sites:
            if site.scats_num == scats_num:
                return site
        return None

    def get_site_by_intersection(self, intersection):
        for site in self.sites:
            if intersection in site.intersections:
                return site
        return None
