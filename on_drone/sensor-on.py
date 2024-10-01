import time
import random
import threading
import serial  # Assuming we're using a serial port for data transmission
import json

class IMU:
    def __init__(self):
        self.accelerometer = [0, 0, 0]  # X, Y, Z
        self.gyroscope = [0, 0, 0]      # X, Y, Z

    def get_imu_data(self):
        """Simulate IMU data collection from accelerometer and gyroscope."""
        self.accelerometer = [round(random.uniform(-10, 10), 2) for _ in range(3)]
        self.gyroscope = [round(random.uniform(-500, 500), 2) for _ in range(3)]
        return {"accelerometer": self.accelerometer, "gyroscope": self.gyroscope}

class DataTransmitter:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        # Initialize serial communication for data transmission
        self.serial_port = serial.Serial(port, baudrate, timeout=1)

    def send_data(self, data):
        """Send data over the serial port."""
        try:
            json_data = json.dumps(data)  # Convert data to JSON
            self.serial_port.write(json_data.encode())  # Send the data
            print(f"Sent data: {json_data}")
        except Exception as e:
            print(f"Error transmitting data: {e}")

def collect_and_send_data():
    imu = IMU()
    transmitter = DataTransmitter()

    while True:
        # Collect IMU data
        imu_data = imu.get_imu_data()
        
        # Send IMU data
        transmitter.send_data(imu_data)
        
        # Sleep for 1 second before the next transmission
        time.sleep(1)

if __name__ == "__main__":
    # Run data collection and transmission in a separate thread
    data_thread = threading.Thread(target=collect_and_send_data)
    data_thread.start()