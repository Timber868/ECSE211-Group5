#!/usr/bin/env python3

import time
from subsystems import motor_arm_settings, motor_settings, collect_us_sensor_data, collect_color_sensor_data
from subsystems.utils.brick import reset_brick


if __name__ == "__main__":
    try:
        motor_settings.wheel_limits(100,180,100,180)
        motor_arm_settings.arm_limits(70,90,70,90)

        detected_block = collect_us_sensor_data.detect_block_and_move()
        
        motor_settings.wheel_limits(100,180,100,180)
        if detected_block:
            #detect color
            motor_arm_settings.rotate_sensor_arm()
            
            #if is_yellow():
            motor_arm_settings.rotate_initial_position_arm()
            motor_settings.catch_poop()
            #else:
                #stop_sensor_arm()
                #print("avoid obstacle")
        else:
            motor_settings.wheel_position(640,640,4)
    except KeyboardInterrupt:
        reset_brick()
        print("Robot was interrupted")
    
    
