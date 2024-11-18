#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from subsystems.utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor
from time import sleep

COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensorGREEN.csv"

# complete this based on your hardware setup
COLOR_SENSOR_LEFT = EV3ColorSensor(4)
COLOR_SENSOR_RIGHT = EV3ColorSensor(2)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

# How it works:
# 1.when the function is called, at each button press, it prints the r, g, b values
# 2.when Ctrl + C is pressed, it writes the values to a file and terminates
def collect_color_sensor_data():
    "Collect color sensor data."
    try:
        output_file = open(COLOR_SENSOR_DATA_FILE, "w")
        while(1):
                sleep(0.5)
                aColors = COLOR_SENSOR.get_rgb() #Hungarian notation, array of [R, G, B] colors
                sColors = str(aColors[0]) + "," + str(aColors[1]) + "," + str(aColors[2])
                if (aColors != [None, None, None]):
                    print(sColors)
                    output_file.write(f"{sColors}\n")
        
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        pass
    finally:
        output_file.close()
        print("file closed")
        exit()

def is_yellow():
    rgb = COLOR_SENSOR_LEFT.get_rgb()
    red, green, blue = rgb
    
    print(red)
    print(green)
    print(blue)
    if red > 100 and green > 50 and blue < 100:
        print("is yellows")
        return True
    else:
        return False
    
    
if __name__ == "__main__":
    is_yellow()
