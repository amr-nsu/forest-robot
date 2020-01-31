import cv2
import time
from time import gmtime, strftime

static_frame = None
last_motion_time = None
motion_state = False

MOTION_TIMEOUT = 5  # s
THRESHOLD = 30
CONTOUR_AREA = 2000


def motion(frame, gray_frame, draw=False):
    motion = False
    global static_frame
    global last_motion_time
    if static_frame is None:
        static_frame = gray_frame
        return
    elif last_motion_time is not None:
        if time.time() - last_motion_time > MOTION_TIMEOUT:
            static_frame = None
            last_motion_time = None
            return

    diff_frame = cv2.absdiff(static_frame, gray_frame)

    _, thresh_frame = cv2.threshold(diff_frame, THRESHOLD, 255,
                                    cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(thresh_frame.copy(),
                                      cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow("Gray", gray_frame)
    # cv2.imshow("Diff", diff_frame)
    # cv2.imshow("Threshold", thresh_frame)

    for contour in contours:
        if cv2.contourArea(contour) < CONTOUR_AREA:
            continue
        motion = True
        if draw:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

    global motion_state
    if motion_state != motion:
        motion_state = motion
        if motion:
            print(strftime('%Y-%m-%d %H:%M:%S', gmtime()), 'motion detect')
            last_motion_time = time.time()
    return motion


cascadeWildCats = cv2.CascadeClassifier("lib/haarcascade_frontalcatface.xml")
cascadeMonkeys = cv2.CascadeClassifier("lib/haarcascade_frontalface_default.xml")


def animal(frame, frame_gray, draw=False):
    wildcats = cascadeWildCats.detectMultiScale(frame_gray, 1.5, 1)
    if len(wildcats) > 0:
        return 'wildcat', wildcats[0]
    monkeys = cascadeMonkeys.detectMultiScale(frame_gray, 1.5, 1)
    if len(monkeys) > 0:
        return 'monkey', monkeys[0]
    return None, None


def animal_info(frame, title, position):
    (x, y, w, h) = position
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(frame, title, (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))


def main():
    video = cv2.VideoCapture(1)
    while True:
        _, frame = video.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.GaussianBlur(frame_gray, (21, 21), 0)

        motion(frame, frame_gray, draw=True)
        t, a = animal(frame, frame_gray, draw=True)
        if t is not None:
            animal_info(frame, t, a)

        cv2.imshow("Color", frame)

        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    main()
