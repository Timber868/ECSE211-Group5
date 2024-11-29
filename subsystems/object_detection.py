#!/usr/bin/env python3

from subsystems.utils.brick import EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from subsystems.motor_settings import *
from subsystems.motor_arm_settings import *
from subsystems.Avoidance import *
from subsystems.color_sensor_start_stop import *
from time import sleep
import math
import threading

US_SENSOR = EV3UltrasonicSensor(3)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

DETECTED_BLOCKS = []

angle_to_rotate_back = None
is_left = False
is_right = False

def detect_block(is_near_wall):
    detected = False
    max_distance_to_detect = 0
    current_angle = 0
    for i in range(0,45):
        Turn(-5, 90)
        
        current_angle = current_angle + 5
        distance = US_SENSOR.get_value()
        print(distance)
        block_detected = any(abs(d - distance) < 2 or abs(a - current_angle) < 5 for d, a in DETECTED_BLOCKS)

        if is_near_wall:
            max_distance_to_detect = detect_wall_distance()
        else:
            max_distance_to_detect = 25

        if block_detected == False:
            if(distance <= max_distance_to_detect and distance > 0):
                detected = True
                wheel_limits(100,180,100,180)
                wheel_position(distance-3,distance-3,2)
                                
                DETECTED_BLOCKS.append((distance, current_angle))

                sweep_and_align()

                move_and_catch(distance)
                
                if is_right:
                    Turn(-angle_to_rotate_back, 70)
                elif is_left:
                    Turn(angle_to_rotate_back, 70)


    Turn(90, 80)
    return detected

def sweep_and_align():
    is_left = False
    is_right = False
    min_distance = 6
    final_distance = None

    initial_angle = gyro.get_abs_measure()
    
    i = 0
    while i < 5:
        Turn(-5, 70)
        distance = US_SENSOR.get_value()
        print(distance)
        if 0 <= distance < min_distance:
            print("rotated left")
            is_left = True
            final_distance = distance
            break

        i = i+1
            

    if is_left == False:
        i=0
        while i < 10:
            Turn(5, 70)
            distance = US_SENSOR.get_value()
            print(distance)

            if 0 <= distance < min_distance:
                print("rotated right")
                is_right = True
                final_distance = distance
                break

            i = i+1
            
    current_angle = gyro.get_abs_measure()
    angle_to_rotate_back = current_angle - initial_angle
    print("angle to rotate back")
    print(angle_to_rotate_back)

    #if is_right:
        #Turn(angle_to_rotate_back, 70)
    #elif is_left:
        #Turn(angle_to_rotate_back, 70)

    #print(f"Aligned to block at angle: {angle_to_rotate_back} at {final_distance}")
        
    if final_distance is not None:
        return final_distance
    else:
        return None

def move_and_catch(distance):
    is_poop = False
    rotate_sensor_arm()
    color = get_left_sensor_color()
    if color == "yellow" or color == "orange" or color == "red":
        is_poop = True
        catch_poop()
    else:
        print("avoid")
    rotate_initial_position_arm()
    move_to_initial_position(distance, is_poop)

    
def move_to_initial_position(distance, is_poop):
    wheel_limits(100,180,100,180)
    if is_poop:
        wheel_position(-(distance + 10), -(distance + 10), 3)
    else:
        wheel_position(-distance +3,-distance+3,3)

def detect_obstacles():
    is_obstacle = False
    for i in range(0,5):
        Turn(-10, 90)
        distance = US_SENSOR.get_value()
        print(distance)

        if(distance <= 25 and distance > 0):
            is_obstacle = True
            wheel_limits(100,180,100,180)
            wheel_position(distance-3,distance-3,3)

            rest_distance = sweep_and_align()
            if rest_distance is not None:
                wheel_limits(100,180,100,180)
                wheel_position(rest_distance-1,rest_distance-1,1)
        
    if is_obstacle:
        avoid_block()

    return is_obstacle

def detect_wall_distance():
    rotate_sensor_arm()
    distance = US_SENSOR.get_value()
    rotate_initial_position_arm()

    return distance

def detect_at_angle():
    Turn(20,100)
    wheel_position(10,10,2)

def deposit_blocks():
    rotate_sensor_arm()
    wheel_position(-25,-25,3)
    rotate_initial_position_arm()


if __name__ == "__main__":
    detect_block()

