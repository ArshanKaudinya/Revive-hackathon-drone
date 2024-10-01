import random
import time
import threading

class IMU:
    def __init__(self):
        self.accelerometer = [0, 0, 0]  # X, Y, Z
        self.gyroscope = [0, 0, 0]  # X, Y, Z
        self.magnetometer = [0, 0, 0]  # X, Y, Z

    def get_imu_data(self):
        """Simulate IMU data."""
        self.accelerometer = [round(random.uniform(-10, 10), 2) for _ in range(3)]
        self.gyroscope = [round(random.uniform(-500, 500), 2) for _ in range(3)]
        self.magnetometer = [round(random.uniform(-50, 50), 2) for _ in range(3)]

        return (
            f"IMU - Accelerometer: X={self.accelerometer[0]} Y={self.accelerometer[1]} Z={self.accelerometer[2]}\n"
            f"IMU - Gyroscope: X={self.gyroscope[0]} Y={self.gyroscope[1]} Z={self.gyroscope[2]}\n"
            f"IMU - Magnetometer: X={self.magnetometer[0]} Y={self.magnetometer[1]} Z={self.magnetometer[2]}"
        )

class ProximitySensors:
    def __init__(self):
        self.sensors = {"front": 0, "back": 0, "left": 0, "right": 0}

    def get_proximity_data(self):
        """Simulate proximity sensor data (distance in meters)."""
        for direction in self.sensors:
            self.sensors[direction] = round(random.uniform(0.5, 10.0), 2)  # Random distance from 0.5 to 10 meters

        return (
            f"Proximity\nFront: {self.sensors['front']}m, Back: {self.sensors['back']}m,\n"
            f"Left: {self.sensors['left']}m, Right: {self.sensors['right']}m"
        )

class Barometer:
    def __init__(self):
        self.altitude = 0.0  # Altitude in meters
        self.pressure = 1013.25  # Pressure in hPa

    def get_barometer_data(self):
        """Simulate barometer data (altitude in meters, pressure in hPa)."""
        self.altitude = round(random.uniform(0, 5000), 2)  # Random altitude from 0 to 5000 meters
        self.pressure = round(random.uniform(900, 1050), 2)  # Random pressure from 900 to 1050 hPa

        return f"Barometer - Altitude: {self.altitude}m,\nPressure: {self.pressure}hPa"

class LIDAR:
    def __init__(self):
        self.distance = 0.0

    def get_lidar_data(self):
        """Simulate LIDAR distance data (distance in meters)."""
        self.distance = round(random.uniform(1, 100), 2)  # Random distance from 1 to 100 meters

        return f"LIDAR - Distance: {self.distance}m"

class OpticalFlowSensor:
    def __init__(self):
        self.velocity = [0, 0]  # X and Y velocity

    def get_optical_flow_data(self):
        """Simulate optical flow sensor data (velocity in pixels/second)."""
        self.velocity = [round(random.uniform(-5, 5), 2) for _ in range(2)]  # Random velocity from -5 to 5

        return f"Optical Flow - Velocity\nX: {self.velocity[0]}px/s,\nY: {self.velocity[1]}px/s"

class Compass:
    def __init__(self):
        self.heading = 0.0  # Heading in degrees from North

    def get_compass_data(self):
        """Simulate compass data (heading in degrees)."""
        self.heading = round(random.uniform(0, 360), 2)  # Random heading from 0 to 360 degrees

        return f"Compass - Heading: {self.heading}°"

class ThermalImagingSensor:
    def __init__(self):
        self.temperature = 0.0
        self.heat_signature_detected = False

    def get_thermal_data(self):
        """Simulate thermal imaging data (temperature in Celsius, heat signature)."""
        self.temperature = round(random.uniform(-20, 100), 2)  # Random temperature from -20 to 100°C
        self.heat_signature_detected = random.choice([True, False])  # Randomly detect heat signature

        return (
            f"Thermal Imaging - Temperature: {self.temperature}°C,\n"
            f"Heat Signature: {'Detected' if self.heat_signature_detected else 'Not Detected'}"
        )

class Camera:
    def __init__(self):
        self.resolution = "Low"  # Placeholder for low-quality video feed

    def get_camera_data(self):
        """Simulate camera data (low-quality video feed placeholder)."""
        return "Camera - Low-Quality Video Feed"

