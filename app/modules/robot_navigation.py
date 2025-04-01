# app/modules/robot_navigation.py

import math

class RobotNavigation:
    """
    Handles higher-level navigation logic for the robot, including:
      - Storing a target location (x, y)
      - Periodically computing speed commands to move the robot toward the goal
      - Stopping when the goal is reached

    In a real-world setup, you would integrate with a more advanced path-planning
    algorithm and obstacle avoidance techniques, possibly using SLAM to handle 
    unknown or dynamic environments.

    This file is provided as a simple template to show how you might structure a 
    RobotNavigation module in Python.
    """

    def __init__(self, building_model, robot_integration):
        """
        :param building_model: Data structure from ingestion, describing the environment.
        :param robot_integration: Instance of RobotIntegration for sending motor commands 
                                  and receiving pose updates.
        """
        self.building_model = building_model
        self.robot_integration = robot_integration

        # If the robot is told to go somewhere, store the target here
        self.target_location = None   # (x, y) in building coordinate space
        self.arrival_threshold = 0.2  # distance in meters for "close enough"

    def set_destination(self, x, y):
        """
        Set a global navigation goal (x, y) in the building coordinate system.
        For instance, if the user or system says: "Go to the fridge, which is at (5, 2)."

        :param x: Target x-coordinate in building coordinate system
        :param y: Target y-coordinate in building coordinate system
        """
        self.target_location = (x, y)
        print(f"[RobotNavigation] Destination set to (x={x:.2f}, y={y:.2f})")

    def clear_destination(self):
        """Clear the current destination, causing the robot to stop navigating."""
        self.target_location = None
        print("[RobotNavigation] Destination cleared.")

    def update_navigation(self):
        """
        Called periodically (e.g., in the main loop) to move the robot toward the target
        if one is set. When the robot is close enough to the target, it stops.

        This simple example just drives in a straight line towards the target, ignoring
        obstacles and orientation. In reality, you would incorporate a path-planning
        algorithm and rotate the robot to the correct heading, etc.
        """
        # 1. If no target is set, do nothing
        if self.target_location is None:
            self.robot_integration.send_motor_command(0.0, 0.0)
            return

        # 2. Get current robot pose
        current_pose = self.robot_integration.get_robot_pose()  # (x, y, theta)
        x_now, y_now, theta_now = current_pose

        # 3. Compute distance to target
        dx = self.target_location[0] - x_now
        dy = self.target_location[1] - y_now
        distance = math.sqrt(dx**2 + dy**2)

        # 4. If within arrival threshold, stop
        if distance < self.arrival_threshold:
            print("[RobotNavigation] Destination reached. Stopping.")
            self.robot_integration.send_motor_command(0.0, 0.0)
            self.clear_destination()
            return

        # 5. Otherwise, move forward
        #    This is a naive approach. A real approach might:
        #      - Compute heading error
        #      - Rotate the robot towards the heading
        #      - Move forward
        #    Here, we simply set a small linear speed, no rotation.
        linear_speed = 0.1  # 0.1 m/s forward
        angular_speed = 0.0 # no turning in this simplified approach

        self.robot_integration.send_motor_command(linear_speed, angular_speed)
