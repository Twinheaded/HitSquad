class Site:
    def __init__(self, node_id, coordinates):
        """
        A data structure representing a single SCATS site.
        Ported from the "Node" class in 2A - only attribute names have been edited.

        A site is created during the search process.
        """
        self.site_id = site_id              # String - the SCATS id of the site
        self.coordinates = coordinates      # (lat,long) - the latitude and longitude values of the site

    def __repr__(self):
        return f"{self.node_id}"
