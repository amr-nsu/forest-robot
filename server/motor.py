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
        

def camera_scan_stop():
    global camera_angle
    global scan_status
    # move_servo(c1_gpio, camera_angle, 0)
    # camera_angle = 0
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
