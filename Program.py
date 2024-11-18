#!/usr/bin/env python3

from utils.brick import Motor, EV3GyroSensor, wait_ready_sensors
import time
from motor_arm_settings import *
from motor_settings import *
from collect_us_sensor_data import *
from collect_color_sensor_data import *


if __name__ == "__main__":
    
    wheel_limits(100,180,100,180)
    arm_limits(70,90,70,90)

    detected_block = detect_block_and_move()
    
    wheel_limits(100,180,100,180)
    if detected_block:
        #detect color
        rotate_sensor_arm()
        
        #if is_yellow():
        rotate_initial_position_arm()
        catch_poop()
        #else:
            #stop_sensor_arm()
            #print("avoid obstacle")
    else:
        wheel_position(640,640,4)
