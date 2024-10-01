from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Simulated sensor data
sensor_data = {
    'imu': [[0, 0, 0], [0, 0, 0]],  # Accelerometer, Gyroscope data
    'proximity': {'front': 0, 'back': 0, 'left': 0, 'right': 0},
    'barometer': {'altitude': 0, 'pressure': 1013.25},
    'lidar': 0,
    'optical_flow': {'x': 0, 'y': 0},
    'compass': 0,
    'thermal': {'temperature': 0, 'heat_signature': False},
    'camera': "Low-Quality Video Feed",
    'gps': {'latitude': 29.38, 'longitude': 79.47}  # Default to Nainital Cantonment
}

drone_active = False
@app.route('/update-drone-position', methods=['POST'])
def update_drone_position():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Update the drone's position on the map
    # This could involve re-rendering the map with new coordinates
    # Or using WebSockets if you're updating the map in real-time

    # Return success response
    return jsonify({'status': 'success', 'message': 'Drone position updated.'})

@app.route('/start-drone', methods=['POST'])
def start_drone():
    global drone_active
    drone_active = True
    return jsonify({'message': 'Drone started successfully'}), 200

@app.route('/stop-drone', methods=['POST'])
def stop_drone():
    global drone_active
    drone_active = False
    return jsonify({'message': 'Drone stopped successfully'}), 200

@app.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    if drone_active:
        # Simulate sensor data updates
        sensor_data['imu'][0] = [random.uniform(-10, 10) for _ in range(3)]  # Accelerometer
        sensor_data['imu'][1] = [random.uniform(-500, 500) for _ in range(3)]  # Gyroscope
        sensor_data['proximity'] = {key: round(random.uniform(0.5, 10.0), 2) for key in sensor_data['proximity']}
        sensor_data['barometer']['altitude'] = round(random.uniform(0, 5000), 2)
        sensor_data['barometer']['pressure'] = round(random.uniform(900, 1050), 2)
        sensor_data['lidar'] = round(random.uniform(1, 100), 2)
        sensor_data['optical_flow'] = {'x': random.uniform(-5, 5), 'y': random.uniform(-5, 5)}
        sensor_data['compass'] = round(random.uniform(0, 360), 2)
        sensor_data['thermal']['temperature'] = round(random.uniform(-20, 100), 2)
        sensor_data['thermal']['heat_signature'] = random.choice([True, False])
        # Simulate GPS location updates
        sensor_data['gps']['latitude'] += random.uniform(-0.001, 0.001)
        sensor_data['gps']['longitude'] += random.uniform(-0.001, 0.001)
    return jsonify(sensor_data)

@app.route('/manual-coordinates', methods=['POST'])
def set_manual_coordinates():
    data = request.get_json()
    if 'latitude' in data and 'longitude' in data:
        sensor_data['gps']['latitude'] = data['latitude']
        sensor_data['gps']['longitude'] = data['longitude']
        return jsonify({'message': 'Coordinates updated successfully'}), 200
    return jsonify({'message': 'Invalid coordinates'}), 400

@app.route('/gps', methods=['GET'])
def get_gps_coordinates():
    return jsonify(sensor_data['gps'])

if __name__ == '__main__':
    app.run(debug=True)











