import time
import pigpio

pi = pigpio.pi()

c1_gpio = 17  # camera
w1_gpio = 22  # claw1
b1_gpio = 27  # body1
b2_gpio = 6   # body2
b3_gpio = 13  # body3
b4_gpio = 19  # body4
w2_gpio = 26  # claw2


def clamp(value, min_value, max_value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


def angle2pwm(angle):
    """convert angles from [-90, 90] to servo pwm"""
    return 1500 + 1000.0 / 90.0 * clamp(angle, -90, 90)


global camera_angle
camera_angle = 0

global scan_status
scan_status = False


def camera_scan():
    global camera_angle
    global scan_status
    if not scan_status:
        move_servo(c1_gpio, camera_angle, 45)
        camera_angle = 45        
        scan_status = True
        
        # disable motor for save power
        pi.set_servo_pulsewidth(c1_gpio, 0)
    else:
        rotate_camera(-15)
        if camera_angle == -90:
            return False
    return True
        

def camera_scan_stop(return_to_center=False):
    global camera_angle
    global scan_status
    if return_to_center:
        move_servo(c1_gpio, camera_angle, 0)
        camera_angle = 0
    scan_status = False


def rotate_camera(step):
    global camera_angle
    new_camera_angle = clamp(camera_angle + step, -90, 45)
    move_servo(c1_gpio, camera_angle, new_camera_angle)
    camera_angle = new_camera_angle
    
    # disable motor for save power
    pi.set_servo_pulsewidth(c1_gpio, 0)


def move_servo(servo_gpio, from_angle, to_angle):
    if to_angle > from_angle:
        step = 1
    else:
        step = -1
    for angle in range(from_angle, to_angle, step):
        pi.set_servo_pulsewidth(servo_gpio, angle2pwm(angle))
        time.sleep(0.02)

def move_servo_pwm(servo_gpio, from_pwm, to_pwm):
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
        move_servo_pwm(w1_gpio, 1500, 2000)
    else:
        move_servo_pwm(w1_gpio, 2000, 1500)
    

def hold2(param=True):
    if param:
        move_servo_pwm(w2_gpio, 1500, 2000)
    else:
        move_servo_pwm(w2_gpio, 2000, 1500)
        

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


def move_forward(count):
    for _ in range(count):
        hold1()
        hold2(False)
        step()
        hold2()
        hold1(False)
        step_back()
    stop()
    
def move_backward(count):
    stop()

