from subsystems.utils import brick
from subsystems.motor_arm_settings import close_catcher, stop_sensor_arm, rotate_sensor_arm, rotate_initial_position_arm, arm_limits
import time

# orientation
motor_left = brick.Motor("C")
motor_right = brick.Motor("B")

# connect GyroSensor to port S1
gyro = brick.EV3GyroSensor(1)

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
    wheel_circumference = 12.56637
    tick = wheel_circumference / 360
    
    distance_p1 = p1 / tick
    distance_p2 = p2 / tick
    motor_left.set_position_relative(distance_p1)
    motor_right.set_position_relative(distance_p2)
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
    
    while(result > new_angle):
        wheel_position(-1.4,1.4,speed)
        current = gyro.get_abs_measure()
        
        # current == result
        while(current is None or current == 0):
            current = gyro.get_abs_measure()
        result = current
        time.sleep(0.1)

def rotate_right(angle, speed):  # speed: 0.01 = very fast, 0.25 = very slow
    #angle = -1*angle
    #if (angle < 0):
    #    angle = angle + 360
    gyro.reset_measure()
    #time.sleep(0.1)
    new_angle = 0
    result = gyro.get_abs_measure()
    while(result is None):
        result = gyro.get_abs_measure()
    new_angle = (result + angle)
    
    print(result)
    print(new_angle)
    
    while(result < new_angle):
        wheel_position(1.4,-1.4,speed)
        current = gyro.get_abs_measure()
        
        # current == result
        while(current is None or current == 0):
            current = gyro.get_abs_measure()
        result = current
        time.sleep(0.1)
    
def wheel_limits(p1,d1,p2,d2):
    motor_left.set_limits(power=p1, dps=d1)
    motor_right.set_limits(power=p2, dps=d2)
    
def catch_poop():
    wheel_position(10,10,3)

if __name__ == "__main__":
    # Prevents position control from going over either:
    # 50% power or 90 deg/sec, whichever is slower
    #wheels_reset()
    #arms_reset()
    wheel_limits(100,180,100,180)
    arm_limits(70,90,70,90)
    
    #wheel_position(-600,-600,4)
    rotate(90, 0.002)

