#!/usr/bin/env python3

import time
from subsystems import motor_arm_settings, motor_settings, object_detection, color_sensor_start_stop    
from subsystems.utils.brick import reset_brick

if __name__ == "__main__":
    try:
        motor_settings.wheel_limits(100,180,100,180)
        motor_arm_settings.arm_limits(80,100,80,100)
        
        object_detection.detect_block(True, 90)

        #object_detection.sweep_and_move_to_next_grid()
    except KeyboardInterrupt:
        reset_brick()
        print("Robot was interrupted")

    
        
   
