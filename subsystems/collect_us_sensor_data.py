#!/usr/bin/env python3

from subsystems.utils.brick import EV3ColorSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from subsystems.motor_settings import *
from subsystems.collect_color_sensor_data import collect_color_sensor_data
from time import sleep
from math import sqrt
import threading


US_SENSOR = EV3UltrasonicSensor(3)
COLOR_SENSOR_LEFT = EV3ColorSensor(4)
COLOR_SENSOR_LEFT = EV3ColorSensor(2)

COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"



wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

def collect_color_sensor_data(left_color_array, right_color_array):
    "Collect color sensor data."
    try:
        i = 0
        # output_file = open(COLOR_SENSOR_DATA_FILE, "w")
        while i<4:
                left_colors = COLOR_SENSOR_LEFT.get_rgb() #Hungarian notation, array of [R, G, B] colors
                right_colors = COLOR_SENSOR_RIGHT.get_rgb()
                # sColors = str(aColors[0]) + "," + str(aColors[1]) + "," + str(aColors[2])
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

def detect_block():
    detected = False
    distance = 0
    
    gyro.reset_measure()
    new_angle = 0
    result = gyro.get_abs_measure()
    while(result is None):
        result = gyro.get_abs_measure()
    new_angle = result-90
    
    wheel_limits(50,80,50,80)
    
    while(result > new_angle and detected == False):
        wheel_position(-20,20,0.1)
        
        distance = US_SENSOR.get_value()
        if(distance <= 20 and distance > 0):
            detected = True
            print(distance)
            break
        current = gyro.get_abs_measure()
            
        while(current is None or current == result or current > result):
            current = gyro.get_abs_measure()
        result = current
        
        sleep(0.01)
    if detected:
        return distance
    else:
        return None       

def detect_block_and_move():

    distance = detect_block()
    
    if distance is not None:
        print(distance)
        
        circumference = 12.56637
        tick = circumference / 360
        distance = (distance-1.5) / tick
        print(distance)
        wheel_limits(100,180,100,180)
        wheel_position(distance,distance,3)
        return True
    
    return False