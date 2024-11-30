#!/usr/bin/env python3

import time
from subsystems import Avoidance, motor_arm_settings, motor_settings, object_detection, color_sensor_start_stop    
from subsystems.utils.brick import reset_brick
from subsystems.utils.brick import EV3UltrasonicSensor, wait_ready_sensors, reset_brick
import threading

if __name__ == "__main__":
    try:
        
        motor_settings.wheel_limits(100,180,100,180)
        motor_arm_settings.arm_limits(80,100,80,100)
        
        #max_distance = object_detection.detect_wall_distance()
# #         
        #color_sensor_start_stop.get_both_sensor_color()
        #Avoidance.MoveDistFwd(-10, 200)
        #Avoidance.avoid_water()
#         while True:
#             color_left = color_sensor_start_stop.get_left_sensor_color()
#             time.sleep(0.1)
        #motor_settings.wheel_position(15,15,3)

        map_color_thread = threading.Thread(target = color_sensor_start_stop.get_both_sensor_color)
        map_color_thread.start()
        
                
        time.sleep(2)
            
        object_detection.DETECTED_BLOCKS = []
        #color_sensor_start_stop.get_left_sensor_color()
        #object_detection.sweep_and_align()
        #object_detection.a(40, 40)
        while True:
            if color_sensor_start_stop.map_color_data["color_left"] != "water" and color_sensor_start_stop.map_color_data["color_right"] != "water" and object_detection.detected == False:
                object_detection.a_gyro(30, 30)
                time.sleep(1)
            
            if color_sensor_start_stop.map_color_data["color_left"] == "water" or color_sensor_start_stop.map_color_data["color_right"] == "water":
                motor_settings.speed(0,0)
                motor_settings.power(0,0)
            
        
        #object_detection.detect_obstacles()
#         object_detection.deposit_blocks()
        #time.sleep(5)

        

        #object_detection.sweep_and_move_to_next_grid()
    except KeyboardInterrupt:
        reset_brick()
        print("Robot was interrupted")

    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        