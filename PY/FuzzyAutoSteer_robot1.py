import time
import numpy as np
import skfuzzy as fuzz
import RPi.GPIO as GPIO
from random import randrange

GPIO.setmode(GPIO.BCM)

# constant
HC_SR04_RIGHT = 1
HC_SR04_FRONT = 2
HC_SR04_LEFT = 3
HC_SR04_BACK = 4
HC_SR04_MAX_TIMEOUT = 0.4

PIN_TRIG_RIGHT = 22
PIN_ECHO_RIGHT = 25

PIN_TRIG_FRONT = 5
PIN_ECHO_FRONT = 12

PIN_TRIG_LEFT = 24
PIN_ECHO_LEFT = 16

PIN_TRIG_BACK = 21
PIN_ECHO_BACK = 20

PIN_STANDBY = 26

PIN_LEFT_FORWARD = 19
PIN_LEFT_BACKWARD = 6

PIN_RIGHT_FORWARD = 13
PIN_RIGHT_BACKWARD = 17

MAX_DISTANCE = 400
MAX_SPEED = 100
SENSOR_DISTANCE_SPACE = np.arange(0, 121, 1)
SPEED_SPACE = np.arange(0, 31, 1)

IS_DOING_BACKWARD = False

# setup
# right HC_SR04
GPIO.setup(PIN_TRIG_RIGHT, GPIO.OUT)
GPIO.setup(PIN_ECHO_RIGHT, GPIO.IN)

# front HC_SR04
GPIO.setup(PIN_TRIG_FRONT, GPIO.OUT)
GPIO.setup(PIN_ECHO_FRONT, GPIO.IN)

# left HC_SR04
GPIO.setup(PIN_TRIG_LEFT, GPIO.OUT)
GPIO.setup(PIN_ECHO_LEFT, GPIO.IN)

# back HC_SR04
GPIO.setup(PIN_TRIG_BACK, GPIO.OUT)
GPIO.setup(PIN_ECHO_BACK, GPIO.IN)

# Standby pin
GPIO.setup(PIN_STANDBY, GPIO.OUT)

# Left pins
GPIO.setup(PIN_LEFT_FORWARD, GPIO.OUT)
GPIO.setup(PIN_LEFT_BACKWARD, GPIO.OUT)

# Right pins
GPIO.setup(PIN_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(PIN_RIGHT_BACKWARD, GPIO.OUT)

# PWM initialisation
left_forward_intensity = GPIO.PWM(PIN_LEFT_FORWARD, MAX_SPEED)
right_forward_intensity = GPIO.PWM(PIN_RIGHT_FORWARD, MAX_SPEED)
left_backward_intensity = GPIO.PWM(PIN_LEFT_BACKWARD, MAX_SPEED)
right_backward_intensity = GPIO.PWM(PIN_RIGHT_BACKWARD, MAX_SPEED)
left_forward_intensity.start(0)
right_forward_intensity.start(0)
left_backward_intensity.start(0)
right_backward_intensity.start(0)

# ----------------
def get_sensor_trigger_pin(sensor_const):
    if sensor_const == HC_SR04_RIGHT:
        return PIN_TRIG_RIGHT
    elif sensor_const == HC_SR04_FRONT:
        return PIN_TRIG_FRONT
    elif sensor_const == HC_SR04_LEFT:
        return PIN_TRIG_LEFT
    elif sensor_const == HC_SR04_BACK:
        return PIN_TRIG_BACK
    else:
        return 0
    
def get_sensor_echo_pin(sensor_const):
    if sensor_const == HC_SR04_RIGHT:
        return PIN_ECHO_RIGHT
    elif sensor_const == HC_SR04_FRONT:
        return PIN_ECHO_FRONT
    elif sensor_const == HC_SR04_LEFT:
        return PIN_ECHO_LEFT
    elif sensor_const == HC_SR04_BACK:
        return PIN_ECHO_BACK
    else:
        return 0

def distance(sensor_const):
    # set Trigger to HIGH
    GPIO.output(get_sensor_trigger_pin(sensor_const), True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(get_sensor_trigger_pin(sensor_const), False)
 
    # set timeout
    start_time = time.time()
    timeout = start_time + HC_SR04_MAX_TIMEOUT
 
    # save StartTime
    while GPIO.input(get_sensor_echo_pin(sensor_const)) == 0 and start_time < timeout:
        start_time = time.time()

    # set timeout
    stop_time = time.time()
    timeout = stop_time + HC_SR04_MAX_TIMEOUT
 
    # save time of arrival
    while GPIO.input(get_sensor_echo_pin(sensor_const)) == 1 and stop_time < timeout:
        stop_time = time.time()
 
    # time difference between start and arrival
    time_elapsed = stop_time - start_time
    
    # sonic speed (34300 cm/s)
    distance = round(time_elapsed * 17150, 2)
 
    return distance

def stop():
    left_forward_intensity.ChangeDutyCycle(0)
    right_forward_intensity.ChangeDutyCycle(0)
    left_backward_intensity.ChangeDutyCycle(0)
    right_backward_intensity.ChangeDutyCycle(0)
    GPIO.output(PIN_LEFT_FORWARD, False)
    GPIO.output(PIN_LEFT_BACKWARD, False)
    GPIO.output(PIN_RIGHT_FORWARD, False)
    GPIO.output(PIN_RIGHT_BACKWARD, False)
# ----------------

sensor_left = 0
sensor_front = 0
sensor_right = 0
sensor_back = 0

x_dist_front = SENSOR_DISTANCE_SPACE
x_dist_right = SENSOR_DISTANCE_SPACE
x_dist_left = SENSOR_DISTANCE_SPACE
x_dist_back = SENSOR_DISTANCE_SPACE

x_speed_left = SPEED_SPACE
x_speed_right = SPEED_SPACE

dist_front_1 = fuzz.trapmf(x_dist_front, [0, 0, 10, 20])
dist_front_2 = fuzz.trapmf(x_dist_front, [10, 20, 20, 40])
dist_front_3 = fuzz.trapmf(x_dist_front, [20, 40, MAX_DISTANCE, MAX_DISTANCE])

dist_right_1 = fuzz.trapmf(x_dist_right, [0, 0, 10, 20])
dist_right_2 = fuzz.trapmf(x_dist_right, [10, 20, 20, 40])
dist_right_3 = fuzz.trapmf(x_dist_right, [20, 40, MAX_DISTANCE, MAX_DISTANCE])

dist_left_1 = fuzz.trapmf(x_dist_left, [0, 0, 10, 20])
dist_left_2 = fuzz.trapmf(x_dist_left, [10, 20, 20, 40])
dist_left_3 = fuzz.trapmf(x_dist_left, [20, 40, MAX_DISTANCE, MAX_DISTANCE])

dist_back_1 = fuzz.trapmf(x_dist_back, [0, 0, 10, 20])
dist_back_2 = fuzz.trapmf(x_dist_back, [10, 20, 20, 40])
dist_back_3 = fuzz.trapmf(x_dist_back, [20, 40, MAX_DISTANCE, MAX_DISTANCE])

speed_left_1 = fuzz.trimf(x_speed_left, [0, 0, 5])
speed_left_2 = fuzz.trimf(x_speed_left, [0, 5, 15])
speed_left_3 = fuzz.trapmf(x_speed_left, [5, 15, MAX_SPEED, MAX_SPEED])

speed_right_1 = fuzz.trimf(x_speed_right, [0, 0, 5])
speed_right_2 = fuzz.trimf(x_speed_right, [0, 5, 15])
speed_right_3 = fuzz.trapmf(x_speed_right, [5, 15, MAX_SPEED, MAX_SPEED])

'''
if the distance at the front is close, turn to the direction with the the most far distance
if the distance at the front-right is close, turn to the left
if the distance at the front-left is close, turn to the right
if the distance at the front, left, and right is close, go backward
'''

GPIO.output(PIN_TRIG_RIGHT, GPIO.LOW)
GPIO.output(PIN_TRIG_FRONT, GPIO.LOW)
GPIO.output(PIN_TRIG_LEFT, GPIO.LOW)
GPIO.output(PIN_TRIG_BACK, GPIO.LOW)

GPIO.output(PIN_STANDBY, True)
GPIO.output(PIN_LEFT_FORWARD, True)
GPIO.output(PIN_LEFT_BACKWARD, False)
GPIO.output(PIN_RIGHT_FORWARD, True)
GPIO.output(PIN_RIGHT_BACKWARD, False)

print('Waiting for sensor to settle')
time.sleep(2)

try:
    while True:
        sensor_left = distance(HC_SR04_LEFT)
        sensor_front = distance(HC_SR04_FRONT)
        sensor_right = distance(HC_SR04_RIGHT)
        sensor_back = distance(HC_SR04_BACK)

        # rules
        dist_front_1_level = fuzz.interp_membership(x_dist_front, dist_front_1, sensor_front)
        dist_front_2_level = fuzz.interp_membership(x_dist_front, dist_front_2, sensor_front)
        dist_front_3_level = fuzz.interp_membership(x_dist_front, dist_front_3, sensor_front)

        dist_right_1_level = fuzz.interp_membership(x_dist_right, dist_right_1, sensor_right)
        dist_right_2_level = fuzz.interp_membership(x_dist_right, dist_right_2, sensor_right)
        dist_right_3_level = fuzz.interp_membership(x_dist_right, dist_right_3, sensor_right)

        dist_left_1_level = fuzz.interp_membership(x_dist_left, dist_left_1, sensor_left)
        dist_left_2_level = fuzz.interp_membership(x_dist_left, dist_left_2, sensor_left)
        dist_left_3_level = fuzz.interp_membership(x_dist_left, dist_left_3, sensor_left)

        dist_back_1_level = fuzz.interp_membership(x_dist_back, dist_back_1, sensor_back)
        dist_back_2_level = fuzz.interp_membership(x_dist_back, dist_back_2, sensor_back)
        dist_back_3_level = fuzz.interp_membership(x_dist_back, dist_back_3, sensor_back)
        # rules

        left_motor_lo = np.fmin(np.fmin(dist_front_1_level, dist_left_1_level), speed_left_1)
        left_motor_mid = np.fmin(np.fmin(dist_front_2_level, dist_left_2_level), speed_left_2)
        left_motor_hi = np.fmin(np.fmin(dist_front_3_level, dist_left_3_level), speed_left_3)

        right_motor_lo = np.fmin(np.fmin(dist_front_1_level, dist_right_1_level), speed_right_1)
        right_motor_mid = np.fmin(np.fmin(dist_front_2_level, dist_right_2_level), speed_right_2)
        right_motor_hi = np.fmin(np.fmin(dist_front_3_level, dist_right_3_level), speed_right_3)

        left_aggregated = np.fmax(left_motor_lo, np.fmax(left_motor_mid, left_motor_hi))
        right_aggregated = np.fmax(right_motor_lo, np.fmax(right_motor_mid, right_motor_hi))

        left_speed = fuzz.defuzz(x_speed_left, left_aggregated, 'mom')
        right_speed = fuzz.defuzz(x_speed_right, right_aggregated, 'mom')

        if left_speed == 0 and right_speed == 0:
            left_forward_intensity.ChangeDutyCycle(0)
            right_forward_intensity.ChangeDutyCycle(0)
            time.sleep(1)
            IS_DOING_BACKWARD = True
            GPIO.output(PIN_LEFT_FORWARD, False)
            GPIO.output(PIN_LEFT_BACKWARD, True)
            GPIO.output(PIN_RIGHT_FORWARD, False)
            GPIO.output(PIN_RIGHT_BACKWARD, True)
            left_backward_intensity.ChangeDutyCycle(MAX_SPEED/2)
            right_backward_intensity.ChangeDutyCycle(MAX_SPEED/2)
        else:
            if IS_DOING_BACKWARD == True:
                left_backward_intensity.ChangeDutyCycle(0)
                right_backward_intensity.ChangeDutyCycle(0)
                time.sleep(1)
                IS_DOING_BACKWARD = False
                
            GPIO.output(PIN_LEFT_FORWARD, True)
            GPIO.output(PIN_LEFT_BACKWARD, False)
            GPIO.output(PIN_RIGHT_FORWARD, True)
            GPIO.output(PIN_RIGHT_BACKWARD, False)
            left_forward_intensity.ChangeDutyCycle(left_speed)
            right_forward_intensity.ChangeDutyCycle(right_speed)

        print('++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('Left Sensor: %d | Front Sensor : %d | Right Sensor : %d' % (sensor_left, sensor_front, sensor_right))
        print('Left Motor : %d | Right Motor : %d' % (left_speed, right_speed))
        print('----------------------------------------------------')
        time.sleep(0.5)
        
except KeyboardInterrupt:
    print("Stopped by User")
    stop()
    GPIO.output(PIN_STANDBY, False)
    GPIO.cleanup()