import time
import pigpio

pi = pigpio.pi()

while True:
    print(pi.read(18))
    time.sleep(0.2)

