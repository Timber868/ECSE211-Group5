from subsystems.utils import brick
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
    #gyro.reset_measure()
    #time.sleep(0.1)
    new_angle = 0
    result = gyro.get_abs_measure()
    while(result is None):
        result = gyro.get_abs_measure()
    new_angle = (result + angle)
    
    print(result)
    print(new_angle)
    
    wheel_limits(50,70,50,70)
            
    while(result < new_angle):
        wheel_position(0.7,-0.7,speed)
        current = gyro.get_abs_measure()
        
        # current == result
        while(current is None or current == 0):
            current = gyro.get_abs_measure()
        result = current
        time.sleep(0.1)


RW = 0.021  # Radius of wheel in cm
RB = 0.05   # Robot radius in m which is half the distance between the wheels
ORIENTTODEG = RB/RW

#function to turn without the help of the gyro sensor
def Turn(angle, speed):
    try:
        motor_left.set_limits(50 , speed)  # Set speed
        motor_right.set_limits(50 , speed)  # Set speed

        motor_right.set_position_relative(int(-angle * ORIENTTODEG))
        motor_left.set_position_relative(int(angle * ORIENTTODEG))
        motor_right.wait_is_stopped(0.01) # Wait for the motor to stop and checks every 0.1s
        #motor_left.wait_is_stopped(0.01)
        #time.sleep(0.1)
    except IOError as error:
        print(error)

DISTTODEG = 180 / (3.1416 * RW)  # Scale factor for distance
ORIENTTODEG = RB / RW            # Scale factor for rotation

#If no speed is specified it is set to 200
def MoveDistFwd(dist, speed = 200):
    try:
        motor_left.set_limits(50, speed)   # Set speed, same rotation
        motor_right.set_limits(50, speed)  # Set speed, same rotation
        motor_left.set_position_relative(int(dist * DISTTODEG / 100))   # Rotate wheels
        motor_right.set_position_relative(int(dist * DISTTODEG / 100))  # Rotate wheels
        motor_right.wait_is_stopped()  # Wait for the motor to stop and checks every 0.1s
        motor_left.wait_is_stopped()
    except IOError as error:
        print(error)

    
def wheel_limits(p1,d1,p2,d2):
    motor_left.set_limits(power=p1, dps=d1)
    motor_right.set_limits(power=p2, dps=d2)
    
def catch_poop():
    wheel_limits(100,180,100,180)
    wheel_position(15,15,3)

if __name__ == "__main__":
    # Prevents position control from going over either:
    # 50% power or 90 deg/sec, whichever is slower
    #wheels_reset()
    #arms_reset()
    wheel_limits(100,180,100,180)
    
    #wheel_position(-600,-600,4)
    rotate(90, 0.002)

