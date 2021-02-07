import time
import numpy as np
import skfuzzy as fuzz
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
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
SENSOR_DISTANCE_SPACE = np.arange(0, MAX_DISTANCE + 1, 1)
SPEED_SPACE = np.arange(0, MAX_SPEED + 1, 1)

IS_DOING_BACKWARD = False

'''
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
'''

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

x_speed = SPEED_SPACE

dist_front_near = fuzz.trapmf(x_dist_front, [0, 0, 20, 50])
dist_front_far = fuzz.trapmf(x_dist_front, [20, 50, MAX_DISTANCE, MAX_DISTANCE])

dist_left_near = fuzz.trapmf(x_dist_left, [0, 0, 20, 50])
dist_left_far = fuzz.trapmf(x_dist_left, [20, 50, MAX_DISTANCE, MAX_DISTANCE])

dist_right_near = fuzz.trapmf(x_dist_right, [0, 0, 20, 50])
dist_right_far = fuzz.trapmf(x_dist_right, [20, 50, MAX_DISTANCE, MAX_DISTANCE])

dist_back_near = fuzz.trapmf(x_dist_back, [0, 0, 20, 50])
dist_back_far = fuzz.trapmf(x_dist_back, [20, 50, MAX_DISTANCE, MAX_DISTANCE])

left_speed_slow = fuzz.trapmf(x_speed, [0, 0, 5, 10])
left_speed_slow_mid = fuzz.trimf(x_speed, [8, 25, 50])
left_speed_mid = fuzz.trimf(x_speed, [25, 50, 75])
left_speed_mid_fast = fuzz.trimf(x_speed, [50, 75, 95])
left_speed_fast = fuzz.trapmf(x_speed, [65, 95, MAX_SPEED, MAX_DISTANCE])

right_speed_slow = fuzz.trapmf(x_speed, [0, 0, 5, 10])
right_speed_slow_mid = fuzz.trimf(x_speed, [8, 25, 50])
right_speed_mid = fuzz.trimf(x_speed, [25, 50, 75])
right_speed_mid_fast = fuzz.trimf(x_speed, [50, 75, 95])
right_speed_fast = fuzz.trapmf(x_speed, [65, 95, MAX_SPEED, MAX_DISTANCE])

'''
fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(8, 9))

ax0.plot(x_dist_front, dist_front_near, 'b', linewidth=1.5, label='1')
ax0.plot(x_dist_front, dist_front_far, 'g', linewidth=1.5, label='2')
ax0.set_title('Front Distance')
ax0.legend()

ax1.plot(x_dist_left, dist_left_near, 'b', linewidth=1.5, label='1')
ax1.plot(x_dist_left, dist_left_far, 'g', linewidth=1.5, label='2')
ax1.set_title('Left Distance')
ax1.legend()

# Turn off top/right axes
for ax in (ax0, ax1):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()
plt.show()
'''

'''
fig, (ax0) = plt.subplots(nrows=1, figsize=(8, 9))

ax0.plot(x_speed, left_speed_slow, 'b', linewidth=1.5, label='slow')
ax0.plot(x_speed, left_speed_slow_mid, 'g', linewidth=1.5, label='slow-mid')
ax0.plot(x_speed, left_speed_mid, 'r', linewidth=1.5, label='mid')
ax0.plot(x_speed, left_speed_mid_fast, 'y', linewidth=1.5, label='mid-fast')
ax0.plot(x_speed, left_speed_fast, 'c', linewidth=1.5, label='fast')
ax0.set_title('Speed Left')
ax0.legend()

# Turn off top/right axesax.spines['top'].set_visible(False)
ax0.spines['right'].set_visible(False)
ax0.get_xaxis().tick_bottom()
ax0.get_yaxis().tick_left()

plt.tight_layout()
plt.show()
'''

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

        # interpretation
        dist_front_near_level = fuzz.interp_membership(x_dist_front, dist_front_near, sensor_front)
        dist_front_far_level = fuzz.interp_membership(x_dist_front, dist_front_far, sensor_front)

        dist_right_near_level = fuzz.interp_membership(x_dist_right, dist_right_near, sensor_right)
        dist_right_far_level = fuzz.interp_membership(x_dist_right, dist_right_far, sensor_right)

        dist_left_near_level = fuzz.interp_membership(x_dist_left, dist_left_near, sensor_left)
        dist_left_far_level = fuzz.interp_membership(x_dist_left, dist_left_far, sensor_left)
        
        dist_back_near_level = fuzz.interp_membership(x_dist_back, dist_back_near, sensor_back)
        dist_back_far_level = fuzz.interp_membership(x_dist_back, dist_back_far, sensor_back)
        # interpretation

        # rules=
        left_motor_slow = np.fmin(np.asarray([dist_left_near_level
                                              , dist_front_near_level
                                              , dist_right_near_level
                                              , dist_left_far_level
                                              , dist_right_far_level]).min(0), left_speed_slow)
        left_motor_slow_mid = np.fmin(np.asarray([dist_left_near_level
                                              , dist_front_near_level
                                              , dist_right_near_level
                                              , dist_left_far_level
                                              , dist_right_far_level]).min(0), left_speed_slow_mid)
        left_motor_mid = np.fmin(np.asarray([dist_left_near_level
                                              , dist_front_near_level
                                              , dist_right_near_level
                                              , dist_left_far_level
                                              , dist_right_far_level]).min(0), left_speed_mid)
        left_motor_mid_fast = np.fmin(np.asarray([dist_left_near_level
                                              , dist_front_near_level
                                              , dist_right_near_level
                                              , dist_left_far_level
                                              , dist_right_far_level]).min(0), left_speed_mid_fast)
        left_motor_fast = np.fmin(np.asarray([dist_left_near_level
                                              , dist_front_near_level
                                              , dist_right_near_level
                                              , dist_left_far_level
                                              , dist_right_far_level]).min(0), left_speed_fast)

        right_motor_lo = np.fmin(np.fmin(dist_front_1_level, dist_right_1_level), speed_right_1)
        right_motor_mid = np.fmin(np.fmin(dist_front_2_level, dist_right_2_level), speed_right_2)
        right_motor_hi = np.fmin(np.fmin(dist_front_3_level, dist_right_3_level), speed_right_3)
        # rules

        # aggregation
        left_aggregated = np.fmax(left_motor_lo, np.fmax(left_motor_mid, left_motor_hi))
        right_aggregated = np.fmax(right_motor_lo, np.fmax(right_motor_mid, right_motor_hi))
        # aggregation

        # defuzzification
        left_speed = fuzz.defuzz(x_speed_left, left_aggregated, 'mom')
        right_speed = fuzz.defuzz(x_speed_right, right_aggregated, 'mom')
        # defuzzification
        
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