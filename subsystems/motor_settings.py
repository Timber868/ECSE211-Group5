from subsystems.utils import brick
from subsystems.motor_arm_settings import open_catcher, close_catcher, stop_sensor_arm, rotate_sensor_arm, rotate_initial_position_arm, arm_limits
import time

# orientation
motor_left = brick.Motor("C")
motor_right = brick.Motor("B")

# connect GyroSensor to port S1
gyro = brick.EV3GyroSensor(2)

# waits until every previously defined sensor is ready
brick.wait_ready_sensors()

gyro.set_mode('abs')

def wheels_reset():
    # Designates to Encoder, that the current physical position is 0 degrees
    motor_left.reset_encoder()
    motor_right.reset_encoder()

### Power ###
def power(power1,power2):
    motor_left.set_power(power1)# 100%
    motor_right.set_power(power2)# 100%

### Speed ###
def speed(speed1, speed2):
    # Forward -> speed = 90
    # Backward -> speed = -720
    # Stops -> speed = 0
    motor_left.set_dps(speed1) # 90 deg/sec
    motor_right.set_dps(speed2) # 90 deg/sec

def wheel_position(p1,p2,wait):
    motor_left.set_position_relative(p1)
    motor_right.set_position_relative(p2)
    # get motor speed here time.sleep(p1/motor_speed)
    time.sleep(wait)
    
def rotate(angle): 
    angle = angle - 7
    gyro.reset_measure()
    time.sleep(0.1)
    new_angle = 0
    result = gyro.get_abs_measure()
    while(result is None):
        result = gyro.get_abs_measure()
    print(result)
    new_angle = (result - angle)
    print(new_angle)
    print()
    while(result > new_angle):
        wheel_position(-20,20,0.075)
        current = gyro.get_abs_measure()
        
        # current == result
        while(current is None or (result != 0 and current == 0)):
            current = gyro.get_abs_measure()
        print(current)
        result = current

def rotate_right(angle):  
    angle = angle - 7
    gyro.reset_measure()
    time.sleep(0.1)
    new_angle = 0
    result = gyro.get_abs_measure()
    while(result is None):
        result = gyro.get_abs_measure()
    new_angle = (result + angle)
    
    print(result)
    print(new_angle)
    
    while(result < new_angle):
        wheel_position(20,-20,0.075)
        current = gyro.get_abs_measure()
        
        # current == result
        while(current is None or current == 0):
            current = gyro.get_abs_measure()
        print(current)
        result = current
        
def wheel_limits(p1,d1,p2,d2):
    motor_left.set_limits(power=p1, dps=d1)
    motor_right.set_limits(power=p2, dps=d2)
    
def catch_poop():
    wheel_position(-600,-600,4)
    rotate(170)
    open_catcher()  
    wheel_position(-350,-350,1)
    close_catcher()

def move_forward(dist, speed):
    wheel_position(dist, dist, speed)

def move_backward(dist, speed):
    wheel_position(-dist, -dist, speed)