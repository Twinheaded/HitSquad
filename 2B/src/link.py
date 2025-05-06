class Link():

    def __init__(self, origin, destination, travel_time):
        self.origin = origin
        self.destination = destination
        self.travel_time = travel_time

    def __repr__(self):
        return f"<Link> origin: {self.origin}, dest: {self.destination}, travel_time: {self.travel_time}"
