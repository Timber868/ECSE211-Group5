#!/usr/bin/env python3

from utils import sound
from utils.brick import EV3ColorSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from time import sleep
from motor_settings import *
from collect_color_sensor_data import collect_color_sensor_data
from math import sqrt
import threading


US_SENSOR = EV3UltrasonicSensor(3)
COLOR_SENSOR_LEFT = EV3ColorSensor(4)
COLOR_SENSOR_LEFT = EV3ColorSensor(2)

COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"



wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

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

def detect_water():
    
        
if __name__ == "__main__":
    detect_block_and_move()
    

