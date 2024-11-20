#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from subsystems.utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor
from time import sleep

# complete this based on your hardware setup
COLOR_SENSOR_LEFT = EV3ColorSensor(4)
COLOR_SENSOR_RIGHT = EV3ColorSensor(2)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

# How it works:
# 1.when the function is called, at each button press, it prints the r, g, b values
# 2.when Ctrl + C is pressed, it writes the values to a file and terminates
def collect_color_sensor_data(left_color_array, right_color_array):
    "Collect color sensor data."
    try:
        i = 0
        # output_file = open(COLOR_SENSOR_DATA_FILE, "w")
        while i<10:
                left_colors = COLOR_SENSOR_LEFT.get_rgb() #Hungarian notation, array of [R, G, B] colors
                right_colors = COLOR_SENSOR_RIGHT.get_rgb()
                # sColors = str(aColors[0]) + "," + str(aColors[1]) + "," + str(aColors[2])
                if (left_colors != [None, None, None]):
                    print(f"left color added : {left_colors}" )
                    left_color_array.append(left_colors)
                if (right_colors != [None, None, None]):
                    print(f"right color added : {right_colors}" )
                    right_color_array.append(right_colors)
                sleep(0.02)
                i = i + 1
        
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        pass
    
if __name__ == "__main__":
    collect_color_sensor_data()