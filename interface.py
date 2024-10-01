import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import threading
import webbrowser
import os
from navigation import KalmanFilter, simulate_movement
from path import main as run_pathfinding
import requests
from sensors import IMU, ProximitySensors, Barometer, LIDAR, OpticalFlowSensor, Compass, ThermalImagingSensor, Camera
from on_drone.travel_delivery import TravelDelivery

kf = KalmanFilter(initial_position=0, initial_velocity=0, delta_time=0.1)

class DroneInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Drone Control System")
        self.root.geometry("1000x900")

        self.coordinates = None  # Store manual coordinates
        self.imu = IMU()  # Initialize IMU model
        self.proximity_sensors = ProximitySensors()  # Initialize Proximity Sensors
        self.barometer = Barometer()  # Initialize Barometer
        self.lidar = LIDAR()  # Initialize LIDAR
        self.optical_flow_sensor = OpticalFlowSensor()  # Initialize Optical Flow Sensor
        self.compass = Compass()  # Initialize Compass
        self.thermal_sensor = ThermalImagingSensor()  # Initialize Thermal Imaging Sensor
        self.camera = Camera()  # Initialize Camera
        
        threading.Thread(target=self.run_flask_server, daemon=True).start()

        self.travel_delivery = None  # TravelDelivery object
        self.simulation_running = False  # Keep track of whether the simulation is running

        # Add additional attributes for statistics and flight time
        self.flight_time_label = None
        self.stats_label = None
        self.create_widgets()

    def update_drone_position(self, acceleration):
        # Update drone's position based on sensor data using Kalman filter
        updated_position = simulate_movement(acceleration, kf)
        return updated_position

    def create_widgets(self):
        # Layout configuration
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Place buttons on top using grid
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=0, column=0, pady=10, padx=10, sticky="n")

        self.manual_coords_button = tk.Button(button_frame, text="Enter Target Coordinates", command=self.open_manual_coordinates)
        self.manual_coords_button.grid(row=0, column=0, padx=10)

        self.track_button = tk.Button(button_frame, text="Track Drone", command=self.track_drone)
        self.track_button.grid(row=0, column=1, padx=10)

        self.simulate_button = tk.Button(button_frame, text="Simulate Sensors", command=self.start_simulation)
        self.simulate_button.grid(row=0, column=2, padx=10)

        control_frame = tk.Frame(self.root)
        control_frame.grid(row=1, column=0, pady=10, padx=10, sticky="n")

        self.launch_button = tk.Button(control_frame, text="Launch", command=self.launch_drone)
        self.launch_button.grid(row=0, column=0, padx=10)

        self.delivery_button = tk.Button(control_frame, text="Confirm Delivery", command=self.confirm_delivery)
        self.delivery_button.grid(row=0, column=1, padx=10)

        # Frame to show flight statistics and time
        stats_frame = tk.Frame(self.root)
        stats_frame.grid(row=1, column=1, pady=10, padx=10)

        self.flight_time_label = tk.Label(stats_frame, text="Flight Time: 0 seconds")
        self.flight_time_label.grid(row=0, column=0, padx=10)

        self.stats_label = tk.Label(stats_frame, text="Drone Statistics:")
        self.stats_label.grid(row=1, column=0, padx=10)

        # Drone control button frame
        control_button_frame = tk.Frame(self.root)
        control_button_frame.grid(row=1, column=2, pady=10, padx=10, sticky="n")

        self.control_drone_button = tk.Button(control_button_frame, text="Open Drone Control", command=self.open_drone_control_window)
        self.control_drone_button.grid(row=0, column=0, padx=10)

        # Create a frame for sensor data and place it below the buttons
        sensor_frame = tk.Frame(self.root)
        sensor_frame.grid(row=2, column=0, columnspan=3, pady=20, padx=10, sticky="nsew")

        # IMU Data Section
        self.imu_label = tk.Label(sensor_frame, text="IMU Data", font=("Arial", 12))
        self.imu_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.imu_data_text = tk.Text(sensor_frame, height=4, width=40)
        self.imu_data_text.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Proximity Sensors Data Section
        self.proximity_label = tk.Label(sensor_frame, text="Proximity Sensors", font=("Arial", 12))
        self.proximity_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.proximity_data_text = tk.Text(sensor_frame, height=4, width=40)
        self.proximity_data_text.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Barometer Data Section
        self.barometer_label = tk.Label(sensor_frame, text="Barometer", font=("Arial", 12))
        self.barometer_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.barometer_data_text = tk.Text(sensor_frame, height=4, width=40)
        self.barometer_data_text.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # LIDAR Data Section
        self.lidar_label = tk.Label(sensor_frame, text="LIDAR", font=("Arial", 12))
        self.lidar_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.lidar_data_text = tk.Text(sensor_frame, height=4, width=40)
        self.lidar_data_text.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Optical Flow Sensor Data Section
        self.optical_flow_label = tk.Label(sensor_frame, text="Optical Flow Sensor", font=("Arial", 12))
        self.optical_flow_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.optical_flow_data_text = tk.Text(sensor_frame, height=4, width=40)
        self.optical_flow_data_text.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        # Compass Data Section
        self.compass_label = tk.Label(sensor_frame, text="Compass", font=("Arial", 12))
        self.compass_label.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.compass_data_text = tk.Text(sensor_frame, height=4, width=40)
        self.compass_data_text.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Thermal Imaging Sensor Data Section
        self.thermal_label = tk.Label(sensor_frame, text="Thermal Imaging Sensor", font=("Arial", 12))
        self.thermal_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.thermal_data_text = tk.Text(sensor_frame, height=4, width=40)
        self.thermal_data_text.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        # Camera Data Section
        self.camera_label = tk.Label(sensor_frame, text="Camera Feed", font=("Arial", 12))
        self.camera_label.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        self.camera_data_text = tk.Text(sensor_frame, height=4, width=40)
        self.camera_data_text.grid(row=7, column=1, padx=10, pady=5, sticky="w")
        
    def open_drone_control_window(self):
        """Open a new window for controlling the drone."""
        control_window = tk.Toplevel(self.root)
        control_window.title("Drone Control")
        control_window.geometry("500x400")

        # Labels and Scales for Throttle, Pitch, Roll, Yaw
        tk.Label(control_window, text="Throttle", font=("Arial", 12)).pack(pady=5)
        throttle_scale = tk.Scale(control_window, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.01)
        throttle_scale.pack()

        tk.Label(control_window, text="Pitch", font=("Arial", 12)).pack(pady=5)
        pitch_scale = tk.Scale(control_window, from_=-1, to=1, orient=tk.HORIZONTAL, resolution=0.01)
        pitch_scale.pack()

        tk.Label(control_window, text="Roll", font=("Arial", 12)).pack(pady=5)
        roll_scale = tk.Scale(control_window, from_=-1, to=1, orient=tk.HORIZONTAL, resolution=0.01)
        roll_scale.pack()

        tk.Label(control_window, text="Yaw", font=("Arial", 12)).pack(pady=5)
        yaw_scale = tk.Scale(control_window, from_=-1, to=1, orient=tk.HORIZONTAL, resolution=0.01)
        yaw_scale.pack()

        # Frame for displaying control values
        control_values_frame = tk.Frame(control_window)
        control_values_frame.pack(pady=10)

        # Throttle, Pitch, Roll, Yaw Value Labels
        self.throttle_value_label = tk.Label(control_values_frame, text="Throttle: 0.00", width=15, relief=tk.SUNKEN)
        self.throttle_value_label.grid(row=0, column=0, padx=5)

        self.pitch_value_label = tk.Label(control_values_frame, text="Pitch: 0.00", width=15, relief=tk.SUNKEN)
        self.pitch_value_label.grid(row=0, column=1, padx=5)

        self.roll_value_label = tk.Label(control_values_frame, text="Roll: 0.00", width=15, relief=tk.SUNKEN)
        self.roll_value_label.grid(row=0, column=2, padx=5)

        self.yaw_value_label = tk.Label(control_values_frame, text="Yaw: 0.00", width=15, relief=tk.SUNKEN)
        self.yaw_value_label.grid(row=0, column=3, padx=5)

        # Button to apply control changes
        apply_button = tk.Button(control_window, text="Apply", command=lambda: self.update_drone_controls(
            throttle_scale, pitch_scale, roll_scale, yaw_scale))
        apply_button.pack(pady=10)

    def update_drone_controls(self, throttle_scale, pitch_scale, roll_scale, yaw_scale):
        """Update the drone control values from the new window and display in frames."""
        throttle = throttle_scale.get()
        pitch = pitch_scale.get()
        roll = roll_scale.get()
        yaw = yaw_scale.get()

        # Update the control value labels with the current values
        self.throttle_value_label.config(text=f"Throttle: {throttle:.2f}")
        self.pitch_value_label.config(text=f"Pitch: {pitch:.2f}")
        self.roll_value_label.config(text=f"Roll: {roll:.2f}")
        self.yaw_value_label.config(text=f"Yaw: {yaw:.2f}")

    def start_simulation(self):
        """Start simulating sensor data continuously only when the button is clicked."""
        if not self.simulation_running:
            self.simulation_running = True
            self.update_sensors_data()  # Start the first update

    def update_sensors_data(self):
        """Update sensor data in the interface every second using Tkinter's after() method."""
        if self.simulation_running:
            # IMU Data
            imu_data = self.imu.get_imu_data()
            self.imu_data_text.delete(1.0, tk.END)
            self.imu_data_text.insert(tk.END, imu_data)

            # Proximity Sensors Data
            proximity_data = self.proximity_sensors.get_proximity_data()
            self.proximity_data_text.delete(1.0, tk.END)
            self.proximity_data_text.insert(tk.END, proximity_data)

            # Barometer Data
            barometer_data = self.barometer.get_barometer_data()
            self.barometer_data_text.delete(1.0, tk.END)
            self.barometer_data_text.insert(tk.END, barometer_data)

            # LIDAR Data
            lidar_data = self.lidar.get_lidar_data()
            self.lidar_data_text.delete(1.0, tk.END)
            self.lidar_data_text.insert(tk.END, lidar_data)

            # Optical Flow Sensor Data
            optical_flow_data = self.optical_flow_sensor.get_optical_flow_data()
            self.optical_flow_data_text.delete(1.0, tk.END)
            self.optical_flow_data_text.insert(tk.END, optical_flow_data)

            # Compass Data
            compass_data = self.compass.get_compass_data()
            self.compass_data_text.delete(1.0, tk.END)
            self.compass_data_text.insert(tk.END, compass_data)

            # Thermal Imaging Sensor Data
            thermal_data = self.thermal_sensor.get_thermal_data()
            self.thermal_data_text.delete(1.0, tk.END)
            self.thermal_data_text.insert(tk.END, thermal_data)

            # Camera Data
            camera_data = self.camera.get_camera_data()
            self.camera_data_text.delete(1.0, tk.END)
            self.camera_data_text.insert(tk.END, camera_data)

            # Schedule the next sensor data update after 1 second (1000 ms)
            self.root.after(1000, self.update_sensors_data)

    def launch_drone(self):
        # Run pathfinding to get the path coordinates
        if self.coordinates is not None:
            drone_coordinates = [29.38, 79.47]  # Initial drone position (example)
            path_coords = run_pathfinding(self.coordinates, drone_coordinates)

            # Start moving the drone along the path
            self.move_drone_along_path(path_coords)
        else:
            messagebox.showwarning("Coordinates Missing", "Please enter manual coordinates first.")

    def move_drone_along_path(self, path_coords):
        """Move the drone incrementally along the path coordinates."""
        def update_position(i=0):
            if i < len(path_coords):
                # Update the drone's position to the next coordinate on the path
                lat, lon = path_coords[i]
                
                # Simulate updating the drone's GPS position (replace this if real-time GPS is used)
                self.drone_position = [lat, lon]

                # Redraw the map with the updated position
                self.update_map_position(lat, lon)

                # Schedule the next update (moving to the next point on the path)
                self.root.after(1000, update_position, i + 1)  # Update every 1 second
            else:
                print("Drone reached the destination.")
        
        # Start the movement
        update_position()

    def update_map_position(self, lat, lon):
        """Update the map with the new drone position."""
        # Send the updated coordinates to the map (tracking_map.html or the React app)
        data = {'latitude': lat, 'longitude': lon}
        try:
            response = requests.post('http://127.0.0.1:5000/update-drone-position', json=data)
            if response.status_code == 200:
                print(f"Updated drone position to: ({lat}, {lon})")
            else:
                print("Failed to update the map.")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")

    def confirm_delivery(self):
        if self.travel_delivery:
            self.travel_delivery.deliver_payload()
            messagebox.showinfo("Delivery", "Payload Delivered Successfully!")

    def open_manual_coordinates(self):
        manual_coords_window = tk.Toplevel(self.root)
        ManualCoordinatesInterface(manual_coords_window, self)

    def track_drone(self):
        if self.coordinates is not None:
            # Set manual coordinates and
                    # Set manual coordinates and start pathfinding
            self.set_manual_coordinates()

            # Example drone coordinates (can be dynamic)
            drone_coordinates = [29.38, 79.47]  # Replace with actual drone position
            
            # Run the pathfinding between manual coordinates and drone coordinates
            run_pathfinding(self.coordinates, drone_coordinates)
            
            os.system("C:\\Users\\kaudi\\Desktop\\REVIVE HACKATHON\\drone-tracker & npm start")

            # Open the generated tracking map in a new browser tab
            webbrowser.open("tracking_map.html", new=2)
        else:
            messagebox.showwarning("Coordinates Missing", "Please enter manual coordinates first.")

    def set_manual_coordinates(self):
        lat, lon = self.coordinates
        data = {'latitude': lat, 'longitude': lon}
        try:
            response = requests.post('http://127.0.0.1:5000/manual-coordinates', json=data)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Manual coordinates set successfully.")
            else:
                messagebox.showerror("Error", "Failed to set manual coordinates.")
        except requests.exceptions.ConnectionError as e:
            messagebox.showerror("Connection Error", f"Could not connect to the Flask server: {e}")

    def run_flask_server(self):
        subprocess.run(["python", "server.py"])

class ManualCoordinatesInterface:
    def __init__(self, root, parent_app):
        self.root = root
        self.root.title("Manual Coordinates Input")
        self.root.geometry("400x200")  # Set window size
        self.parent_app = parent_app  # To pass coordinates back to the main interface

        self.create_widgets()

    def create_widgets(self):
        self.enter_coords_button = tk.Button(self.root, text="Enter Coordinates", command=self.get_coordinates)
        self.enter_coords_button.pack(pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
        self.exit_button.pack(pady=10)

    def get_coordinates(self):
        lat = simpledialog.askfloat("Input", "Enter Latitude:", parent=self.root)
        lng = simpledialog.askfloat("Input", "Enter Longitude:", parent=self.root)

        if lat is not None and lng is not None:
            self.parent_app.coordinates = [lat, lng]
            messagebox.showinfo("Coordinates Registered", f"Coordinates: {self.parent_app.coordinates}")
        else:
            messagebox.showwarning("Input Error", "Please enter valid coordinates.")

# Main loop to run the interface
if __name__ == "__main__":
    root = tk.Tk()
    app = DroneInterface(root)
    root.mainloop()

