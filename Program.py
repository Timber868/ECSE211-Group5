#!/usr/bin/env python3

import time
from subsystems import motor_arm_settings, motor_settings, object_detection, collect_color_sensor_data


if __name__ == "__main__":
    
    motor_settings.wheel_limits(100,180,100,180)
    motor_arm_settings.arm_limits(70,90,70,90)
   
    object_detection.detect_block()
    #move to next grid
    motor_settings.wheel_position(30,30,3)
        
   
