#!/bin/env python3

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
p = GPIO.PWM(17, 50)  # channel=X frequency=50Hz
p.start(0)
try:
    while 1:
        for dc in range(5, 10, 1):
            print(dc)
            p.ChangeDutyCycle(dc)
            time.sleep(0.5)
        for dc in range(10, 5, -1):
            print(dc)
            p.ChangeDutyCycle(dc)
            time.sleep(0.5)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()
