import pandas as pd
import numpy as np
import folium
import json
from folium.plugins import MarkerCluster

class MapGUI:
    def __init__(self, sites, origin, destination, final_path):
        self.sites = sites
        self.pins = {} # {Site: (lat, long), ...} - A list of location pins representing the average location of each Site's intersections
        self.origin = origin
        self.destination = destination
        self.final_path = final_path

        for site in sites:
            intersection_coords = [i.coordinates for i in site.intersections]
            self.pins[site.scats_num] = tuple(map(float, np.mean(intersection_coords, axis=0)))

        print(self.pins)

        # self.pins =


# # Load your cleaned node list
# # nodes = pd.read_csv("2B/gui/boroondara_nodes.csv")
# nodes = pd.read_csv(SRC_PATH + "boroondara_nodes.csv")


# # Create map centered on Boroondara
# m = folium.Map(location=[-37.83, 145.05], zoom_start=13)

# # Add Boroondara boundary
# with open("src/source_data/boroondara_boundary.geojson", "r") as f:
#     boro_boundary = json.load(f)

# folium.GeoJson(
#     boro_boundary,
#     name="Boroondara Boundary",
#     style_function=lambda x: {
#         'fillColor': '#0000ff20',
#         'color': 'blue',
#         'weight': 2,
#         'fillOpacity': 0.1
#     }
# ).add_to(m)

# # Optional: cluster markers
# marker_cluster = MarkerCluster().add_to(m)

# # Add JS function to store origin/destination
# js = """
# <script>
# var origin = null;
# var destination = null;

# function setPoint(siteId, lat, lon) {
#     if (!origin) {
#         origin = {id: siteId, lat: lat, lon: lon};
#         alert("Origin set: " + siteId);
#     } else if (!destination) {
#         destination = {id: siteId, lat: lat, lon: lon};
#         alert("Destination set: " + siteId + "\\n(Routing ready when integrated)");
#     } else {
#         origin = {id: siteId, lat: lat, lon: lon};
#         destination = null;
#         alert("Origin reset: " + siteId);
#     }
# }
# </script>
# """
# m.get_root().html.add_child(folium.Element(js))

# # Add markers with selection links
# for _, row in nodes.iterrows():
#     popup = folium.Popup(f"""
#         <b>SCATS ID: {row['site_id']}</b><br>
#         <a href='#' onclick="setPoint('{row['site_id']}', {row['latitude']}, {row['longitude']})">Select as O/D</a>
#     """, max_width=250)
#     folium.Marker(
#         location=[row['latitude'], row['longitude']],
#         popup=popup,
#         tooltip="Click to select"
#     ).add_to(marker_cluster)

# # Save map
# m.save("./boroondara_interactive_map.html")
