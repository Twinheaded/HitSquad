from src.data_structures import Site, Link
from src.traffic_utils import flow_to_speed, haversine_distance
import numpy as np
import datetime

class TrafficProblem():
    """
    The Traffic-Based Route Guidance Problem.

    Contains all sites, intersections, and connecting links.
    An origin and destination site are set upon initialisation.
    """
    def __init__(self, sites, intersections, origin, destination, links, time=datetime.datetime(2006, 10, 1, 0, 15), estimator=None):
        self.sites = sites # [<Site>, <Site>, ...] - All sites in the problem
        self.intersections = intersections # [<Intersection>, <Intersection>, ...] - All intersections in the problem
        self.origin = next(s for s in self.sites if s.scats_num == origin)    # <Site> - first site of the search
        self.destination = next(s for s in self.sites if s.scats_num == destination)        # <Site> - the final site of the search
        self.links = links # [<Link>, <Link>, ...]
        self.time = time # the current time
        self.estimator = estimator  # TravelTimeEstimator instance
  
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

    def get_actions(self, s):
        actions = []
        for l in self.links:
            if l.origin.scats_num == s.scats_num:
                actions.append(self.get_site_by_intersection(l.destination))
        return actions

    # Returns a bool: is site 's' the destination?
    def goal_test(self, s):
        return s == self.destination

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

    def distance_between_sites(self, a, b):
        """
        Computes the Haversine (great-circle) distance, in km, of the closest intersections between site 'a' and site 'b'
        """
        min_dist = float('inf')
        for site_i in a.intersections: # Intersections of site 'a'
            for dest_i in b.intersections: # Intersections of the destination site
                dist = haversine_distance(site_i.coordinates[0], site_i.coordinates[1], dest_i.coordinates[0], dest_i.coordinates[1])
                if dist < min_dist:
                    min_dist = dist
        return min_dist
    
    def get_flow_now(self, s):
        return self.get_flow_at_time(s, self.time)

    def get_flow_at_time(self, s, date_hour):
        """
        Given site 's' and a datetime.time object,
        return the flow closest to the provided time.
        """

        print("date_hour:", date_hour)
        summed_flow = 0.0
        records_counted = 0
        for intersection in s.intersections:
            for datetime_in_hour in [record for record in intersection.flow_records.keys() if record.date() == date_hour.date() and record.hour == date_hour.hour]:
                flow = intersection.flow_records[datetime_in_hour]
                summed_flow += float(flow)
                records_counted += 1
        avg_flow = summed_flow / records_counted
        return avg_flow

    def travel_time(self, a, b):
        """
        Calculate travel time from Site a to Site b using the estimator.
        """

        dist = self.distance_between_sites(a,b) # Distance (km) between site 'a' and site 'b'
        
        flow = self.get_flow_at_time(scats_b, time)
        speed = flow_to_speed(flow)  # in km/h

        travel_seconds = (distance / speed) * 3600 + 30  # add delay
        return travel_seconds

        # if self.estimator is None:
        #     raise Exception("No estimator assigned to TrafficProblem.")
        # return self.estimator.travel_time(a, b, self.time)

