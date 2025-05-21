# This script is used to test the travel time estimation functionality, we can delete it after connecting it with the main.py (Phil's code)

from src.file_parser import FileParser
from src.travel_time.travel_time_estimator import TravelTimeEstimator
from datetime import time

# Load and parse the data
parser = FileParser("Oct_2006_Boorondara_Traffic_Flow_Data.csv")
parser.parse()

# Get data dictionaries
flow_dict = parser.get_flow_dict()
location_dict = parser.get_location_dict()

# Create the estimator
estimator = TravelTimeEstimator(flow_dict, location_dict)

# Pick two known intersections (by SCATS number)
site_a = None
site_b = None

# Use parser.sites to find corresponding Site objects
for site in parser.sites:
    if site.scats_num == "2000":
        site_a = site
    elif site.scats_num == "3002":
        site_b = site

# Set a known time
query_time = time(8, 0)  # 8:00 AM

# Call the estimator
if site_a and site_b:
    travel_time_sec = estimator.travel_time(site_a, site_b, query_time)
    print(f"Estimated travel time from {site_a.scats_num} to {site_b.scats_num} at {query_time}: {travel_time_sec:.2f} seconds")
else:
    print("One or both SCATS sites not found.")