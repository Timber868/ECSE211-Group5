from subsystems.motor_settings import Turn, MoveDistFwd 
from subsystems.color_sensor_start_stop import get_both_sensor_color
from subsystems.object_detection import detect_obstacles, a_gyro
from subsystems.utils.brick import EV3ColorSensor, EV3UltrasonicSensor
from subsystems.utils.brick import reset_brick
import time
import threading


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
            a_gyro()

        blockInTheWay = detect_obstacles()

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