from subsystems.utils.brick import *
from subsystems.motor_settings import Turn
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
    color_left = get_left_sensor_color()
    color_right = get_right_sensor_color()
    print("Left: ", color_left)
    print("Right: ", color_right)

    while color_left == "water" and color_right == "water":
        print("Both sensors detected water")
        #Back up until youre out of water
        MoveDistFwd(-5, 200)
        time.sleep(1)

        color_left = get_left_sensor_color()
        color_right = get_right_sensor_color()

    if color_left == "water":
        print("Left sensor detected water")
        #Back up until youre out of water
        Turn(25, 200)
        MoveDistFwd(-5, 200)
        time.sleep(1)
        
        while get_right_sensor_color() != "water":
            Turn

        #Turn right away from the water
        Turn(45, 200)
        time.sleep(1)

        #Move forward
        MoveDistFwd(10, 200)
        time.sleep(1.5)
    
    if color_right == "water":
        print("Right sensor detected water")
        #Back up until youre out of water
        Turn(25, 200)
        MoveDistFwd(-5, 200)
        time.sleep(1)
        
        time.sleep(5)

        #Turn left away from the water
        Turn(50, 200)
        time.sleep(1)

        #Move forward
        MoveDistFwd(10, 200)
        time.sleep(1.5)


# Create the thread
# thread = threading.Thread(target=detect_color)