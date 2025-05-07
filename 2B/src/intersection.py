# TODO: Replace comments

class Intersection:
    def __init__(self, scats_num, location, coordinates, roads, flow_records):
        """
        A data structure representing a single SCATS site.
        Ported from the "Node" class in 2A - only attribute names have been edited.

        A site is created during the search process.
        """
        self.scats_num = scats_num
        self.location = location
        self.coordinates = coordinates      # (lat,long) - the latitude and longitude values of the site
        self.roads = roads # ["DENMARK_ST", "BARKERS_RD", ...] - Streets on the intersection of this site
        self.flow_records = flow_records  # {datetime: int, datetime: int, ...} - a set of flow data, compiled from all days/times at this site

    def __repr__(self):
        return f"<Intersection> {self.location}"
