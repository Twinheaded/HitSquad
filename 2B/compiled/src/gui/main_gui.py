import tkinter as tk
from tkinter import ttk, messagebox

from src import FileParser, TrafficProblem, ALGORITHMS
# from src.data_structures import Site, Link

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic-Based Route Guidance System")
        self.root.geometry("600x400")
        self.fp = FileParser("Oct_2006_Boorondara_Traffic_Flow_Data.csv")

        # Parse file into data structures
        self.fp.parse()

        # -------------
        # GUI Display
        # -------------

        # Title Label
        ttk.Label(root, text="Traffic Route Finder (Boroondara)", font=("Helvetica", 16)).pack(pady=10)

        # Frame for selection
        frame = ttk.Frame(root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Origin SCATS ID:").grid(row=0, column=0, padx=5, pady=5)
        self.origin_var = tk.StringVar()
        self.origin_menu = ttk.Combobox(frame, textvariable=self.origin_var)
        self.origin_menu.grid(row=0, column=1)

        ttk.Label(frame, text="Destination SCATS ID:").grid(row=1, column=0, padx=5, pady=5)
        self.destination_var = tk.StringVar()
        self.destination_menu = ttk.Combobox(frame, textvariable=self.destination_var)
        self.destination_menu.grid(row=1, column=1)

        ttk.Label(frame, text="Search Method:").grid(row=2, column=0, padx=5, pady=5)
        self.method_var = tk.StringVar()
        self.method_menu = ttk.Combobox(frame, textvariable=self.method_var)
        self.method_menu.grid(row=2, column=1)

        self.origin_menu['values'] = self.fp.sites
        self.destination_menu['values'] = self.fp.sites
        self.method_menu['values'] = [a for a in ALGORITHMS.keys()]

        # Button to calculate
        ttk.Button(root, text="Generate Routes", command=self.display_routes).pack(pady=10)

        # Result box
        self.result_text = tk.Text(root, height=10, width=70)
        self.result_text.pack(pady=10)

    def display_routes(self):
        origin = self.origin_var.get()
        destination = self.destination_var.get()
        search_method = self.method_var.get()

        if not (origin and destination):
            messagebox.showwarning("Input Error", "Please select both Origin and Destination.")
            return

        # Create a problem object with the specified origin and destination SCATS sites
        problem = self.fp.create_problem(origin, destination) # Arguments: origin, destination

        searchObj = ALGORITHMS[search_method](problem)
        searchObj.search()
        self.result_text.delete(1.0, tk.END)

        route_str = ' → '.join(map(lambda x: x.scats_num, searchObj.final_path)) 

        # TODO: Show multiple routes
        # for i, route in enumerate(routes):
            # route_str = f"Route {i+1}: \n"

        self.result_text.insert(tk.END, route_str)
