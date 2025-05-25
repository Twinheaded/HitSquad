import regex as re
import pandas as pd
from datetime import datetime, timedelta

from src.traffic_utils import haversine_distance

from .traffic_problem import TrafficProblem
from .data_structures import Site, Intersection, Link

class FileParser:
    DATA_DIR_PATH = "src/source_data/"
    ML_PREDICTIONS_DIR_PATH = DATA_DIR_PATH + "ml_flow_predictions/"
    OFFSET_LAT = 0.001497
    OFFSET_LONG = 0.0013395

    def __init__(self, file_name):
        self.file_name = file_name
        self.origin = None        # <Site> - the first site of the search
        self.dest = None          # <Site> - the final site of the search
        self.sites = []           # [<Site>, <Site>, ...]
        self.intersections = []   # [<Intersection>, <Intersection>, ...]
        self.links = []           # [<Link>, <Link>, ...]

    def create_problem(self, origin, dest, date_time=datetime(2006, 10, 1, 0, 0)):
        scats_nums = [s.scats_num for s in self.sites]
        if not (origin in scats_nums and dest in scats_nums):
            raise ValueError(f"Could not find origin or destination site: {origin}, {dest}")
        if not datetime(2006, 10, 1, 0, 0) <= date_time < datetime(2006, 12, 1, 0, 0):
            raise ValueError(f"Invalid date/time {date_time}. Must be within October or November of 2006.")
        return TrafficProblem(self.sites, self.intersections, origin, dest, self.links, date_time)
        
    def parse(self):
        # CREATE SITE OBJECTS
        sites_data = pd.read_csv(
                self.DATA_DIR_PATH + self.file_name,
                dtype=str,
                usecols=[
                    "SCATS Number",
                    "Location",
                    "NB_LATITUDE",
                    "NB_LONGITUDE",
                    "Date",
                    "V00","V01","V02","V03","V04","V05","V06","V07","V08","V09","V10","V11","V12","V13","V14","V15","V16","V17","V18","V19","V20","V21","V22","V23","V24","V25","V26","V27","V28","V29","V30","V31","V32","V33","V34","V35","V36","V37","V38","V39","V40","V41","V42","V43","V44","V45","V46","V47","V48","V49","V50","V51","V52","V53","V54","V55","V56","V57","V58","V59","V60","V61","V62","V63","V64","V65","V66","V67","V68","V69","V70","V71","V72","V73","V74","V75","V76","V77","V78","V79","V80","V81","V82","V83","V84","V85","V86","V87","V88","V89","V90","V91","V92","V93","V94","V95"
                    ])

        # Gather all unique SCATS numbers and roads
        unique_scats_nums = []
        unique_intersections = []
        unique_roads = []
        for index, site in sites_data.iterrows():
            if not site["SCATS Number"] in unique_scats_nums:
                unique_scats_nums.append(site["SCATS Number"])

            if not site["Location"] in unique_intersections:
                unique_intersections.append(site["Location"])

            # Extract ['WARRIGAL_RD', 'TOORAK_RD'] from 'WARRIGAL_RD N of TOORAK_RD'
            for road in re.split(r" [NSEW]{1,2} of ", site.Location, flags=re.IGNORECASE):
                if not road in unique_roads:
                    unique_roads.append(road)

        # Create Intersection objects for each intersection
        for intersection in unique_intersections:
            scats_num = ""
            lat, long = 0, 0
            roads = re.split(r" [NSEW]{1,2} of ", intersection, flags=re.IGNORECASE)
            # Existing flow (number of cars per 15 mins) data for October
            flow_records = {}
            for index, site in sites_data.loc[sites_data['Location'] == intersection].iterrows():
                scats_num = site["SCATS Number"]
                lat, long = site.NB_LATITUDE, site.NB_LONGITUDE
                date = datetime.strptime(site.Date, '%d/%m/%Y')
                flow_list = site[[
                    "V00","V01","V02","V03","V04","V05","V06","V07","V08","V09","V10","V11","V12","V13","V14","V15","V16","V17","V18","V19","V20","V21","V22","V23","V24","V25","V26","V27","V28","V29","V30","V31","V32","V33","V34","V35","V36","V37","V38","V39","V40","V41","V42","V43","V44","V45","V46","V47","V48","V49","V50","V51","V52","V53","V54","V55","V56","V57","V58","V59","V60","V61","V62","V63","V64","V65","V66","V67","V68","V69","V70","V71","V72","V73","V74","V75","V76","V77","V78","V79","V80","V81","V82","V83","V84","V85","V86","V87","V88","V89","V90","V91","V92","V93","V94","V95"
                    ]].values.tolist()
                for i in range(len(flow_list)):
                    flow_records[date + timedelta(minutes=i*15)] = flow_list[i]
            self.intersections.append(Intersection(scats_num, intersection, (float(lat)+self.OFFSET_LAT, float(long)+self.OFFSET_LONG), roads, flow_records))
        
        # Add Intersections to the .intersection attribute of Site objects
        for num in unique_scats_nums:
            intersections_in_site = []
            for index, site in sites_data.loc[sites_data['SCATS Number'] == num].iterrows():
                for intersection in self.intersections:
                    if site.Location == intersection.location and not intersection in intersections_in_site:
                        intersections_in_site.append(intersection)
            self.sites.append(Site(num, intersections_in_site))

        # Create links between Intersections
        MAXIMUM_LINK_DISTANCE = 4 # in km
        for a in self.intersections:
            for b in self.intersections:
                if all([
                    b.scats_num != a.scats_num,
                    a.roads[0] in b.roads or a.roads[1] in b.roads,
                    haversine_distance(a.coordinates[0], a.coordinates[1], b.coordinates[0], b.coordinates[1]) < MAXIMUM_LINK_DISTANCE
                    ]):
                    self.links.append(Link(a,b))

        # November flow records predicted by LSTM, GRU, and RNN machine learning models
        print("Loading lSTM/GRU/RNN predicted flow data...", end="")
        for intersection in self.intersections:
            scats_num = intersection.scats_num
            # Retrieve LSTM/GRU/RNN flow data for the current site
            # File path example: 'src/source_data/ml_flow_predictions/0970/lstm_0970.csv'
            lstm_data = pd.read_csv(
                self.ML_PREDICTIONS_DIR_PATH + scats_num + "/lstm_" + scats_num + ".csv",
                dtype=float,
                ).values.tolist()
            gru_data = pd.read_csv(
                self.ML_PREDICTIONS_DIR_PATH + scats_num + "/gru_" + scats_num + ".csv",
                dtype=float,
                ).values.tolist()
            rnn_data = pd.read_csv(
                self.ML_PREDICTIONS_DIR_PATH + scats_num + "/rnn_" + scats_num + ".csv",
                dtype=float,
                ).values.tolist()

            VALUE_COUNT = 2880 # Number of 15 minute intervals from 2006/11/1 0:00 to 2006/11/30 23:45
            for i in range(VALUE_COUNT):
                date_time = datetime(2006,11,1) + timedelta(minutes=i*15)
                intersection.lstm_data[date_time] = lstm_data[i][0]
                intersection.gru_data[date_time] = gru_data[i][0]
                intersection.rnn_data[date_time] = rnn_data[i][0]
        print(" done")

                    
    # TODO Phil's code for getting flow and location dicts (Still need to be tested and reworked)
    def get_flow_dict(self):
        """
        Returns {scats_id: [FlowRecord-like dict]}.
        Useful for use in TravelTimeEstimator.
        """
        flow_dict = {}
        for intersection in self.intersections:
            scats_id = intersection.scats_num
            if scats_id not in flow_dict:
                flow_dict[scats_id] = []

            # Wrap it in an object-like dict with `data` and `date`
            flow_data_list = []
            for dt, flow in intersection.flow_records.items():
                flow_data_list.append({"time": dt.time(), "flow": int(flow)})
            flow_dict[scats_id].append({
                "date": dt.date(),
                "data": flow_data_list
            })

        return flow_dict

    def get_location_dict(self):
        """
        Returns {scats_id: (lat, lon)}.
        """
        location_dict = {}
        for intersection in self.intersections:
            scats_id = intersection.scats_num
            location_dict[scats_id] = (
                float(intersection.coordinates[0]),
                float(intersection.coordinates[1])
            )
        return location_dict
