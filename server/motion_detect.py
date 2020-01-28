import cv2
import time
from time import gmtime, strftime

static_frame = None
last_motion_time = None
motion_state = False

MOTION_TIMEOUT = 30  # s
THRESHOLD = 30
CONTOUR_AREA = 2000


def detect_motion(frame, gray_frame):
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
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    global motion_state
    if motion_state != motion:
        motion_state = motion
        if motion:
            print(strftime('%Y-%m-%d %H:%M:%S', gmtime()), 'motion detect')
            last_motion_time = time.time()


def main():
    video = cv2.VideoCapture(0)
    while True:
        _, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray, (11, 11), 0)

        detect_motion(frame, gray)

        cv2.imshow("Color", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
