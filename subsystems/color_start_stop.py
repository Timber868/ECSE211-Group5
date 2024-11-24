#!/usr/bin/env python3

from subsystems.utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, Motor
from ast import literal_eval
import time
from subsystems.collect_color_sensor_data import collect_color_sensor_data
from math import sqrt

# INITIALIZING OBJECTS

# REFER TO note_deciding.py FOR PORTS
COLOR_SENSOR_LEFT = EV3ColorSensor(4)
COLOR_SENSOR_RIGHT = EV3ColorSensor(2)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

# START OF PROGRAM

red_measured, green_measured, blue_measured = 0, 0, 0           # initializing the measured colors' values\
left_color_array =[]
right_color_array=[]

def get_average_RGB_from_csv(i):
        
    red_measured, green_measured, blue_measured = 0, 0, 0      # reset (because of infinite while loop)

    n_lines = 0                                                 # track number of lines (measurements) to compute mean
    collect_color_sensor_data(left_color_array,right_color_array)

    a_array = []
    if i == "left":
        a_array = left_color_array
    else:
        a_array = right_color_array

        
    for colors in a_array:
        r, g, b = colors # convert string to 3 floats
        if r != None and g != None and b != None:
            red_measured += r
            green_measured += g
            blue_measured += b
        n_lines = n_lines + 1
        
        red_measured_avg = red_measured / n_lines
        green_measured_avg = green_measured / n_lines
        blue_measured_avg = blue_measured / n_lines 
    

    return(red_measured_avg, green_measured_avg, blue_measured_avg)

match_colors = {}                                               # initializing the colors dict for color matching
def color_matching(i):
    DETECTED_COLOR = None

    r_avg, g_avg, b_avg =  get_average_RGB_from_csv(i)
    #print(r_avg, g_avg, b_avg)

    if r_avg > 95 and g_avg > 12 and g_avg < 40 and b_avg > 5 and b_avg < 25:
        DETECTED_COLOR = "red"
    elif r_avg > 80 and g_avg > 45 and g_avg < 100 and b_avg > 15 and b_avg < 50:
        DETECTED_COLOR = "orange"
    elif r_avg < 35 and r_avg > 15  and g_avg > 65 and g_avg < 150 and b_avg > 12 and b_avg < 35:
        DETECTED_COLOR = "green"
    elif r_avg > 130 and g_avg > 90 and g_avg < 250 and b_avg > 8 and b_avg < 30:
        DETECTED_COLOR = "yellow"
    elif r_avg > 15 and r_avg < 40 and g_avg > 15 and g_avg < 50 and b_avg > 20 and b_avg< 60:
        DETECTED_COLOR = "water"
    elif r_avg > 20 and g_avg > 30 and g_avg < 175 and b_avg < 24:
        DETECTED_COLOR = "ground"    
      # DETECTED_COLOR = "green"
    else:
        DETECTED_COLOR = "nothing"        
    
    if DETECTED_COLOR == None:
        print("COLOR WAS NOT CLOSE ENOUGH TO REFERENCE COLORS")
    
    return DETECTED_COLOR

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

def get_left_sensor_color():
    DETECTED_COLOR = None
    while DETECTED_COLOR == None:
        collect_color_sensor_data(left_color_array,right_color_array)
        DETECTED_COLOR = color_matching("left")
    print(f"left color detected: {DETECTED_COLOR}")
    return DETECTED_COLOR

def get_right_sensor_color():
    DETECTED_COLOR = None
    while DETECTED_COLOR == None:
        collect_color_sensor_data(left_color_array,right_color_array)
        DETECTED_COLOR = color_matching("right")
    
    print(f"right color detected: {DETECTED_COLOR}")
    return DETECTED_COLOR

def get_both_sensor_color():
    DETECTED_COLOR_LEFT = None
    DETECTED_COLOR_RIGHT = None
    while DETECTED_COLOR_LEFT == None or DETECTED_COLOR_RIGHT == None:
        collect_color_sensor_data(left_color_array,right_color_array)
        DETECTED_COLOR_LEFT = color_matching("left")
        DETECTED_COLOR_RIGHT = color_matching("right")
    print(f"left: {DETECTED_COLOR_LEFT}, right: {DETECTED_COLOR_RIGHT}")
    return (DETECTED_COLOR_LEFT, DETECTED_COLOR_RIGHT)
     
# # #     return (DETECTED_COLOR_LEFT, DETECTED_COLOR_RIGHT)



if __name__ == "__main__": 
    get_both_sensor_color()
