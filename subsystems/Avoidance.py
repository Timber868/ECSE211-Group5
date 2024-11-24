from subsystems.utils.brick import *
from subsystems.motor_settings import rotate, rotate_right, wheel_limits, wheel_position, power, speed
import threading
import time

stop_event = threading.Event()

# orientation
motor_left = Motor("C")
motor_right = Motor("B")


RW = 0.055  # Radius of wheel in cm
RB = 0.115  # Robot radius in m which is half the distance between the wheels
ORIENTTODEG = RB/RW

def Rotate(BP, angle, speed):
    try:
        BP.set_motor_limits(motor_left, 50, speed)  # Set speed
        BP.set_motor_limits(motor_right, 50, speed)  # Set speed
        BP.set_motor_position_relative(motor_left, int(angle * ORIENTTODEG))  # Rotate L wheel +ve
        BP.set_motor_position_relative(motor_right, int(-angle * ORIENTTODEG))  # Rotate R wheel -ve
        motor_right.wait_is_stopped(0.1) # Wait for the motor to stop and checks every 0.1s
    except IOError as error:
        print(error)


def detect_color():
    COLOR_SENSOR_LEFT = EV3ColorSensor(4)
    COLOR_SENSOR_RIGHT = EV3ColorSensor(2)

    while not stop_event.is_set():
#         color_left = COLOR_SENSOR_LEFT.get_color()
#         color_right = COLOR_SENSOR_RIGHT.get_color()

        if "grey" == "BLUE" or "black" == "BLUE":
            print("Blue color detected!")
            stop_event.set()  # Signal to stop the thread
            return
        time.sleep(0.1)

# Create the thread
thread = threading.Thread(target=detect_color)

def avoid_block_left():
    thread.start()
    
    #Set the limits of the wheels so that the result is always the same
    wheel_limits(50,80,50,80)
    
    speed(200, 200)
    
    #
    #back up 5cm
    #

    print("initial backup")
    wheel_position(-2,-2,0.05)
    
    print("rotate 1")
    #turn 1
    #try to position it so that the block passes through our arms
    rotate(6,0.05)
    
    print("forwards 1")
    #forward 1
    #Try to position the block close to the backwheel
    wheel_position(10,10,2)
    
    rotate(10, 0.05)
    
    wheel_position(7, 7, 2)
    
    print("rotate 2")
    rotate_right(25,0.1)
    
    total_cm = 0
    while(total_cm < 10):
        wheel_position(5,5,1)
        total_cm += 5
        time.sleep(0.1)
        if stop_event.is_set():
            print("Blue color detected!")
            return
    
    rotate_right(35,0.05)
    
    wheel_position(10,10,1)
    
    rotate(10, 0.05)
    
    wheel_position(10, 10, 1)
    
    rotate(40, 0.05)
    
    print("rotate 40 done")
    wheel_position(-10, -10, 2)
    
    rotate_right(20, 0.05)
    
    time.sleep(10)

    thread.join()

def retrace_step_1(right_degrees = 25):
    #retrace step 1 is called when the robot detects blue on the left side, it will move back to the initial position
    print("retrace step 1")
   
    rotate_right(right_degrees,0.05)
    return

def retrace_step_2(forward_distance = 15):
    #retrace step 2 is called when the robot detects blue on the left side, it will move back to the initial position
    print("retrace step 2")
    wheel_position(-forward_distance,-forward_distance,1)

    #retrace step 1 is called to turn the robot back to the initial position
    retrace_step_1()
    return

def retrace_step_3(left_degrees = 25):
    #retrace step 3 is called when the robot detects blue on the left side, it will move back to the initial position
    print("retrace step 3")
    rotate(left_degrees,0.05)
    
    #Calls retrace step 2 to incrementally move back
    retrace_step_2()
    return

def retrace_step_4(back_distance = 20):
    #retrace step 4 is called when the robot detects blue on the left side, it will move back to the initial position
    print("retrace step 4")
    wheel_position(-back_distance,-back_distance,1)
    
    #Calls retrace step 3 to incrementally move back
    retrace_step_3()
    return

def retrace_step_5(right_degrees = 25):
    #retrace step 5 is called when the robot detects blue on the left side, it will move back to the initial position
    print("retrace step 5")

    #turn right_degrees in the oposite direction as before
    rotate(right_degrees,0.05)
    
    #Calls retrace step 4 to incrementally move back
    retrace_step_4()
    return

def retrace_step_6(forward_distance = 10):
    #retrace step 6 is called when the robot detects blue on the left side, it will move back to the initial position
    print("retrace step 6")

    #move back the distance previously covered
    wheel_position(-forward_distance,-forward_distance,1)
    
    #Calls retrace step 5 to incrementally move back
    retrace_step_5()
    return

def avoid_block_right():
    #same function as avoid left but goes on the right side, it is called by avoid_block_left when blue is detected there
    thread.start()
    gyro = EV3GyroSensor(1)

    gyro.reset_measure()
    #You can use the following code to get the current angle of the robot

    print("initial backup")
    #back up 5cm
    wheel_position(-600,-600,2)
    time.sleep(0.2)

    if(stop_event.is_set()):
        print("Blue color detected!")
        return
    
    print("first rotate")
    #turn 90 degrees
    rotate_right(25,0.05)

    time.sleep(0.2)

    print("first forwards")
    #move forward 10cm
    wheel_position(400,400,1)

    time.sleep(0.2)

    print("second rotate")
    #turn 90 degrees back
    rotate(25,0.05)

    time.sleep(0.2)

    print("second forwards")

    #move forward 20cm
    wheel_position(1000,1000,1)

    time.sleep(0.2)
    
    print("third rotate")
    #turn 90 degrees
    rotate(90,0.05)

    time.sleep(0.2)

    print("third forward")
    #move forward 10cm
    wheel_position(200,200,1)

    time.sleep(0.2)

    print("last rotate")
    #turn back to initial position
    rotate_right(90,0.05)