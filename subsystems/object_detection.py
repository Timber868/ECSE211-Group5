#!/usr/bin/env python3

from utils.brick import EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from motor_settings import *
from motor_arm_settings import *
from Avoidance import *
from color_sensor_start_stop import *
from time import sleep
from math import sqrt
import threading

US_SENSOR = EV3UltrasonicSensor(3)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

DETECTED_BLOCKS = []

def detect_block(is_detecting_grid, angle):
    detected = False

    new_angle = 0
    current_angle = gyro.get_abs_measure()
    while(current_angle is None):
        current_angle = gyro.get_abs_measure()
    new_angle = current_angle - angle
    

    while(current_angle > new_angle):
        wheel_limits(60,80,60,80)
        wheel_position(-0.7,0.7,0.1)
        
        distance = US_SENSOR.get_value()
        print(distance)
        block_detected = any(abs(d - distance) < 2 or abs(a - current_angle) < 2 for d, a in DETECTED_BLOCKS)

        if block_detected == False:
            if(distance <= 25 and distance > 0):
                print("detected")
                wheel_limits(100,180,100,180)
                wheel_position(distance -5,distance-5,3)
                                
                if is_detecting_grid:
                    DETECTED_BLOCKS.append((distance, current_angle))

                    rest_distance = sweep_and_align()
                    wheel_limits(100,180,100,180)
                    if rest_distance is not None:
                        wheel_position(rest_distance,rest_distance,1)
                    else:
                        wheel_position(3,3,1)

                    move_and_catch(distance)
                print("break")
                detected = True
                if not is_detecting_grid:
                    break
                    
            current = gyro.get_abs_measure()
            while(current is None):
                current = gyro.get_abs_measure()
            current_angle = current
            print(current_angle)
            print(new_angle)
        
    rotate_right(80, 0.01)
    return detected

def sweep_and_align():
    is_left = False
    is_right = False
    min_distance = 6
    final_distance = None
    
    wheel_limits(50,70,50,70)
            
    current_angle = gyro.get_abs_measure()
    while(current_angle is None):
        current_angle = gyro.get_abs_measure()
        
    new_angle = current_angle - 2
    while current_angle > new_angle:
        distance = US_SENSOR.get_value()
        
        if 0 <= distance < min_distance:
            is_left = True
            final_distance = distance
            break
        
        wheel_position(-0.5, 0.5, 0.1)  # Sweep left

        current = gyro.get_abs_measure()
        while(current is None or current == 0):
            current = gyro.get_abs_measure()
        current_angle = current
    
    if is_left ==  False:  
        current_angle = gyro.get_abs_measure()
        new_angle = current_angle + 4
        while current_angle < new_angle:
            distance = US_SENSOR.get_value()

            if 0 <= distance < min_distance:
                final_distance = distance
                is_right = True
                break

            wheel_position(0.5, -0.5, 0.1)  # Sweep right
            current = gyro.get_abs_measure()
            while(current is None or current == 0):
                current = gyro.get_abs_measure()
            current_angle = current
    
    if is_left == False and is_right == False:
        rotate(2, 0.2)

    print(f"Aligned to block at angle: {distance}")
        
    if final_distance is not None:
        return final_distance
    else:
        return None

    
def move_and_catch(distance):
    is_poop = False
    rotate_sensor_arm()
    color = get_left_sensor_color()
    if color == "yellow" or color == "orange":
        is_poop = True
        catch_poop()
    else:
        print("avoid")
    rotate_initial_position_arm()
    move_to_initial_position(distance, is_poop)
    
def move_to_initial_position(distance, is_poop):
    if is_poop:
        wheel_position(-(distance + 10), -(distance + 10), 3)
    else:
        wheel_position(-distance,-distance,3)

def sweep_and_move_to_next_grid():
    is_obstacle = detect_block(False, 5)
    if is_obstacle:
        avoid_block()
    else: 
        #move to next grid
        wheel_position(30,30,3)


if __name__ == "__main__":
    detect_block()