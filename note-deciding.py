#!/user/bin/env python3


from utils import sound
from utils.brick import EV3GyroSensor, wait_ready_sensors, TouchSensor
import time
import math

SOUND_1 = sound.Sound(duration=0.5, pitch="A4", volume=60)
SOUND_2 = sound.Sound(duration=1, pitch="A4", volume=60)
SOUND_3 = sound.Sound(duration=2, pitch="A4", volume=60)
SOUND_4 = sound.Sound(duration=3, pitch="A4", volume=60)

GYRO_SENSOR = EV3GyroSensor(1)
TOUCH_SENSOR_1 = TouchSensor(2)
TOUCH_SENSOR_2 = TouchSensor(3)

wait_ready_sensors()

GYRO_SENSOR.set_mode('abs')

def play_sound_1():
    print("note 1 played")
    SOUND_1.play()
    SOUND_1.wait_done()
    
def play_sound_2():
    print("note 2 played")
    SOUND_2.play()
    SOUND_2.wait_done()
    
def play_sound_3():
    print("note 3 played")
    SOUND_3.play()
    SOUND_3.wait_done()

def play_sound_4():
    print("note 4 played")
    SOUND_4.play()
    SOUND_4.wait_done()

def play_sound_on_con():
    try:
        while True:
            GYRO_SENSOR.reset_measure()
            result = GYRO_SENSOR.get_abs_measure()
            if result is None:
                result = 0
            tolerance = abs(result)
            print(f"tolerance: {tolerance}")
            time.sleep(0.3)
            if TOUCH_SENSOR_1.is_pressed() and TOUCH_SENSOR_2.is_pressed():
                play_sound_3()
            if (TOUCH_SENSOR_1.is_pressed() or TOUCH_SENSOR_2.is_pressed()) and tolerance > 15:
                play_sound_4()
            if TOUCH_SENSOR_1.is_pressed():
                play_sound_1()
            if TOUCH_SENSOR_2.is_pressed():
                play_sound_2()
                
                
    except BaseException:
        exit()
        
if __name__=='__main__':
    play_sound_1()
    play_sound_on_con()
                