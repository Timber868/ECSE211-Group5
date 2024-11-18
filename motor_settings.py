from utils.brick import Motor, EV3GyroSensor, wait_ready_sensors
from motor_arm_settings import *
import time

# orientation
motor_left = Motor("C")
motor_right = Motor("B")

# connect GyroSensor to port S1
gyro = EV3GyroSensor(1)

# waits until every previously defined sensor is ready
wait_ready_sensors()

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
    
def rotate(angle, speed):  # speed: 0.01 = very fast, 0.25 = very slow
    #angle = -1*angle
    #if (angle < 0):
    #    angle = angle + 360
    gyro.reset_measure()
    #time.sleep(0.1)
    new_angle = 0
    result = gyro.get_abs_measure()
    while(result is None):
        result = gyro.get_abs_measure()
    new_angle = (result - angle)
    
    print(f"result: {result}")
    print("\n\n")
    print(f"new angle: {new_angle}")
    print("\n\n")
    while(result > new_angle):
        wheel_position(-40,40,speed)
        current = gyro.get_abs_measure()
        
        # current == result
        while(current is None or current == 0):
            print(1)
            current = gyro.get_abs_measure()
        print(f"current: {current}")
        result = current
        time.sleep(0.1)
    
def wheel_limits(p1,d1,p2,d2):
    motor_left.set_limits(power=p1, dps=d1)
    motor_right.set_limits(power=p2, dps=d2)
    
def catch_poop():
    wheel_position(-600,-600,4)
    rotate(170)
    open_catcher()  
    wheel_position(-350,-350,1)
    close_catcher()

if __name__ == "__main__":
    # Prevents position control from going over either:
    # 50% power or 90 deg/sec, whichever is slower
    #wheels_reset()
    #arms_reset()
    wheel_limits(100,180,100,180)
    arm_limits(70,90,70,90)
    
    #wheel_position(-600,-600,4)
    rotate(90, 0.002)
# #     
# #     stop_catcher()
# 
# #     power(0,0)
#     rotate_sensor_arm()
#     rotate_initial_position_arm()
#     stop_sensor_arm()
#     
#     wheel_position(-640,-640,4)
#     rotate(170)
#     open_catcher()  
#     wheel_position(-350,-350,1)
#     close_catcher()
#     
#     
# #     t_move()
#     rotate("left")
