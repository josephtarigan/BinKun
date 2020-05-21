import time
from random import randrange

sensor_left = 0
sensor_front = 0
sensor_right = 0
sensor_back = 0

direction_constant = 0.0
speed_constant = 0.0

MAX_DISTANCE = 90

while True:
    sensor_left = randrange(1, MAX_DISTANCE)
    sensor_front = randrange(1, MAX_DISTANCE)
    sensor_right = randrange(1, MAX_DISTANCE)
    sensor_back = MAX_DISTANCE

    speed_constant = min([sensor_left, sensor_front, sensor_right])/MAX_DISTANCE

    print('Left Sensor: %d | Front Sensor : %d | Right Sensor : %d' % (sensor_left, sensor_front, sensor_right))
    print('Speed Constant : %.3f' % speed_constant)
    time.sleep(1)
