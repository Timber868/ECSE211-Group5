from utils.brick import wait_ready_sensors, TouchSensor, Motor
from utils.sound import Sound
from time import sleep
from threading import Thread


###############################
### Global I/O declarations ###
###############################

touch1 = TouchSensor(1)     # Sensor port 1
touch2 = TouchSensor(2)     # Sensor port 2
touch3 = TouchSensor(3)     # Sensor port 3
enter = TouchSensor(4)      # Sensor port 4
motor = Motor("A")          # Motor port A

wait_ready_sensors()


#############################
### Drumming loop process ###
#############################

drum_on = False


def drum_loop():
    while True:
        if (drum_on):
            motor.set_position(-20)
            sleep(0.2)
            motor.set_position(20)
            sleep(0.2)


drum_th = Thread(target=drum_loop)
drum_th.start()


######################
### Robot commands ###
######################

def play_sound1():
    print('sound 1')
    sound1 = Sound(duration=1, pitch="A4", volume=90)
    sound1.play()


def play_sound2():
    print('sound 2')
    sound2 = Sound(duration=1, pitch="B4", volume=90)
    sound2.play()


def play_sound3():
    print('sound 3')
    sound3 = Sound(duration=1, pitch="C5", volume=90)
    sound3.play()


def play_sound4():
    print('sound 4')
    sound4 = Sound(duration=1, pitch="D5", volume=90)
    sound4.play()


def stop_all():
    no_tone = Sound(duration=1, pitch="A1", volume=0)
    no_tone.play()


#################
### Main loop ###
#################

while True:
    # While Enter TS is not pressed, do nothing
    if enter.get_raw_value() == 0:
        continue

    # Read command value from TS and concatenate in a 3 bit string
    command = str(touch3.get_raw_value()) + \
        str(touch2.get_raw_value()) + str(touch1.get_raw_value())

    # Switch statement to determine which command to execute
    if command == "000":
        play_sound1()
    elif command == "001":
        play_sound2()
    elif command == "010":
        play_sound3()
    elif command == "011":
        play_sound4()
    elif command == "100":
        if (not drum_on):
            motor.set_power(0)
            motor.set_limits(power=50)
            motor.reset_encoder()
            drum_on = True
        else:
            drum_on = False
            motor.set_position(0)
            motor.set_power(0)
    elif command == "101":
        pass
    elif command == "110":
        pass
    elif command == "111":
        drum_on = False
        motor.set_position(0)
        motor.set_power(0)
        stop_all()

    # Add a delay to slow down processor speed
    sleep(0.3)
