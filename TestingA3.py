#!/usr/bin/env python3

# Testing A3
import time
from subsystems import motor_settings

if __name__ == "__main__":
    motor_settings.wheel_limits(100,180,100,180)
    motor_settings.arm_limits(70,90,70,90)
    motor_settings.rotate(90, 0.002)
