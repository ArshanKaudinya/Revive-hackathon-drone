import tkinter as tk
from tkinter import simpledialog, messagebox
import folium
import webbrowser

class ManualCoordinatesInterface:
    def __init__(self, root, parent_app):
        self.root = root
        self.root.title("Manual Coordinates Input")
        self.root.geometry("400x200")  # Set window size
        self.parent_app = parent_app  # To pass coordinates back to the main interface

        # Add buttons for manual coordinate input
        self.create_widgets()

    def create_widgets(self):
        # Button to input coordinates manually
        self.enter_coords_button = tk.Button(self.root, text="Enter Coordinates", command=self.get_coordinates)
        self.enter_coords_button.pack(pady=10)

        # Button to display tracking map
        self.track_map_button = tk.Button(self.root, text="Show Tracking Map", command=self.show_tracking_map)
        self.track_map_button.pack(pady=10)

        # Button to exit
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
        self.exit_button.pack(pady=10)

    def get_coordinates(self):
        lat = simpledialog.askfloat("Input", "Enter Latitude:", parent=self.root)
        lng = simpledialog.askfloat("Input", "Enter Longitude:", parent=self.root)

        if lat is not None and lng is not None:
            self.parent_app.coordinates = [lat, lng]  # Store the coordinates in the parent app
            messagebox.showinfo("Coordinates Registered", f"Coordinates: {self.parent_app.coordinates}")
        else:
            messagebox.showwarning("Input Error", "Please enter valid coordinates.")

    def show_tracking_map(self):
        try:
            if hasattr(self.parent_app, 'coordinates'):
                self.create_tracking_map(self.parent_app.coordinates)
                webbrowser.open('manual_tracking_map.html')
            else:
                messagebox.showwarning("No Coordinates", "Please enter coordinates first.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load map: {e}")

    def create_tracking_map(self, coordinates):
        # Create a folium map centered on the entered coordinates
        tracking_map = folium.Map(location=coordinates, zoom_start=14)
        folium.Marker(location=coordinates, popup="Manual Location").add_to(tracking_map)

        # Save the map as an HTML file
        tracking_map.save("manual_tracking_map.html")

# Main loop to run the manual coordinates interface separately if needed
if __name__ == "__main__":
    root = tk.Tk()
    app = ManualCoordinatesInterface(root, None)
    root.mainloop()






