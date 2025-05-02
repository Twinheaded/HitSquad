class Node:
    def __init__(self, node_id, coordinates):
        """A node is created during the search process.
        Its 'state' represents its coordinates.
        Multiple nodes of the same coordinates can exist, because a state can be approached from different paths.
        """
        self.node_id = node_id              # Integer - the ID of the state (e.g. the 1 in '1: (3,4)')
        self.coordinates = coordinates      # (x,y)

    def __repr__(self):
        return f"{self.node_id}"
