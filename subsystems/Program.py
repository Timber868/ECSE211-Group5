#!/usr/bin/env python3

import time
from subsystems import Avoidance, motor_arm_settings, motor_settings, object_detection, color_sensor_start_stop
from subsystems.utils.brick import reset_brick
import threading

stop_robot = False

def monitor_color_sensor():
    global stop_robot
    while not stop_robot:
        left_color, right_color = color_sensor_start_stop.get_both_sensor_color()
        if left_color == "water" or right_color == "water":
            stop_robot = True
        time.sleep(0.1)  # Reduce CPU usage

if __name__ == "__main__":
    try:
        # Set up motors and sensors
        motor_settings.wheel_limits(100, 180, 100, 180)
        motor_arm_settings.arm_limits(80, 100, 80, 100)

        object_detection.DETECTED_BLOCKS = []

        # Main loop for robot behavior
        while not stop_robot:
            # Perform regular actions
            object_detection.a_gyro(30, 30)
            time.sleep(0.5)  # Simulate other robot tasks

        # Stop the robot when water is detected
        motor_settings.speed(0, 0)
        motor_settings.power(0, 0)
        print("Water detected. Robot stopped.")

    except KeyboardInterrupt:
        reset_brick()
        print("Robot was interrupted")

    finally:
        # Ensure the robot is stopped on exit
        reset_brick()
        print("Robot safely stopped.")
