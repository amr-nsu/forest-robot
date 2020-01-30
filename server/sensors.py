import time
import pigpio

pi = pigpio.pi()

global last_motion_time
last_motion_time = 0

MOTION_GPIO = 18
MOTION_TIMEOUT = 10  # s

pi.set_mode(MOTION_GPIO, pigpio.INPUT)


def motion():
    global last_motion_time
    if time.time() - last_motion_time < MOTION_TIMEOUT:
        return False
    if pi.read(MOTION_GPIO):
        last_motion_time = time.time()
        return True
    return False


if __name__ == '__main__':
    while True:
        print(pi.read(MOTION_GPIO))
        time.sleep(0.2)
