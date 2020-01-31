import time
import pigpio
from lib.bmp280 import BMP280

pi = pigpio.pi()

global last_motion_time
last_motion_time = 0

MOTION_GPIO = 18
MOTION_TIMEOUT = 30  # s

pi.set_mode(MOTION_GPIO, pigpio.INPUT)


def motion():
    global last_motion_time
    if time.time() - last_motion_time < MOTION_TIMEOUT:
        return False
    if pi.read(MOTION_GPIO):
        last_motion_time = time.time()
        return True
    return False


bmp280 = BMP280()

global pressure_init
pressure_init = 0


def init():
    global pressure_init
    pressure_init, _ = pressure_and_temperature()


def pressure_and_temperature():
    return bmp280.getReading()    


def altitude_baro():
    global pressure_init
    pressure, temperature = pressure_and_temperature()
    R = 29.27   # Газовая постоянная, м/град
    TR = 0.005  # Температурный градиент, град/м
    T = 273 + temperature  # Абсолютная температура
    return (1 - (pressure / pressure_init)**(TR * R)) * T / TR


if __name__ == '__main__':
    while True:
        print(pressure_and_temperature())
        print(pi.read(MOTION_GPIO))
        time.sleep(1)
