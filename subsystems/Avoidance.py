from utils.brick import Motor, EV3GyroSensor, wait_ready_sensors
from motor_settings import *
import threading

def avoid_block():
    gyro = EV3GyroSensor(1)
    
    gyro.reset_measure()
    #You can use the following code to get the current angle of the robot
    
    print("initial backup")
    #back up 5cm
    wheel_position(-600,-600,2)
    
    print("first rotate")
    #turn 90 degrees
    rotate(45,0.05)
    
    print("first forwards")
    #move forward 10cm
    wheel_position(200,200,1)
    
    print("second rotate")
    #turn 90 degrees back
    rotate_right(45,0.05)
    
    print("second forwards")
    #move forward 20cm
    wheel_position(1000,1000,1)
    
    print("third rotate")
    #turn 90 degrees
    rotate_right(90,0.05)
    
    print("third forward")
    #move forward 10cm
    wheel_position(200,200,1)
    
    print("last rotate")
    #turn back to initial position
    rotate(90,0.05)

if __name__ == "__main__":
    avoid_block()