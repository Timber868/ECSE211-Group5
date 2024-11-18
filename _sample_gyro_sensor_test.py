#!/usr/bin/env python3

# Test for gyro senor


from utils.brick import EV3GyroSensor, wait_ready_sensors
import time

# connect GyroSensor to port S1
gyro = EV3GyroSensor(1)

# waits until every previously defined sensor is ready
wait_ready_sensors()

gyro.set_mode('abs')

i = 0

while(i<10):
    print(f"iteration {i}:")
    # reset gyro sensor
    gyro.reset_measure()
    
    time.sleep(5)
    
    # read gyro sensor result
    result = gyro.get_abs_measure()
    print(f"the abs value is {result}.")
          
    i = i+1