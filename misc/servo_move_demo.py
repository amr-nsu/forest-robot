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
        step = 10
    else:
        step = -10
    for pwm in range(from_pwm, to_pwm, step):
        pi.set_servo_pulsewidth(servo_gpio, pwm)
        time.sleep(0.01)
        
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
    pi.set_servo_pulsewidth(b1_gpio, 1500)
    pi.set_servo_pulsewidth(b2_gpio, 1500)
#    pi.set_servo_pulsewidth(b3_gpio, 1100)
    pi.set_servo_pulsewidth(b4_gpio, 1500)
    pi.set_servo_pulsewidth(w2_gpio, 1500)
    
def hold1(param=True):
    if param:
        move_servo(w1_gpio, 1500, 1800)
    else:
        move_servo(w1_gpio, 1800, 1500)
    
def hold2(param=True):
    if param:
        move_servo(w2_gpio, 1500, 1800)
    else:
        move_servo(w2_gpio, 1800, 1500)
        
def step():
    for v in range(0, 200, 1):
        pi.set_servo_pulsewidth(b1_gpio, 1500 - v/4)
        pi.set_servo_pulsewidth(b2_gpio, 1500 + v)
        pi.set_servo_pulsewidth(b4_gpio, 1500 + v)
        time.sleep(0.003)

def step_back():
    for v in range(200, 0, -1):
        pi.set_servo_pulsewidth(b1_gpio, 1500 - v/4)
        pi.set_servo_pulsewidth(b2_gpio, 1500 + v)
        pi.set_servo_pulsewidth(b4_gpio, 1500 + v)
        time.sleep(0.003)
   
init()

time.sleep(3)

for _ in range(5):
    hold1()
    hold2(False)
    step()
    hold2()
    hold1(False)
    step_back()

stop()


