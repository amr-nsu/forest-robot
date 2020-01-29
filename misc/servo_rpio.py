import time
from RPIO import PWM
servo = PWM.Servo()
# Set servo on GPIO17 to 900.s (0.9ms)
servo.set_servo(17, 900)
# Set servo on GPIO17 to 2000.s (2.0ms)
#servo.set_servo(17, 2000)
try:
    while True:
        servo.set_servo(17, 750)
        print("Left")
        time.sleep(1)
        servo.set_servo(17, 1500)
        print("Center")
        time.sleep(1)
        print("Right")
        servo.set_servo(17, 2500)
        time.sleep(1)
except KeyboardInterrupt:
    # Clear servo on GPIO17
    servo.stop_servo(17)
