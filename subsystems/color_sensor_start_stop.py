#!/usr/bin/env python3

# This script is for color detection. It will collect the data from both color sensors
# And return the result in a String tuple.
# def: get_both_sensor_color() -> ("red","water")
# Color set: red, yellow, orange, green, water, ground, others.
# @anthor: Zhengxuan Zhao

from subsystems.utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, Motor
from time import sleep
from subsystems.object_detection import *

# INITIALIZING OBJECTS
map_color_data = {"color_left": None, "color_right": None}

stop_sequence = False
# REFER TO note_deciding.py FOR PORTS
COLOR_SENSOR_LEFT = EV3ColorSensor(4)
COLOR_SENSOR_RIGHT = EV3ColorSensor(2)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

# START OF PROGRAM

DETECTED_BLOCK_COLOR = None

red_measured, green_measured, blue_measured = 0, 0, 0 # initializing the measured colors' values\
left_color_array =[] # initializing the data array for left color sensor
right_color_array=[] # initializing the data array for right color sensor

def collect_color_sensor_data(left_color_array, right_color_array):
    "Collect color sensor data."
    left_color_array.clear()
    right_color_array.clear()
    try:
        i = 0
        while i<4: # just the i here to make faster data collection
                left_colors = COLOR_SENSOR_LEFT.get_rgb()
                right_colors = COLOR_SENSOR_RIGHT.get_rgb()
   
                if (left_colors != [None, None, None]):
                    #print(f"left color added : {left_colors}" )
                    left_color_array.append(left_colors)
                if (right_colors != [None, None, None]):
                    # print(f"right color added : {right_colors}" )
                    right_color_array.append(right_colors)
                sleep(0.01)
                i = i + 1
        
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        pass

def get_average_RGB_from_csv(array):
        
    red_measured, green_measured, blue_measured = 0, 0, 0 # reset (because of infinite while loop)

    n_lines = 0  # track number of lines (measurements) to compute average
        
    for colors in array:
        r, g, b = colors # convert string to 3 floats
        if r != None and g != None and b != None:
            red_measured += r
            green_measured += g
            blue_measured += b
        n_lines = n_lines + 1
        
        red_measured_avg = red_measured / n_lines
        green_measured_avg = green_measured / n_lines
        blue_measured_avg = blue_measured / n_lines 
    
    # return the average of r, g, b values
    return(red_measured_avg, green_measured_avg, blue_measured_avg)

def color_matching(i):
    DETECTED_COLOR = None

    r_avg, g_avg, b_avg =  get_average_RGB_from_csv(i)
    #print(r_avg, g_avg, b_avg)

    # About to change if any miss dectection
    if r_avg > 95 and g_avg > 12 and g_avg < 45 and b_avg > 5 and b_avg < 25:
        DETECTED_COLOR = "red" # grid
    elif r_avg > 80 and g_avg > 45 and g_avg < 100 and b_avg > 15 and b_avg < 50:
        DETECTED_COLOR = "orange" # poop
    elif r_avg < 35 and r_avg > 15  and g_avg > 65 and g_avg < 150 and b_avg > 12 and b_avg < 35:
        DETECTED_COLOR = "green" # seat
    elif r_avg > 130 and g_avg > 90 and g_avg < 250 and b_avg > 8 and b_avg < 30:
        DETECTED_COLOR = "yellow" # poop & trash area
    elif r_avg > 15 and r_avg < 40 and g_avg > 15 and g_avg < 50 and b_avg > 20 and b_avg< 60:
        DETECTED_COLOR = "water" # water
    elif r_avg > 20 and g_avg > 30 and g_avg < 175 and b_avg < 24:
        DETECTED_COLOR = "ground" # ground   
    else:
        DETECTED_COLOR = "others" # people and other obstacles       
    
    if DETECTED_COLOR == None:
        print("DETECTION ERROR")
    
    return DETECTED_COLOR

def color_matching_left(i):
    DETECTED_COLOR = None

    r_avg, g_avg, b_avg =  get_average_RGB_from_csv(i)
    print(r_avg, g_avg, b_avg)

    # About to change if any miss dectection
    if 8 < r_avg < 12  and 15 < g_avg < 20 and 1 < b_avg < 2:
        DETECTED_COLOR = "green" # seat
    elif 30 < r_avg < 40 and 20 < g_avg < 30 and 1 < b_avg < 4:
        DETECTED_COLOR = "yellow" # poop & trash area
    elif 2 < r_avg < 5 and 4 < g_avg < 6 and 4 < b_avg < 7:
        DETECTED_COLOR = "water" # water
    else:
        DETECTED_COLOR = "others" # people and other obstacles       
    
    if DETECTED_COLOR == None:
        print("DETECTION ERROR")
    
    return DETECTED_COLOR
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

def get_block_color(color_data):
    DETECTED_BLOCK_COLOR = None
    left_color_array = []
    right_color_array = []
    while DETECTED_BLOCK_COLOR == None:
        while DETECTED_BLOCK_COLOR != "yellow" and DETECTED_BLOCK_COLOR != "orange":
            collect_color_sensor_data(left_color_array,right_color_array)
            DETECTED_BLOCK_COLOR = color_matching(left_color_array)

    
    color_data["color"] = DETECTED_BLOCK_COLOR
    print(f"left color detected: {DETECTED_BLOCK_COLOR}")
    return DETECTED_BLOCK_COLOR

def get_left_sensor_color():
    DETECTED_COLOR = None
    left_color_array = []
    right_color_array = []
    while DETECTED_COLOR == None:
        collect_color_sensor_data(left_color_array,right_color_array)
        DETECTED_COLOR = color_matching_left(left_color_array)
    print(f"left color detected: {DETECTED_COLOR}")
    return DETECTED_COLOR

def get_right_sensor_color():
    DETECTED_COLOR = None
    left_color_array = []
    right_color_array = []
    while DETECTED_COLOR == None:
        collect_color_sensor_data(left_color_array,right_color_array)
        DETECTED_COLOR = color_matching(right_color_array)
    print(f"right color detected: {DETECTED_COLOR}")
    return DETECTED_COLOR

def get_both_sensor_color():
    global stop_sequence
    DETECTED_COLOR_LEFT = None
    DETECTED_COLOR_RIGHT = None
    right_color_array = []
    left_color_array = []
    while DETECTED_COLOR_LEFT is None and DETECTED_COLOR_RIGHT is None:
        while True:
            if is_detecting == False:
                collect_color_sensor_data(left_color_array,right_color_array)
                DETECTED_COLOR_LEFT = color_matching_left(left_color_array)
                DETECTED_COLOR_RIGHT = color_matching(right_color_array)
                map_color_data["color_left"] = DETECTED_COLOR_LEFT
                map_color_data["color_right"] = DETECTED_COLOR_RIGHT
                
                if DETECTED_COLOR_LEFT == "water" or DETECTED_COLOR_RIGHT == "water":
                    stop_sequence = True
                time.sleep(0.5)
            else:
                print("pausing color")
                time.sleep(0.5)

    
if __name__ == "__main__": 
    get_both_sensor_color()
