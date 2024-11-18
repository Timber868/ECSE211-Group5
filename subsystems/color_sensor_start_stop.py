#!/usr/bin/env python3

from subsystems.utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, Motor
from ast import literal_eval
import time
from subsystems.collect_color_sensor_data import collect_color_sensor_data
from math import sqrt
from subsystems.motor_arm_settings import get_arm_state

# INITIALIZING OBJECTS

# REFER TO note_deciding.py FOR PORTS
COLOR_SENSOR_LEFT = EV3ColorSensor(4)
COLOR_SENSOR_RIGHT = EV3ColorSensor(2)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


# CONSTANTS
GREEN_R, GREEN_G, GREEN_B = 0.150, 0.706, 0.145                 # GREEN tested normalized RGB values
YELLOW_R, YELLOW_G, YELLOW_B = 0.516, 0.447, 0.037              # YELLOW tested normalized RGB values
RED_R, RED_G, RED_B = 0.690, 0.205, 0.105                       # RED tested normalized RGB values
ORANGE_R, ORANGE_G, ORANGE_B = 0,0,0                            # ORANGE tested normalized RGB values
BLUE_R, BLUE_G, BLUE_B =  0,0,0                                 # BLUE tested normalized RGB values

# START OF PROGRAM

red_measured, green_measured, blue_measured = 0, 0, 0           # initializing the measured colors' values\
left_color_array =[]
right_color_array=[]

def get_normalized_RGB_from_csv(i):
    a_array = []
    if i == "left":
        a_array = left_color_array
    else:
        a_array = right_color_array
        
    red_measured, green_measured, blue_measured = 0, 0, 0      # reset (because of infinite while loop)

    n_lines = 0                                                 # track number of lines (measurements) to compute mean
    collect_color_sensor_data(left_color_array,right_color_array)
    for colors in a_array:
        r, g, b = colors  # convert string to 3 floats
        if r != None and g != None and b != None:
            red_measured += r
            green_measured += g
            blue_measured += b
        n_lines = n_lines + 1
        
        red_measured_avg = red_measured / n_lines
        green_measured_avg = green_measured / n_lines
        blue_measured_avg = blue_measured / n_lines 

        print(f"red_measured_avg: {red_measured_avg}, green_measured_avg: {green_measured_avg}, blue_measured_avg: {blue_measured_avg}")
        denominator = red_measured_avg + green_measured_avg + blue_measured_avg
        
        if denominator != 0:
            red_measured = red_measured_avg / denominator
            green_measured = green_measured_avg / denominator
            blue_measured = blue_measured_avg / denominator
        else:
            red_measured = 0
            green_measured = 0
            blue_measured = 0

    return(red_measured, green_measured, blue_measured, red_measured_avg, green_measured_avg, blue_measured_avg)

match_colors = {}                                               # initializing the colors dict for color matching
def color_matching(i):
    DETECTED_COLOR = None

    r_measured, g_measured, b_measured, r_avg, g_avg, b_avg =  get_normalized_RGB_from_csv(i)

    match_colors["green_euclid_dist"] = sqrt(( r_measured - GREEN_R )**2 + ( g_measured - GREEN_G)**2 + ( b_measured - GREEN_B )**2 )
    match_colors["yellow_euclid_dist"] = sqrt(( r_measured - YELLOW_R )**2 + ( g_measured - YELLOW_G)**2 + ( b_measured - YELLOW_B )**2 )
    match_colors["red_euclid_dist"] = sqrt(( r_measured - RED_R )**2 + ( g_measured - RED_G )**2 + ( b_measured - RED_B )**2 )
    match_colors["blue_euclid_dist"] = sqrt(( r_measured - BLUE_R )**2 + ( g_measured - BLUE_G )**2 + ( b_measured - BLUE_B )**2 )
    match_colors["orange_euclid_dist"] = sqrt(( r_measured - ORANGE_R )**2 + ( g_measured - ORANGE_G )**2 + ( b_measured - ORANGE_B )**2 )
    
    min_dist = 100
    min_color = None
    for key in match_colors:
        if match_colors[key] < min_dist:
            min_dist = match_colors[key]
            min_color = key
    
    if min_dist < 0.2 and (r_avg>=10 or g_avg>=10 or b_avg>=10): #ensures that color sensor is detecting colours that aren't blank
        if min_color == "green_euclid_dist":
            DETECTED_COLOR = "green"
        elif min_color == "yellow_euclid_dist":
            DETECTED_COLOR = "yellow"
        elif min_color == "red_euclid_dist":
            DETECTED_COLOR = "red"
        elif min_color == "orange_euclid_dist":
            DETECTED_COLOR = "orange"
        elif min_color == "blue_euclid_dist":
            DETECTED_COLOR = "blue"
        else:
            print("COLOR DETECTION ERROR")        
    
    if DETECTED_COLOR == None:
        print("COLOR WAS NOT CLOSE ENOUGH TO REFERENCE COLORS")
    
    return DETECTED_COLOR

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

def get_left_sensor_color():
    DETECTED_COLOR = None
    i = 0
    while DETECTED_COLOR == None and i < 5:
        print("BEFORE COLLECTING DATA")
        collect_color_sensor_data(left_color_array,right_color_array)
        print("COLLECTED COLOR DATA")
        DETECTED_COLOR = color_matching("left")

        if DETECTED_COLOR is not None:
            print(f"DETECTED_COLOR: {DETECTED_COLOR}")
            return DETECTED_COLOR
        
        time.sleep(0.1) # wait for the color sensor to detect the color
        i += 1 # increment the counter


if __name__ == "__main__": 
    get_left_sensor_color()
