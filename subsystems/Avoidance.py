from subsystems.utils.brick import Motor, EV3GyroSensor, EV3ColorSensor, wait_ready_sensors
from subsystems.motor_settings import rotate, rotate_right, wheel_position
import threading
import time

stop_event = threading.Event()

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
    
    #back up 5cm
    print("initial backup")
    wheel_position(-200,-200,2)
    time.sleep(0.2)
    
    #turn 90 degrees
    print("first rotate")
    rotate(25,0.05)
    time.sleep(0.2)

    #Check if the robot detected blue while moving forward 
    if stop_event.is_set():
        print("Blue color detected!")

        #If blue is detected, retrace back to our initial avoidance position
        retrace_step_1()

        #Then avoid the block on the right side instead
        avoid_block_right()

        return

    #move forward 10cm
    print("first forwards")
    wheel_position(400,400,1)
    time.sleep(0.2)

    #Check if the robot detected blue while moving forward 
    if stop_event.is_set():
        print("Blue color detected!")

        #If blue is detected, retrace back to our initial avoidance position
        retrace_step_2()
        
        #Then avoid the block on the right side instead
        avoid_block_right()
        return

    
    #turn 90 degrees back
    print("second rotate")
    rotate_right(25,0.05)
    time.sleep(0.2)

    if stop_event.is_set():
        print("Blue color detected!")

        #If blue is detected, retrace back to our initial avoidance position
        retrace_step_3()

        avoid_block_right()
        return
    
    #move forward 20cm
    print("second forwards")
    wheel_position(600,600,1)
    time.sleep(0.2)

    if stop_event.is_set():
        print("Blue color detected!")

        #If blue is detected, retrace back to our initial avoidance position
        retrace_step_4()

        avoid_block_right()
        return
    
    

    

    #Finish the thread
    thread.join()

def retrace_step_1(right_degrees = 25):
    #retrace step 1 is called when the robot detects blue on the left side, it will move back to the initial position
    print("retrace step 1")
    rotate_right(25,0.05)
    return

def retrace_step_2(forward_distance = 400):
    #retrace step 2 is called when the robot detects blue on the left side, it will move back to the initial position
    print("retrace step 2")
    wheel_position(-forward_distance,-forward_distance,1)

    #retrace step 1 is called to turn the robot back to the initial position
    retrace_step_1()
    return

def retrace_step_3(left_degrees = 25):
    #retrace step 3 is called when the robot detects blue on the left side, it will move back to the initial position
    print("retrace step 3")
    rotate(25,0.05)
    
    #Calls retrace step 2 to incrementally move back
    retrace_step_2()
    return

def retrace_step_4(back_distance = 1000):
    #retrace step 4 is called when the robot detects blue on the left side, it will move back to the initial position
    print("retrace step 4")
    wheel_position(-back_distance,-back_distance,1)
    
    #Calls retrace step 3 to incrementally move back
    retrace_step_3()
    return

def retrace_step_5(right_degrees = 90):
    #retrace step 5 is called when the robot detects blue on the left side, it will move back to the initial position
    print("retrace step 5")

    #turn 90 degrees in the oposite direction as before
    rotate(90,0.05)
    
    #Calls retrace step 4 to incrementally move back
    retrace_step_4()
    return

def retrace_step_6(forward_distance = 200):
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