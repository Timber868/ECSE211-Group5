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
    
    #
    #back up 5cm
    #

    print("initial backup")
    wheel_position(-5,-5,2)
    time.sleep(0.1)

    #turn 25 degrees
    #We try to avoid the block on the left side and every 5 degrees
    #we check if the robot detected blue while moving forward
    #If blue is detected, we retrace back to our initial avoidance position
    print("first rotate")

    total_degrees = 5
    while(total_degrees < 25):
        rotate(5,0.05)
        total_degrees += 5
        time.sleep(0.1)
        if stop_event.is_set():
            print("Blue color detected!")
            retrace_step_1(total_degrees)
            avoid_block_right()
            return
    
    #
    #move forward 10cm
    #We try to move forward 
    #If blue is detected, we retrace back to our initial avoidance position
    print("first forwards")
    
    total_cm = 5
    while(total_cm < 15):
        wheel_position(5,15,1)
        total_cm += 5
        time.sleep(0.1)
        if stop_event.is_set():
            print("Blue color detected!")
            retrace_step_2(total_cm)
            avoid_block_right()
            return
    
    #
    #turn 25 degrees right
    #
    print("second rotate")

    total_degrees = 5
    while(total_degrees < 25):
        rotate_right(5,0.05)
        total_degrees += 5
        time.sleep(0.1)
        if stop_event.is_set():
            print("Blue color detected!")
            retrace_step_3(total_degrees)
            avoid_block_right()
            return
    
    #
    #move forward 20cm
    #
    print("second forwards")

    total_cm = 5
    while(total_cm < 20):
        wheel_position(5,5,1)
        total_cm += 5
        time.sleep(0.1)
        if stop_event.is_set():
            print("Blue color detected!")
            retrace_step_4(total_cm)
            avoid_block_right()
            return

    #
    #turn 25 degrees right
    #
    print("third rotate")

    total_degrees = 5
    while(total_degrees < 25):
        rotate_right(5,0.05)
        total_degrees += 5
        time.sleep(0.1)
        if stop_event.is_set():
            print("Blue color detected!")
            retrace_step_5(total_degrees)
            avoid_block_right()
            return
    
    # 
    #move forward 10cm
    #
    print("third forward")

    total_cm = 5
    while(total_cm < 10):
        wheel_position(5,5,1)
        total_cm += 5
        time.sleep(0.1)
        if stop_event.is_set():
            print("Blue color detected!")
            retrace_step_6(total_cm)
            avoid_block_right()
            return
    #Final rotation to initial direction
    #No need to retrace back as ther should not be any water   
    rotate(35, 0.05)
    time.sleep(0.1)
    
    #Finish the thread
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