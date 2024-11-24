#!/usr/bin/env python3

# Testing B3
import time
from subsystems import motor_settings, object_detection

if __name__ == "__main__":
    while True:
        object_detection.print_distance()
