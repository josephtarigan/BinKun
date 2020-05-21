import time
from random import randrange

sensor_left = 0
sensor_front = 0
sensor_right = 0
sensor_back = 0

direction_constant = 0.0
speed_constant = 0.0

MAX_DISTANCE = 90

def speed_constant_given_distance (distance):
    if distance > 20:
        return 1
    elif distance <= 20 and distance > 15:
        return 0.5
    elif distance <= 15 and distance > 10:
        return 0.15
    elif distance <= 10:
        return 0

while True:
    sensor_left = randrange(1, MAX_DISTANCE)
    sensor_front = randrange(1, MAX_DISTANCE)
    sensor_right = randrange(1, MAX_DISTANCE)
    sensor_back = MAX_DISTANCE

    speed_constant_left = speed_constant_given_distance(sensor_right);
    speed_constant_right = speed_constant_given_distance(sensor_left)

    # what if those 2 return 0?
    # check which side has the shortest distance
    if speed_constant_right == speed_constant_left:
        if sensor_right < sensor_front:
            speed_constant_left = 0
            speed_constant_right = 0.5
        elif sensor_right > sensor_front:
            speed_constant_left = 0.5
            speed_constant_right = 0
        else:
            speed_constant_left = 0.5
            speed_constant_right = 0


    print('Left Sensor: %d | Front Sensor : %d | Right Sensor : %d' % (sensor_left, sensor_front, sensor_right))
    print('Speed Constant Left : %.3f | Speed Constant Right : %.3f' % (speed_constant_left, speed_constant_right))
    time.sleep(1)

