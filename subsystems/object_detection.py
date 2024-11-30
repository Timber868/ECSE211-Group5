#!/usr/bin/env python3

from subsystems.utils.brick import EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from subsystems.motor_settings import *
from subsystems.motor_arm_settings import *
from time import sleep
import math
import threading

US_SENSOR = EV3UltrasonicSensor(3)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

DETECTED_BLOCKS = []

is_detecting = False

detected = False
detected_angle = 0
detected_distance = 0

def detect_block_gyro(is_near_wall, angle):
    gyro.reset_measure()

    new_angle = 0
    result = gyro.get_abs_measure()

    while(result is None):
        result = gyro.get_abs_measure()

    new_angle = (result - angle)

    detection_values = []
    angles = []
    
    while(result > new_angle):
        wheel_limits(50,50,50,50)
        wheel_position(-0.7,0.7,0.01)
        #current = gyro.get_abs_measure()
        distance = US_SENSOR.get_value()
        while distance == 0:
            distance = US_SENSOR.get_value()

        detection_values.append(distance)
        angles.append(result)
        time.sleep(0.0001)
        
        #print(distance)

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
        
    is_an_obstacle = is_obstacle(detection_values, angles)
    while is_an_obstacle:
        is_an_obstacle = is_obstacle(detection_values, angles)
    
    MIN = min(detection_values)
    index = detection_values.index(MIN)
    
    DETECTED_BLOCKS.append((MIN, angles[index]))
        
    return MIN

def is_obstacle(detection_values, angles):
    MIN = min(detection_values)
    print(detection_values)
    print(MIN)
    
    index = detection_values.index(MIN)
    block_detected = any(abs(d - MIN) < 2 or abs(a - angles[index]) < 5 for d, a in DETECTED_BLOCKS)

    if block_detected:
        detection_values.remove(MIN)
        del angles[index]
        return True
    
    return False
        
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
    
    return MIN

def sweep_and_align_gyro(MIN, init_angle, tolerance):
    gyro.reset_measure()

    new_angle = 0
    result = gyro.get_abs_measure()

    while(result is None):
        result = gyro.get_abs_measure()

    new_angle = (result + init_angle)
    
    current_dist = US_SENSOR.get_value()
    while current_dist == 0 or current_dist == MIN :
        current_dist = US_SENSOR.get_value()
    while(result < new_angle) and abs(current_dist - MIN ) > tolerance:
        
        wheel_limits(50,25,50,25)
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
            Turn(3, 70)
            time.sleep(0.15)
        else:
            break
               
        
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
    global is_detecting
    is_detecting = True
    detected = True
    distance_to_avoid = 0
    
    MIN = detect_block_gyro(False, angle)
    sweep_and_align_gyro(MIN, inital_angle, 1)
    
    is_detecting = False
    wheel_limits(100,180,100,180)
    wheel_position(MIN/2, MIN/2, 3)
    Turn(15, 70)
    time.sleep(0.5)
    
    is_detecting = True
    NEW_MIN = detect_block_gyro(False, 20)
    sweep_and_align_gyro(NEW_MIN, 20, 1)
#     time.sleep(3)

    move_and_catch(NEW_MIN -1, MIN - 1)
    detected = False
def move_and_catch(distance, init_dist):
    global is_detecting
    is_detecting = False
    wheel_limits(100,180,100,180)
    wheel_position(distance, distance, 2)
    is_poop = False
    
    from subsystems.color_sensor_start_stop import get_block_color
    is_detecting = True

    color_data = {"color": None}
    color_thread = threading.Thread(target = get_block_color, args=(color_data,))
    color_thread.start()
    
    time.sleep(0.5)
    
    i = 0
    while color_data["color"] is None and i <= 10:
        if i % 2 == 0:
            rotate_right(1, 0.1)
            time.sleep(0.1)
        else:
            rotate(1,0.1)
            time.sleep(0.1)
        i += 1
        
    color_thread.join()
    if color_data["color"] == "yellow" or color_data["color"] == "orange":
        rotate_sensor_arm()
        is_poop = True
        catch_poop()
    else:
        print("avoid")
    
    rotate_initial_position_arm()
    is_detecting = False
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

