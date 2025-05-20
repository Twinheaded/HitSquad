from .site import Site
from .link import Link
import numpy as np
import datetime

class TrafficProblem():
    """
    The Traffic-Based Route Guidance Problem.
    Ported from the "Problem" class in 2A - only attribute names have been edited.

    Contains all sites and connecting links.
    """

    def __init__(self, sites, intersections, origin, destination, links, time=datetime.time(0,0,0,0)):
        self.sites = sites      # [<Site>, <Site>, ...] - All sites in the problem
        self.intersections = intersections  # [<Intersection>, <Intersection>, ...] - All intersections in the problem
        self.origin = next(s for s in self.sites if s.scats_num == origin)    # <Site> - first site of the search
        self.destination = next(s for s in self.sites if s.scats_num == destination)        # <Site> - the final site of the search
        self.links = links      # [<Link>, <Link>, ...]
        self.time = time        # the current time
                          
    # Returns a set of states the agent can traverse to from site 's'. 
    def get_actions(self, s):
        actions = []
        for l in self.links:
            if l.origin.scats_num == s:
                actions.append(self.get_site_by_intersection(l.destination))
        return actions

    # Returns a bool: is site 's' the destination?
    def goal_test(self, s):
        return s == self.destination

    # returns the travel time of traversing from site A to site B
    def travel_time(a, b):
        """
        Formula:
        time = (distance / speed) + time_delay
        
        Information from the brief:
        (i)     The speed limit on every link will be the same and set at 60km/h.
        (ii)    The travel time from a SCATS site A to a SCATS site B can be approximated by a simple expression
                    based on the accumulated volume per hour at the SCATS site B and the distance between A and B
                    (provided in the Traffic Flow to Travel Time Conversion v1.0.PDF file).
        (iii)   There is an average delay of 30 seconds to pass each controlled intersection.

        Information about the Site object:
        The argument a.flow_records represents a list of all daily collected traffic data from site 'a', with an interval of 15 minutes.
        For example:

        s.flow_records[1] = <FlowRecord> ->
        10/10/2006
        Time    0:00    0:15    0:30    0:45    1:00    1:15    ...
        Cars    86      83      52      58      59      44      ...

        s.flow_records[1].date = datetime.datetime(2006, 10, 10)
        s.flow_records[1].data = [{time: 0:00, flow: 25}, {time: 0:15, flow: 36}, ...]
        """

        # TODO: implement travel time calculation

        return 120 # travel time (seconds?)

    # Computes the Euclidian distance of the closest intersections between site 's' and the destination
    def distance_heuristic(self, s):
        if self.goal_test(s):
            return 0

        min_dist = float('inf')
        for site_i in s.intersections: # Intersections of site 's'
            for dest_i in self.destination.intersections: # Intersections of the destination site
                d_lat = site_i.coordinates[0] - dest_i.coordinates[0]
                d_long = site_i.coordinates[1] - dest_i.coordinates[1]
                dist = (d_lat**2 + d_long**2)**0.5  # Euclidean distance
                print("=", dist)
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
