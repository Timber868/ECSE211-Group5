from subsystems.motor_settings import Turn, MoveDistFwd 
from subsystems.collect_color_sensor_data import collect_color_sensor_data
from subsystems.utils.brick import EV3ColorSensor, EV3UltrasonicSensor
from subsystems.utils.brick import reset_brick
import time
import threading
# import object avoidance function
# 
# 

US_SENSOR_BACK = EV3ColorSensor(1)

def get_distance():
    distance = US_SENSOR_BACK.get_distance()
    return distance

def return_to_origin():
    pass

def first_fwd():
    pass

def second_fwd():
    pass

# go fwd
# scan for obstacles/blocks every 5 cm
# if obstacle or water detected, call return_to_origin()
# if reaching wall from the front, call return_to_origin()
# once return_to_origin() is called, rotate 90 degrees and call second_fwd()
# repeat
# after second return_to_origin(), drop off poop!
# stop sensors
def nav_main():
    pass



if __name__ == "__main__":
    try:
        nav_main()
    except KeyboardInterrupt:
        reset_brick()
        print("Robot was interrupted")
    pass