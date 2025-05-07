import datetime

class FlowRecord:
    """
    A data structure representing a single day of flow data,
        (number of cars passed through the site) in 15 minute
        intervals from 0:00 - 23:45.
    """

    def __init__(self, date, data):
        self.date = date
        self.data = data    # [{time: 0:00, flow: 25}, {time: 0:15, flow: 36}, ...]

    def get_closest_time(self, time):
        return min(self.data, key=lambda x: abs(x - time))


    def __repr__(self):
        return f"<FlowRecord> Date: {self.date}"
