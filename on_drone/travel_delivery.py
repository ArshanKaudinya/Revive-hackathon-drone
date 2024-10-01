import time
import math

class TravelDelivery:
    def __init__(self, path_coords, speed=5):
        self.path_coords = path_coords
        self.current_position = path_coords[0]  # Starting position
        self.target_position = path_coords[-1]  # Destination
        self.speed = speed  # Drone speed (arbitrary units)
        self.rotor_speeds = [0, 0, 0, 0]  # Initial rotor speeds
        self.payload_delivered = False

    def calculate_distance(self, pos1, pos2):
        return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)

    def calculate_rotor_speeds(self, target_pos):
        distance = self.calculate_distance(self.current_position, target_pos)
        direction_x = target_pos[0] - self.current_position[0]
        direction_y = target_pos[1] - self.current_position[1]
        
        # Adjust rotor speeds based on direction
        if direction_x > 0:
            self.rotor_speeds[0] = self.speed  # Prop 1 forward
            self.rotor_speeds[1] = self.speed  # Prop 2 forward
        else:
            self.rotor_speeds[0] = -self.speed  # Prop 1 backward
            self.rotor_speeds[1] = -self.speed  # Prop 2 backward

        if direction_y > 0:
            self.rotor_speeds[2] = self.speed  # Prop 3 forward
            self.rotor_speeds[3] = self.speed  # Prop 4 forward
        else:
            self.rotor_speeds[2] = -self.speed  # Prop 3 backward
            self.rotor_speeds[3] = -self.speed  # Prop 4 backward

        return self.rotor_speeds

    def update_position(self):
        # Move towards target position
        for coord in self.path_coords[1:]:
            self.rotor_speeds = self.calculate_rotor_speeds(coord)
            self.current_position = coord
            print(f"Moving to {self.current_position} with rotor speeds {self.rotor_speeds}")
            time.sleep(1)  # Simulate travel time

    def deliver_payload(self):
        self.payload_delivered = True
        print("Payload delivered.")

    def get_flight_time(self):
        # Approximate flight time calculation
        total_distance = sum(self.calculate_distance(self.path_coords[i], self.path_coords[i+1]) 
                             for i in range(len(self.path_coords)-1))
        flight_time = total_distance / self.speed  # Assuming speed is constant
        return flight_time