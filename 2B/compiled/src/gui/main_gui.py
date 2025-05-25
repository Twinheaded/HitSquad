from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from src import FileParser, TrafficProblem, ALGORITHMS
from .map_gui import MapGUI

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic-Based Route Guidance System")
        self.root.geometry("600x600")
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
        self.origin_menu['values'] = [s.scats_num for s in self.fp.sites]
        self.origin_menu.current(0)

        ttk.Label(frame, text="Destination SCATS ID:").grid(row=1, column=0, padx=5, pady=5)
        self.destination_var = tk.StringVar()
        self.destination_menu = ttk.Combobox(frame, textvariable=self.destination_var)
        self.destination_menu.grid(row=1, column=1)
        self.destination_menu['values'] = [s.scats_num for s in self.fp.sites]
        self.destination_menu.current(0)

        ttk.Label(frame, text="ML Model:").grid(row=2, column=0, padx=5, pady=5)
        self.method_var = tk.StringVar()
        self.method_menu = ttk.Combobox(frame, textvariable=self.method_var)
        self.method_menu.grid(row=2, column=1)
        self.method_menu['values'] = ['LSTM', 'GRU', 'RNN']
        self.method_menu.current(0)

        ttk.Label(frame, text="Date in November:").grid(row=3, column=0, padx=5, pady=5)
        self.date_var = tk.StringVar()
        self.date_menu = ttk.Combobox(frame, textvariable=self.date_var)
        self.date_menu.grid(row=3, column=1)
        self.date_menu['values'] = [str(n) for n in range(1,31)]
        self.date_menu.current(0)

        ttk.Label(frame, text="Hour (24hr time):").grid(row=4, column=0, padx=5, pady=5)
        self.hour_var = tk.StringVar()
        self.hour_menu = ttk.Combobox(frame, textvariable=self.hour_var)
        self.hour_menu.grid(row=4, column=1)
        self.hour_menu['values'] = [str(n) for n in range(0, 24)]
        self.hour_menu.current(0)

        # Button to calculate
        ttk.Button(root, text="Generate Routes", command=self.display_routes).pack(pady=10)

        # Result box
        self.result_text = tk.Text(root, height=20, width=70)
        self.result_text.pack(pady=10)

    def display_routes(self):
        origin = self.origin_var.get()
        destination = self.destination_var.get()
        ml_model = self.method_var.get()
        date = int(self.date_var.get())
        hour = int(self.hour_var.get())

        if not (origin and destination and ml_model):
            # messagebox.showwarning("Input Error", "Please select Origin, Destination, and Search Method.")
            messagebox.showwarning("Input Error", "Please select Origin, Destination, and ML Algorithm.")
            return

        # Create a problem object with the specified origin and destination SCATS sites
        problem = self.fp.create_problem(origin, destination, datetime(2006, 11, date, hour, 0)) # Arguments: origin, destination

        search_objects = []
        for a in ALGORITHMS.values():
            search_obj = a(problem, ml_model)
            search_obj.search()
            search_objects.append(search_obj)

        self.result_text.delete(1.0, tk.END)

        paths = []
        for search_obj in search_objects:
            if not search_obj.final_path == []:
                result = f"{search_obj.name} ({search_obj.travel_time:.2f} seconds)\n" + ' → '.join(map(lambda x: x.scats_num, search_obj.final_path)) + '\n\n'
                paths.append(search_obj.final_path)
            else:
                result = f"{search_obj.name}\nNo path found.\n\n"
            self.result_text.insert(tk.END, result)

        mp = MapGUI(problem.sites, origin, destination, paths)
        mp.generate()
        mp.open()
