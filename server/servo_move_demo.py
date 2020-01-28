import sys
import time
import random
import pigpio

pi = pigpio.pi()
c1_gpio = 17  # camera
w1_gpio = 22  # claw1
b1_gpio = 27  # body1
b2_gpio = 6   # body2
b3_gpio = 13  # body3
b4_gpio = 19  # body4
w2_gpio = 26  # claw2

def move_servo(servo_gpio, from_pwm, to_pwm):
    if to_pwm > from_pwm:
        step = 50
    else:
        step = -50
    for pwm in range(from_pwm, to_pwm, step):
        pi.set_servo_pulsewidth(servo_gpio, pwm)
        time.sleep(0.1)
        
def stop():
    pi.set_servo_pulsewidth(c1_gpio, 0)
    pi.set_servo_pulsewidth(w1_gpio, 0)
    pi.set_servo_pulsewidth(b1_gpio, 0)
    pi.set_servo_pulsewidth(b2_gpio, 0)
    pi.set_servo_pulsewidth(b3_gpio, 0)
    pi.set_servo_pulsewidth(b4_gpio, 0)
    pi.set_servo_pulsewidth(w2_gpio, 0)
    pi.stop()

def init():
#    pi.set_servo_pulsewidth(c1_gpio, 1500)
    pi.set_servo_pulsewidth(w1_gpio, 1500)
    pi.set_servo_pulsewidth(b1_gpio, 900)
#    pi.set_servo_pulsewidth(b2_gpio, 1100)
#    pi.set_servo_pulsewidth(b3_gpio, 1100)
    pi.set_servo_pulsewidth(b4_gpio, 1500)
    pi.set_servo_pulsewidth(w2_gpio, 2000)
    
def hold():
    move_servo(w1_gpio, 1500, 2000)  # hold 1

def step():
    for v in range(0, 400, 100):
        pi.set_servo_pulsewidth(b1_gpio, 900 - v)
        pi.set_servo_pulsewidth(b4_gpio, 1500 + v)
        time.sleep(0.25)

    move_servo(w2_gpio, 2000, 1500)  # hold 2
    move_servo(w1_gpio, 2000, 1500)  # unhold 1

    

#init()
#time.sleep(3)

hold()
time.sleep(1)

step()
time.sleep(2)

stop()


