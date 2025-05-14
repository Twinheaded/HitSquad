import tkinter as tk
from tkinter import ttk, messagebox

# Dummy route generator (will be replaced by actual model integration)
def generate_route(origin, destination):
    # Placeholder: simulate 2 dummy routes
    return [
        {'path': [origin, '2041', destination], 'time': 12.3},
        {'path': [origin, '2824', destination], 'time': 13.0}
    ]

class TrafficRouteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic-Based Route Guidance System")
        self.root.geometry("600x400")

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

        # Load SCATS IDs (static for now, ideally load from file)
        scats_ids = ['2000', '2041', '2824', '3002']
        self.origin_menu['values'] = scats_ids
        self.destination_menu['values'] = scats_ids

        # Button to calculate
        ttk.Button(root, text="Generate Routes", command=self.display_routes).pack(pady=10)

        # Result box
        self.result_text = tk.Text(root, height=10, width=70)
        self.result_text.pack(pady=10)

    def display_routes(self):
        origin = self.origin_var.get()
        destination = self.destination_var.get()

        if not origin or not destination:
            messagebox.showwarning("Input Error", "Please select both Origin and Destination.")
            return

        routes = generate_route(origin, destination)
        self.result_text.delete(1.0, tk.END)

        for i, route in enumerate(routes):
            route_str = f"Route {i+1}: {' → '.join(route['path'])} | Estimated Time: {route['time']} mins\n"
            self.result_text.insert(tk.END, route_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficRouteGUI(root)
    root.mainloop()
