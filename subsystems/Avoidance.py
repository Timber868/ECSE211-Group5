from subsystems.utils import brick
from subsystems.utils.brick import *
from subsystems.motor_settings import Turn, speed, wheel_limits
from subsystems.color_sensor_start_stop import get_left_sensor_color, get_right_sensor_color

import threading
import time

stop_event = threading.Event()

# orientation
motor_left = Motor("C")
motor_right = Motor("B")

# Parameters:
RW = 0.021  # Radius of wheel in cm
RB = 0.05   # Robot radius in m which is half the distance between the wheels
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


#Calculated values:
#For 10cm wait 1.5s
#For 20cm, wait 3s
#For 40cm wait 6s


def avoid_block_left(): 
    speed(200)
    wheel_limits(50, 80, 50, 80)

    #Back up 1
    print("initial backup")
    MoveDistFwd(-5, 200)
    time.sleep(0.5)
 
    print("rotate 1")
    #turn 1
    Turn(-45, 200)
    time.sleep(1)
    
    MoveDistFwd(20,200)
    time.sleep(4)
    
    Turn(30, 200)
    time.sleep(1)
    
    MoveDistFwd(10, 200)
    time.sleep(2)
    
    Turn(45, 200)
    time.sleep(1)
    
    MoveDistFwd(10, 200)
    time.sleep(1.5)
    
    print("big turn")
    Turn(-95, 200)
    time.sleep(2)
    
    MoveDistFwd(-10, 200)
    time.sleep(1.5)
    
    Turn(25, 200)
    time.sleep(1)
    
def avoid_water():
    gyro = brick.EV3GyroSensor(2)

    # waits until gyro sensor is ready
    brick.wait_ready_sensors()
    gyro.set_mode('abs')
    
    color_left = get_left_sensor_color()
    color_right = get_right_sensor_color()
    print("Left: ", color_left)
    print("Right: ", color_right)

    while color_left == "water" and color_right == "water":
        print("Both sensors detected water")
        #Back up until youre out of water
        MoveDistFwd(-5, 200)
        time.sleep(0.75)

        color_left = get_left_sensor_color()
        color_right = get_right_sensor_color()

    if color_left == "water":
        print("Left sensor detected water")
        #Back up until youre out of water
        Turn(25, 200)
        time.sleep(4)
        MoveDistFwd(-5, 200)
        time.sleep(0.75)

        #Use the gyro sensor to measure and see once we are on the other side of the water
        gyro.reset_measure()
        result = gyro.get_abs_measure()
        
        if result < 180:    
            target = 360 - result * 2
        else:
            target = result * 2 - 360

        while gyro.get_abs_measure() != target:
            #Back up and turn until the sensor is out of the water
            while get_left_sensor_color() == "water":
                Turn(5, 200)
                time.sleep(0.75)
                
                MoveDistFwd(-5, 200)
                time.sleep(0.75)

            #Keep on moving until our sensor is back in the water
            while get_left_sensor_color() != "water":
                MoveDistFwd(5, 200)
                time.sleep(0.75)

                Turn(-10, 200)
                time.sleep(0.75)

            #Rotate a bit out of the water
            Turn(10, 200)

    
    if color_right == "water":
        print("Right sensor detected water")
        #Back up until youre out of water
        Turn(-25, 200)
        time.sleep(4)
        MoveDistFwd(-5, 200)
        time.sleep(0.75)
        
        if result < 180:    
            target = 360 - result * 2
        else:
            target = result * 2 - 360

        while gyro.get_abs_measure() != target:
            #Back up and turn until the sensor is out of the water
            while get_right_sensor_color() == "water":
                Turn(-5, 200)
                time.sleep(0.75)
                
                MoveDistFwd(5, 200)
                time.sleep(0.75)

            #Keep on moving until our sensor is back in the water
            while get_right_sensor_color() != "water":
                MoveDistFwd(5, 200)
                time.sleep(0.75)

                Turn(10, 200)
                time.sleep(0.75)

            #Rotate a bit out of the water
            Turn(-10, 200)


# Create the thread
# thread = threading.Thread(target=detect_color)