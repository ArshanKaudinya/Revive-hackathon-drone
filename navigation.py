import numpy as np
import time

class KalmanFilter:
    def __init__(self, initial_position, initial_velocity, delta_time):
        self.dt = delta_time  # Time step
        self.x = np.array([[initial_position], [initial_velocity]])  # Initial state (position, velocity)
        self.A = np.array([[1, self.dt], [0, 1]])  # State transition matrix
        self.B = np.array([[0.5 * self.dt**2], [self.dt]])  # Control matrix (for acceleration)
        self.H = np.array([[1, 0]])  # Observation matrix (we only observe position)
        self.P = np.eye(2)  # Initial covariance matrix
        self.Q = np.array([[1, 0], [0, 3]])  # Process noise covariance
        self.R = np.array([[10]])  # Measurement noise covariance
        self.u = 0  # Acceleration (control input)

    def predict(self):
        """ Prediction step of the Kalman filter """
        self.x = self.A @ self.x + self.B * self.u
        self.P = self.A @ self.P @ self.A.T + self.Q
        return self.x[0][0], self.x[1][0]  # Return predicted position and velocity

    def update(self, z):
        """ Update step of the Kalman filter """
        y = z - (self.H @ self.x)
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (np.eye(2) - K @ self.H) @ self.P
        return self.x[0][0], self.x[1][0]  # Return updated position and velocity

def simulate_acceleration():
    """ Simulate random acceleration data for X and Y axes """
    return [round(np.random.uniform(-2, 2), 2) for _ in range(2)]  # Random acceleration

def simulate_movement(acceleration, kalman_filter, predicted_position):
    """ Simulate movement and update the position in X and Y axes using the Kalman filter """
    measured_position = [
        predicted_position[0] + acceleration[0] * 0.5 * (kalman_filter.dt**2),
        predicted_position[1] + acceleration[1] * 0.5 * (kalman_filter.dt**2)
    ]
    updated_position, _ = kalman_filter.update(measured_position[0])  # Update X-axis (modify as needed)
    return updated_position

def continuous_update(kalman_filter, update_interval=1):
    """ Continuously update the position based on simulated movement and acceleration """
    position = [29.38, 79.47]  # Starting position
    while True:
        acceleration = simulate_acceleration()
        position[0] = simulate_movement(acceleration, kalman_filter, position)
        print(f"Updated Position: {position}")
        time.sleep(update_interval)  # Update every `update_interval` seconds




