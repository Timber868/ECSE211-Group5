from subsystems.motor_settings import Turn, MoveDistFwd 
from subsystems.color_sensor_start_stop import get_both_sensor_color
from subsystems.object_detection import detect_obstacles, a_gyro, move_and_catch
from subsystems.utils.brick import EV3ColorSensor, EV3UltrasonicSensor
from subsystems.utils.brick import reset_brick
import time
import threading

US_SENSOR = EV3UltrasonicSensor(3)

#Scan angle is how much we want to scan to it defaults to 90
def scan(scan_angle=90):
    #Needed to track how much we have scanned
    total_angle = 0

    #turns to true if we detect obstacles in our path
    obstacle_in_the_way = False

    while total_angle < scan_angle:
        #Turn incrementally by 3 degrees
        Turn(-3, 200)
        total_angle += 3
        time.sleep(0.1)
        
        #Get the us sensor distance
        distance = US_SENSOR.get_value()
        while distance == 0:
            distance = US_SENSOR.get_value()

        #If its further than 30cm away ignore it
        if distance < 30:
            MoveDistFwd(30, 200)
            time.sleep(5)


            #call mvoe and catch which scans to make sure its poop and catches it if it is
            caught_poop = move_and_catch()

            if caught_poop == True:
                MoveDistFwd(-distance, 200)
                time.sleep(5)

            else:
                #Move further back as we also moved forward to pick up the poop
                MoveDistFwd(-distance - 15, 200)
                time.sleep(5)

                
                #We know that a block thats not poo is in the way if its less than 10 degrees in front of us
                if total_angle < 10:
                    obstacle_in_the_way = True

            #Turn an extra 5 degerees to avoid rescanning the same block
            Turn(-5, 200)
            time.sleep(0.1)

            total_angle += 5

    #Reorient yourself back to what you were facing before
    Turn(total_angle, 200)
    time.sleep(0.1)

    #return wether or not there is something in the way. If there i we cant go forwards.
    return obstacle_in_the_way


stop_event = threading.Event()

# Thread to detect the water
def detect_color():
    while not stop_event.is_set():
        color_left, color_right = get_both_sensor_color()
        print(f"left: {color_left}, right: {color_right}")

        if color_left == "water" or color_right == "water":
            print("Water detected!")
            stop_event.set()
        
        time.sleep(1)


def first_fwd():
    # Create and start the thread
    thread = threading.Thread(target=detect_color)
    thread.start()

    # Boolean that becomes true whenever water or a block in the way is detected
    obstacle_detected = False

    # Boolean that becomes true whenever a block is in the way
    blockInTheWay = False

    total_distance = 0

    # Move forward 5 cm at a time
    while not obstacle_detected and blockInTheWay == False:
        MoveDistFwd(5, 200)
        total_distance += 5

        # Check if water was detected
        if stop_event.is_set():
            obstacle_detected = True
            break
        
        # Every 20cm, scan to see if there are blocks we can pick up
        if total_distance % 20 == 0:
            blockInTheWay = scan()

    # Wait for the detect_color thread to finish
    thread.join()


US_SENSOR_BACK = EV3ColorSensor(1)

def get_distance_behind():
    distance = US_SENSOR_BACK.get_distance()
    return distance

def return_to_origin():
    distance_behind = get_distance_behind()

    # Go back in increments of 2cm until we are 5cm away from the origin
    while distance_behind > 5:
        MoveDistFwd(-2, 200)
        distance_behind = get_distance_behind()

def turning_step():
    Turn(-90, 200)    



def second_fwd():
    first_fwd()

# go fwd
# scan for obstacles/blocks every 5 cm
# if obstacle or water detected, call return_to_origin()
# if reaching wall from the front, call return_to_origin()
# once return_to_origin() is called, rotate 90 degrees and call second_fwd()
# repeat
# after second return_to_origin(), drop off poop!
# stop sensors
def nav_main():
    first_fwd()
    return_to_origin()
    turning_step()
    second_fwd()
    pass





if __name__ == "__main__":
    try:
        nav_main()
    except KeyboardInterrupt:
        reset_brick()
        print("Robot was interrupted")
    pass