from utils.brick import Motor
from time import *
motor = Motor("A")
n = 0
while n<10:
    motor.set_power(-20)
    sleep(0.4)
    motor.set_power(20)
    sleep(0.2)
    
    motor.set_power(-20)
    sleep(0.4)
    motor.set_power(20)
    sleep(0.2)


    motor.set_power(-20)
    sleep(0.2)
    motor.set_power(20)
    sleep(0.1)

    motor.set_power(-20)
    sleep(0.2)
    motor.set_power(20)
    sleep(0.1)


    motor.set_power(-20)
    sleep(0.4)
    motor.set_power(20)
    sleep(0.2)

    motor.set_power(0)
    n+=1