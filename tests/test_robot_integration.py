# tests/test_robot_integration.py

import pytest
from app.modules.robot_integration import RobotIntegration

@pytest.fixture
def robot_integration_instance():
    """
    Creates a fresh RobotIntegration instance for each test.
    """
    return RobotIntegration()

def test_connect_robot_hardware(robot_integration_instance):
    """
    Tests whether robot hardware 'connects' successfully in the stub.
    """
    # Initially, we expect the robot to be disconnected:
    assert not robot_integration_instance.connected

    # Call connect_robot_hardware (stub just sets connected=True)
    robot_integration_instance.connect_robot_hardware()
    assert robot_integration_instance.connected, "Robot should be marked connected after calling connect_robot_hardware."

def test_send_motor_command_disconnected(robot_integration_instance, capsys):
    """
    If the robot is not connected, sending a motor command should produce a warning,
    or be ignored. We capture stdout to confirm the message.
    """
    # Robot not connected yet
    robot_integration_instance.send_motor_command(0.1, 0.2)

    captured = capsys.readouterr()
    assert "Warning: Robot not connected" in captured.out

def test_send_motor_command_connected(robot_integration_instance, capsys):
    """
    Once connected, sending a motor command should print the correct message.
    """
    robot_integration_instance.connect_robot_hardware()
    robot_integration_instance.send_motor_command(0.1, 0.2)

    captured = capsys.readouterr()
    assert "Motor cmd - lin: 0.10, ang: 0.20" in captured.out

def test_get_robot_pose_default(robot_integration_instance):
    """
    By default, the pose should be (0.0, 0.0, 0.0).
    """
    pose = robot_integration_instance.get_robot_pose()
    assert pose == (0.0, 0.0, 0.0), "Expected default pose to be (0,0,0)."

def test_set_robot_pose(robot_integration_instance, capsys):
    """
    set_robot_pose should update the instance's current_pose
    and print a message if connected.
    """
    robot_integration_instance.connect_robot_hardware()
    robot_integration_instance.set_robot_pose(1.5, 2.5, 1.57)

    pose = robot_integration_instance.get_robot_pose()
    assert pose == (1.5, 2.5, 1.57)

def test_get_camera_frame_disconnected(robot_integration_instance):
    """
    If the robot is not connected, get_robot_camera_frame should return None.
    """
    frame = robot_integration_instance.get_robot_camera_frame()
    assert frame is None

def test_get_camera_frame_connected(robot_integration_instance):
    """
    In the stub, get_robot_camera_frame returns None even when connected,
    but let's confirm no errors occur.
    In a real test, you'd mock the camera feed or ROS subscription.
    """
    robot_integration_instance.connect_robot_hardware()
    frame = robot_integration_instance.get_robot_camera_frame()
    # The default stub returns None
    assert frame is None
