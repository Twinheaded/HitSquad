import regex as re
import pandas as pd
from datetime import datetime, timedelta

from .intersection import Intersection
from .site import Site
from .link import Link
from .traffic_problem import TrafficProblem


class FileParser:
    DATA_DIR_PATH = "src/data/"
    def __init__(self, file_name):
        self.file_name = file_name
        self.origin = None        # <Site> - the first site of the search
        self.dest = None          # <Site> - the final site of the search
        self.sites = []           # [<Site>, <Site>, ...]
        self.intersections = []   # [<Intersection>, <Intersection>, ...]
        self.links = []           # [<Link>, <Link>, ...]

    def create_problem(self, origin_scats_num, dest_scats_num):
        origin_site = next((s for s in self.sites if s.scats_num == origin_scats_num), None)
        dest_site = next((s for s in self.sites if s.scats_num == dest_scats_num), None)

        if origin_site is None or dest_site is None:
            raise ValueError(f"Could not find origin or destination site: {origin_scats_num}, {dest_scats_num}")

        return TrafficProblem(self.sites, self.intersections, origin_site, dest_site, self.links)

        
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
            flow_records = {}
            for index, site in sites_data.loc[sites_data['Location'] == intersection].iterrows():
                scats_num = site["SCATS Number"]
                lat, long = site.NB_LATITUDE, site.NB_LONGITUDE
                date = datetime.strptime(site.Date, '%d/%m/%Y')
                time_delay_list = site[[
                    "V00","V01","V02","V03","V04","V05","V06","V07","V08","V09","V10","V11","V12","V13","V14","V15","V16","V17","V18","V19","V20","V21","V22","V23","V24","V25","V26","V27","V28","V29","V30","V31","V32","V33","V34","V35","V36","V37","V38","V39","V40","V41","V42","V43","V44","V45","V46","V47","V48","V49","V50","V51","V52","V53","V54","V55","V56","V57","V58","V59","V60","V61","V62","V63","V64","V65","V66","V67","V68","V69","V70","V71","V72","V73","V74","V75","V76","V77","V78","V79","V80","V81","V82","V83","V84","V85","V86","V87","V88","V89","V90","V91","V92","V93","V94","V95"
                    ]].values.tolist()
                for i in range(len(time_delay_list)):
                    flow_records[date + timedelta(minutes=i*15)] = time_delay_list[i]
            self.intersections.append(Intersection(scats_num, intersection, (float(lat), float(long)), roads, flow_records))
        
        # Add Intersections to the .intersection attribute of Site objects
        for num in unique_scats_nums:
            intersections_in_site = []
            for index, site in sites_data.loc[sites_data['SCATS Number'] == num].iterrows():
                for intersection in self.intersections:
                    if site.Location == intersection.location and not intersection in intersections_in_site:
                        intersections_in_site.append(intersection)
            self.sites.append(Site(num, intersections_in_site))

        # Create links between Intersections
        for a in self.intersections:
            for b in self.intersections:
                if b.scats_num != a.scats_num and (a.roads[0] in b.roads or a.roads[1] in b.roads):
                    self.links.append(Link(a,b))
        
                # === NEW: BUILD GRAPH ===
        self.graph = {}
        for link in self.links:
            from_site = link.origin.scats_num
            to_site = link.destination.scats_num
            weight = link.origin.get_distance(link.destination)  # Ensure this is numeric

            if from_site not in self.graph:
                self.graph[from_site] = {}
            self.graph[from_site][to_site] = weight
                    
    # Phil's code for getting flow and location dicts (Still need to be tested and reworked)
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


