class Site:
    # def __init__(self, scats_num, coordinates, roads, flow_records):
    def __init__(self, scats_num, intersections):
        """
        A data structure representing a single SCATS site.
        Ported from the "Node" class in 2A - only attribute names have been edited.

        A site is created during the search process.
        """
        self.scats_num = scats_num              # String - the SCATS num of the site
        self.intersections = intersections

    def __repr__(self):
        return f"{self.scats_num}"

    def __hash__(self):
        return hash(self.scats_num)

    def __eq__(self, other):
        if isinstance(other, Site):
            if self.scats_num == other.scats_num:
                return True
        return False
