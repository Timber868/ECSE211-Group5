#!/usr/bin/env python3

from utils.brick import EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from motor_settings import *
from motor_arm_settings import *
from time import sleep
from math import sqrt
import threading

US_SENSOR = EV3UltrasonicSensor(3)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

def detect_block():
    detected = False
    gyro.reset_measure()
    new_angle = 0
    result = gyro.get_abs_measure()
    while(result is None):
        result = gyro.get_abs_measure()
    new_angle = result - 90
        
    while(result > new_angle):
        wheel_limits(40,70,40,70)
        wheel_position(-0.7,0.7,0.1)
        
        distance = US_SENSOR.get_value()
        if(distance <= 20 and distance > 0):
            detected = True
            move_and_catch(distance)
                
        current = gyro.get_abs_measure()
        while(current is None or current == result or current > result):
            current = gyro.get_abs_measure()
        result = current
        
        sleep(0.01)
        
    rotate_right(90)
    return detected

def move_and_catch(distance):
    wheel_limits(100,180,100,180)
    distance = distance - 1.5
    wheel_position(distance,distance,3)
    rotate_sensor_arm()

    #detect color
    catch_poop()
    rotate_initial_position_arm()
    move_to_initial_position(distance)

def move_to_initial_position(distance):
    #if is poop
    wheel_position(-(distance + 10),-(distance + 10),3)
    #else:
        #wheel_position(-distance,-distance,3)

def sweep():
    rotate(5)
    detect_block()
    
if __name__ == "__main__":
    detect_block()