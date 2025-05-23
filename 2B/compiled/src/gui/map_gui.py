import pandas as pd
import numpy as np
import folium
import json
import webbrowser
import os

class MapGUI:
    def __init__(self, sites, origin, destination, final_path):
        self.sites = sites # All site objects to display on the map
        self.pins = {} # {Site: (lat, long), ...} - A list of location pins representing the average location of each Site's intersections
        self.origin = origin
        self.destination = destination
        self.final_path = []
        self.html_file_path = os.getcwd()+"/src/source_data/boroondara_interactive_map.html"

        for site in sites:
            intersection_coords = [i.coordinates for i in site.intersections]
            self.pins[site.scats_num] = tuple(map(float, np.mean(intersection_coords, axis=0)))

        for i in final_path:
            self.final_path.append(self.pins[i.scats_num])

    def generate(self):
        # Create map centered on Boroondara
        m = folium.Map(location=[-37.83, 145.05], zoom_start=13, tiles="cartodbpositron")

        # Add Boroondara boundary
        with open("src/source_data/boroondara_boundary.geojson", "r") as f:
            boro_boundary = json.load(f)

        folium.GeoJson(
            boro_boundary,
            name="Boroondara Boundary",
            style_function=lambda x: {
                'fillColor': '#0000ff20',
                'color': 'gray',
                'weight': 2,
                'fillOpacity': 0.1
            }
        ).add_to(m)

        if self.final_path:
            folium.PolyLine(locations=self.final_path, color='red', weight=3, opacity=1).add_to(m)

        # Add JS function to store origin/destination
        js = """
        <script>
        var origin = null;
        var destination = null;

        function setPoint(siteId, lat, lon) {
            if (!origin) {
                origin = {id: siteId, lat: lat, lon: lon};
                alert("Origin set: " + siteId);
            } else if (!destination) {
                destination = {id: siteId, lat: lat, lon: lon};
                alert("Destination set: " + siteId + "\\n(Routing ready when integrated)");
            } else {
                origin = {id: siteId, lat: lat, lon: lon};
                destination = null;
                alert("Origin reset: " + siteId);
            }
        }
        </script>
        """

        m.get_root().html.add_child(folium.Element(js))

        # Add markers with selection links
        for scats_num in self.pins:
            lat, long = self.pins[scats_num]
            popup = folium.Popup(f"""
                <b>SCATS ID: {scats_num}</b><br>
                <a href='#' onclick="setPoint('{scats_num}', {lat}, {long})">Select as O/D</a>
            """, max_width=250)
            folium.Marker(
                location=[lat, long],
                popup=popup,
                tooltip="Click to select"
            ).add_to(m)

        # Save map
        m.save(self.html_file_path)

    def open(self):
        webbrowser.open(self.html_file_path)
