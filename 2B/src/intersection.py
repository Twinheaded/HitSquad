# TODO: Replace comments

class Intersection:
    def __init__(self, scats_num, location, coordinates, roads, flow_records):
        """
        A data structure representing a single intersection within a SCATS site.
        """
        self.scats_num = scats_num
        self.location = location
        self.coordinates = coordinates      # (lat,long) - the latitude and longitude values of the intersection
        self.roads = roads # ["DENMARK_ST", "BARKERS_RD", ...] - roads on the intersection
        self.flow_records = flow_records  # {datetime: int, datetime: int, ...} - a set of flow data, compiled from all days/times at this intersection

    def __repr__(self):
        return f"{self.scats_num} {self.location} {self.coordinates}"
