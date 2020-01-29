import sys
import time
import random
import pigpio

pi = pigpio.pi()
gpio = 17
for pulse in range(500, 2000, 100):
    print(pulse)
    pi.set_servo_pulsewidth(gpio, pulse)
    time.sleep(1)

pi.stop()
