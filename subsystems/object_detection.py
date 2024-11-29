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

#DETECTED_BLOCKS = []

angle_to_rotate_back = None
is_left = False
is_right = False

def detect_block_gyro(is_near_wall, angle, init_angle):
    gyro.reset_measure()

    new_angle = 0
    result = gyro.get_abs_measure()

    while(result is None):
        result = gyro.get_abs_measure()

    new_angle = (result - angle)
    
    detected = False
    max_distance_to_detect = 0
    current_angle = 0
    detection_values = []
    
    while(result > new_angle):
        wheel_limits(50,30,50,30)
        wheel_position(-0.7,0.7,0.01)
        #current = gyro.get_abs_measure()
        distance = US_SENSOR.get_value()
        while distance == 0:
            distance = US_SENSOR.get_value()

        detection_values.append(distance)
        time.sleep(0.0001)
        
        #print(distance)
        #block_detected = any(abs(d - distance) < 2 or abs(a - i) < 5 for d, a in DETECTED_BLOCKS)

        if is_near_wall:
            max_distance_to_detect = detect_wall_distance()
        else:
            max_distance_to_detect = 15
            
        print(result)
        current = gyro.get_abs_measure()
        while(current is None or current == 0):
            current = gyro.get_abs_measure()
        result = current
        time.sleep(0.0001)
        
    MIN = min(detection_values)
    print(detection_values)
    print(MIN)
        
    return MIN

def detect_block(is_near_wall, angle, initial_angle_pos):
    
    detected = False
    max_distance_to_detect = 0
    current_angle = 0
    detection_values = []
    for i in range(0,angle):
        Turn(-3, 70)
        time.sleep(0.05)
        
        distance = US_SENSOR.get_value()
        while distance == 0:
            distance = US_SENSOR.get_value()

        detection_values.append(distance)
        
        #print(distance)
        #block_detected = any(abs(d - distance) < 2 or abs(a - i) < 5 for d, a in DETECTED_BLOCKS)

        if is_near_wall:
            max_distance_to_detect = detect_wall_distance()
        else:
            max_distance_to_detect = 15

    MIN = min(detection_values)
    print(detection_values)
    print(MIN)
#     if block_detected == False:
#             if(distance <= max_distance_to_detect and distance > 0):
#                 detected = True
#                 wheel_limits(100,180,100,180)
#                 wheel_position(distance-5,distance-5,2)
#                                 
#                 DETECTED_BLOCKS.append((distance, current_angle))
# 
#                 rest_distance = sweep_and_align(MIN)
#                 
#                 if rest_distance != 0:
#                     wheel_position(rest_distance, rest_distance, 1)
#                 move_and_catch(distance + rest_distance)
#                 
#                 if is_right:
#                     Turn(-angle_to_rotate_back, 70)
#                 elif is_left:
#                     Turn(angle_to_rotate_back, 70)
    return MIN

def sweep_and_align_gyro(MIN, init_angle, tolerance):
    gyro.reset_measure()

    new_angle = 0
    result = gyro.get_abs_measure()

    while(result is None):
        result = gyro.get_abs_measure()

    new_angle = (result + init_angle)
    
    detected = False
    max_distance_to_detect = 0
    current_angle = 0
    detection_values = []
    
    current_dist = US_SENSOR.get_value()
    while current_dist == 0 or current_dist == MIN :
        current_dist = US_SENSOR.get_value()
    while(result < new_angle) and abs(current_dist - MIN ) > tolerance:
        
        wheel_limits(50,15,50,15)
        wheel_position(0.7,-0.7,0.01)
        
        current = gyro.get_abs_measure()
        while(current is None or current == 0):
            current = gyro.get_abs_measure()
        result = current
        time.sleep(0.0001)
        current_dist = US_SENSOR.get_value()
        while current_dist == 0 or current_dist == MIN :
            current_dist = US_SENSOR.get_value()
        print(abs(current_dist - MIN ) )
    print(f"aa: {US_SENSOR.get_value()}")


def sweep_and_align(MIN, angle,tolerance):
#     is_left = False
#     is_right = False
#     final_distance = None
    
#     i = 0
#     while i < 5:
#         Turn(5, 70)
#         distance = US_SENSOR.get_value()
#         print(distance)
#         if 0 <= distance < min_distance or distance == 255:
#             print("rotated left")
#             is_left = True
#             if distance >= 3:
#                 final_distance = distance -3
#             break
# 
#         i = i+1
            

    #if is_left == False:
    for i in range(0,angle):
        current_dist = US_SENSOR.get_value()
        print(abs(current_dist - MIN ))
        if abs(current_dist - MIN ) > tolerance:
            print("rotated right")
            is_right = True
            Turn(3, 70)
            time.sleep(0.15)
#             if distance >= 3:
#                 final_distance = distance -3
        else:
#             Turn(5, 70)
#             time.sleep(0.1)
#             temp = US_SENSOR.get_value()
#             if(temp > current_dist):
#                 Turn(-4, 70)
#                 time.sleep(0.1)
            break
               
        


        #i = i+1
            
#     current_angle = gyro.get_abs_measure()
#     angle_to_rotate_back = current_angle - initial_angle
#     print("angle to rotate back")
#     print(angle_to_rotate_back)

    #if is_right:
        #Turn(angle_to_rotate_back, 70)
    #elif is_left:
        #Turn(angle_to_rotate_back, 70)

    #print(f"Aligned to block at angle: {angle_to_rotate_back} at {final_distance}")
        
#     if final_distance is not None:
#         return final_distance
#     else:
#         return 0
def a(angle,inital_angle):
    MIN = detect_block(False, angle, inital_angle)
    tolerance = 0
    if MIN <= 15:
        tolerance = 1
    else:
        tolerance = 2
    sweep_and_align(MIN, inital_angle, tolerance)
    wheel_limits(100,180,100,180)
    wheel_position(MIN/2, MIN/2, 4)
    time.sleep(1)
    Turn(15, 70)
    time.sleep(1)
    NEW_MIN = detect_block(False, 20,20)
    sweep_and_align(NEW_MIN, 20, 0.5)
    move_and_catch(NEW_MIN -1.5, MIN - 1.5)
    
def a_gyro(angle,inital_angle):
    MIN = detect_block_gyro(False, angle, inital_angle)
    tolerance = 0
    if MIN <= 15:
        tolerance = 1
    else:
        tolerance = 2
    sweep_and_align_gyro(MIN, inital_angle, 1)
    wheel_limits(100,180,100,180)
    wheel_position(MIN/2, MIN/2, 3)
    Turn(15, 70)
    time.sleep(1)
    NEW_MIN = detect_block_gyro(False, 20,20)
    sweep_and_align_gyro(NEW_MIN, 20, 1)
#     time.sleep(3)
    move_and_catch(NEW_MIN -2, MIN - 2)
    
def move_and_catch(distance, init_dist):
    wheel_limits(100,180,100,180)
    wheel_position(distance, distance, 3)
    is_poop = False
    rotate_sensor_arm()
    color = get_left_sensor_color()
    if color == "yellow" or color == "orange" or color == "red":
        is_poop = True
        catch_poop()
    else:
        print("avoid")
    rotate_initial_position_arm()
    move_to_initial_position(init_dist, is_poop)

    
def move_to_initial_position(distance, is_poop):
    wheel_limits(100,180,100,180)
    if is_poop:
        wheel_position(-(distance + 15), -(distance + 15), 3)
    else:
        wheel_position(-distance,-distance,3)

def detect_obstacles():
    is_obstacle = False
    detect_blocks(False, 40, 35)
        
    if is_obstacle:
        avoid_block_left()
    else:
        wheel_position(5,5,3)

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

