import pandas as pd

# Load the full traffic file
df = pd.read_csv("2B/gui/Oct_2006_Boorondara_Traffic_Flow_Data.csv")

# Extract unique site coordinates
nodes = df.groupby("SCATS Number")[["NB_LATITUDE", "NB_LONGITUDE"]].mean().reset_index()
nodes.columns = ['site_id', 'latitude', 'longitude']

# Save to new CSV
nodes.to_csv("2B/gui/boroondara_nodes.csv", index=False)
