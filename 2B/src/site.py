class Site:
    def __init__(self, scats_num, coordinates, roads):
        """
        A data structure representing a single SCATS site.
        Ported from the "Node" class in 2A - only attribute names have been edited.

        A site is created during the search process.
        """
        self.scats_num = scats_num              # String - the SCATS num of the site
        self.coordinates = coordinates      # (lat,long) - the latitude and longitude values of the site
        self.roads = roads # ["DENMARK_ST", "BARKERS_RD", ...] - Streets on the intersection of this site

    def __repr__(self):
        return f"{self.scats_num}"
