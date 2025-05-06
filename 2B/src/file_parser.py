import regex as re
import pandas as pd

from .site import Site
from .traffic_problem import TrafficProblem

class FileParser:
    DATA_DIR_PATH = "src/data/"
    def __init__(self, file_name):
        self.file_name = file_name
        self.origin = None        # <Site> - the first site of the search
        self.dest = []          # <Dest> - the final site of the search
        self.nodes_by_id = {}
        self.links = {}         # {<Site>:{<Site>:travel_time, <Site>:travel_time, ...}, ...}

    # def create_problem(self):
        # return TrafficProblem([n for n in self.nodes_by_id.values()], self.init, self.goal, self.edges)
        
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

        sites = []
        all_roads = []
        roads_in_site = []
        current_site = sites_data.loc[0]
        prev_site = sites_data.loc[0]

        for index, site in sites_data.iterrows():
            scats_num = site["SCATS Number"]
            final_site = site
            if scats_num != prev_site["SCATS Number"] and not scats_num in [s.scats_num for s in sites]:
                sites.append(Site(prev_site["SCATS Number"], (prev_site.NB_LATITUDE, prev_site.NB_LONGITUDE), roads_in_site))
                roads_in_site = []
                prev_site = site
            else:
                roads = re.split(r" [NSEW]{1,2} of ", site.Location, flags=re.IGNORECASE)
                for r in roads:
                    if not r in roads_in_site:
                        roads_in_site.append(r)
                    if not r in all_roads:
                        all_roads.append(r)

        sites.append(Site(final_site["SCATS Number"], (final_site.NB_LATITUDE, final_site.NB_LONGITUDE), roads_in_site))
        # for s in sites:
        #     print(s, s.coordinates, s.roads)
        
        # LINK SITES BY ROADS
        for road in all_roads:
            sites_with_road = list(filter(lambda x: road in x.roads, sites))
            print(road)
            for s in sites_with_road:
                print(s, s.coordinates, s.roads)
            print()
            # for site in sites:
            #     if road in site.roads:




        # for item in data.keys:
        #     print(item[0])
        # format_error = "\nInput file is not written in the correct format.\n"
        # self.nodes_by_id = {}
        # f = open(self.TEST_DIR_PATH + filename, "r")
        # assert f.readline().strip() == 'Nodes:', wrong_format_error
        # node_str = f.readline().strip()        # Line under the 'Nodes:' heading
        # while node_str != "Edges:":
        #     assert re.match(r'^\d+: \(\d+,\d+\)$', node_str), wrong_format_error # RegEx for '#: (#,#)'
        #     node_id, x, y = [int(x) for x in re.split(r'\D+', node_str[:-1])]
        #     self.nodes_by_id[node_id] = Node(node_id,(x,y))
        #     node_str = f.readline().strip()
        # edge_str = f.readline().strip()        # Line under the 'Edges:' heading
        # while edge_str:                        # Continue until an empty line
        #     # state      - the 'from' address (Int)
        #     # transition - the 'to' address (Node)
        #     # cost       - the expense of traversing (Int)
        #     assert re.match(r'^\(\d+,\d+\): \d+$', edge_str)  # RegEx for the text format, '(#,#): #'
        #     s, t, c = [int(x) for x in re.split(r'\D+', edge_str[1:])]
        #     s = self.nodes_by_id[s]
        #     t = self.nodes_by_id[t]
        #     # Connect s -> t by an edge with a cost of c
        #     if s in self.edges:
        #         self.edges[s].update({t:c})
        #     else:
        #         self.edges[s] = {t:c}
        #     edge_str = f.readline().strip()
        # assert f.readline().strip() == 'Origin:', wrong_format_error
        # self.init = self.nodes_by_id[int(f.readline())]    # initial - the first node of the problem (Node)
        # assert f.readline().strip() == 'Destinations:', wrong_format_error
        # dest_str = f.readline().strip()         # Line under the 'Destinations:' heading
        # assert re.match(r'^\d+(; \d+)*$', dest_str), wrong_format_error # RegEx for '#' or '#; #; ... #'
        # self.goal = [self.nodes_by_id[int(i)] for i in dest_str.split(";")] # [<Node>,<Node>,...]
