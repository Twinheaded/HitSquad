from .traffic_utils import flow_to_speed, haversine_distance
import datetime

class TravelTimeEstimator:
    def __init__(self, flow_data, location_data):
        """
        flow_data: dict {scats_id: [<FlowRecord>]}
        location_data: dict {scats_id: (lat, lon)}
        """
        self.flow_data = flow_data
        self.location_data = location_data

    def get_flow_at_time(self, scats_id, query_time):
        """
        Given a SCATS ID and a datetime.time object,
        return the flow closest to the provided time.
        """
        flow_records = self.flow_data.get(scats_id, [])
        query_hour_minute = (query_time.hour, query_time.minute)

        for record in flow_records:
            for entry in record["data"]:
                entry_time = entry["time"]
                if (entry_time.hour, entry_time.minute) == query_hour_minute:
                    return entry["flow"]
        return 0  # default if no match found

    def travel_time(self, a, b, time=datetime.time(0, 0)):
        """
        Computes travel time (in seconds) from site a to site b.
        `a` and `b` are Site objects with .scats_num and .coordinates
        """
        scats_a = a.scats_num
        scats_b = b.scats_num

        lat1, lon1 = self.location_data[scats_a]
        lat2, lon2 = self.location_data[scats_b]
        distance = haversine_distance(lat1, lon1, lat2, lon2)  # in km

        flow = self.get_flow_at_time(scats_b, time)
        speed = flow_to_speed(flow)  # in km/h

        travel_seconds = (distance / speed) * 3600 + 30  # add delay
        return travel_seconds
