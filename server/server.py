import cv2
import picamera
import socketserver
import sqlite3
from threading import Lock
from http import server
from os import curdir, sep
import io
import numpy as np
import time
import RPi.GPIO as GPIO
from datetime import datetime

# own libs
import detect
import database


SERVO1_GPIO = 17
SERVO_FREQUENCY = 50  # Hz

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO1_GPIO, GPIO.OUT)
servo1_pwm = GPIO.PWM(SERVO1_GPIO, SERVO_FREQUENCY)
servo1_pwm.start(0)

global servo1_dc
servo1_dc = 7.5
servo1_pwm.ChangeDutyCycle(servo1_dc)
time.sleep(0.2)
servo1_pwm.ChangeDutyCycle(0)

def rotate_camera(direction):
    global servo1_dc
    servo1_dc += direction * 0.5
    servo1_pwm.ChangeDutyCycle(servo1_dc)
    time.sleep(0.2)
    servo1_pwm.ChangeDutyCycle(0)


global mode_auto
mode_auto = False 

global counter
counter = 0


class StreamingOutput(object):
    def __init__(self):
        self.lock = Lock()
        self.frame = io.BytesIO()
        self.clients = []


        
    def write(self, buf):
        global counter
        counter += 1
        died = []
        if buf.startswith(b'\xff\xd8'):
            size = self.frame.tell()
            if size > 0:
                self.frame.seek(0)
                data = self.frame.read(size)

                global mode_auto
#                print("mode", mode_auto)
                
                if mode_auto and counter % 10 == 0:              
                    frame = np.fromstring(self.frame.getvalue(), dtype=np.uint8)
                    frame = cv2.imdecode(frame, 1) 
                    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    if detect.motion(frame, frame_gray):
                        database.write('Движение по камере')
                       
                self.frame.seek(0)
                with self.lock:
                    for client in self.clients:
                        try:
                            client.wfile.write(b'--FRAME\r\n')
                            client.send_header('Content-Type', 'image/jpeg')
                            client.send_header('Content-Length', size)
                            client.end_headers()
                            client.wfile.write(data)#bilo data
                            client.wfile.write(b'\r\n')
                        except Exception as e:
                            died.append(client)
        self.frame.write(buf)
        if died:
            self.remove_clients(died)

    def flush(self):
        with self.lock:
            for client in self.clients:
                client.wfile.close()

    def add_client(self, client):
        print('Adding streaming client %s:%d' % client.client_address)
        with self.lock:
            self.clients.append(client)

    def remove_clients(self, clients):
        with self.lock:
            for client in clients:
                try:
                    print('Removing streaming client %s:%d' % client.client_address)
                    self.clients.remove(client)
                except ValueError:
                    pass # already removed


class HTTPHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path += 'index.html'
        if self.path.endswith(".html") or self.path.endswith(".js") or self.path.endswith(".svg") or self.path.endswith(".css"):
            self.send_response(200)
            self.end_headers()
            try:
                f = open(curdir + sep + self.path)
                self.wfile.write(bytes(f.read(), 'utf-8'))
                f.close()
            except IOError as e:
                self.send_error(404, str(e))
        elif self.path == '/stream.mjpg':
            self.close_connection = False
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=--FRAME')
            self.end_headers()
            output.add_client(self)
        if 'cmd=' in self.path:
            self.send_response(200)
            self.end_headers()
            cmd = self.path.split('cmd=')[1][0]
            if cmd == 'a':
                global mode_auto
                mode_auto = not mode_auto
                database.write_mode(mode_auto)
            elif cmd == 'l':
                rotate_camera(1)
            elif cmd == 'r':
                rotate_camera(-1)
            elif cmd == 'd':
                self.wfile.write(bytes(database.read_last(13), 'utf-8'))          
            

if __name__ == '__main__':   

    PORT = 8000
    print("Server started at 10.42.0.1:%s" % PORT)
    database.init_demo()

    class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
        pass
 
    with picamera.PiCamera(resolution=(640, 480), framerate=24) as camera:
        output = StreamingOutput()
        camera.start_recording(output, format='mjpeg')
        try:
            address = ('', PORT)
            server = StreamingServer(address, HTTPHandler)
            server.serve_forever()
        finally:
            camera.stop_recording()
