from utils.brick import Motor
import time

# orientation
motor_catcher = Motor("A")
motor_sensor = Motor("D")

isArmOpen = False

def arms_reset():
    # Designates to Encoder, that the current physical position is 0 degrees
    motor_catcher.reset_encoder()
    motor_sensor.reset_encoder()

def stop_sensor_arm():
    motor_sensor.set_power(0)
    
def rotate_sensor_arm():
    global isArmOpen
    motor_sensor.set_position_relative(100)
    isArmOpen = True
    time.sleep(2)
    
def rotate_initial_position_arm():
    global isArmOpen
    motor_sensor.set_position_relative(-100)
    isArmOpen = True
    time.sleep(2)

def stop_catcher():
    # set the power to 0 when its done
    motor_catcher.set_power(0)

def get_arm_state()->bool:
    return isArmOpen
    
def arm_limits(p1,d1,p2,d2):
    motor_catcher.set_limits(power=p1, dps=d1)
    motor_sensor.set_limits(power=p2, dps=d2)
    
if __name__ == "__main__":
    stop_sensor_arm()
    rotate_sensor_arm()
    get_arm_state()
    #time.sleep(4)
    #rotate_initial_position_arm()