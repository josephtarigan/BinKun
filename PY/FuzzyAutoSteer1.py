import time
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from random import randrange

sensor_left = 0
sensor_front = 0
sensor_right = 0
sensor_back = 0

MAX_DISTANCE = 300
MAX_SPEED = 30
SENSOR_DISTANCE_SPACE = np.arange(0, 121, 1)
SPEED_SPACE = np.arange(0, 31, 1)

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
fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4, figsize=(8, 9))

ax0.plot(x_dist_front, dist_front_1, 'b', linewidth=1.5, label='1')
ax0.plot(x_dist_front, dist_front_2, 'g', linewidth=1.5, label='2')
ax0.plot(x_dist_front, dist_front_3, 'r', linewidth=1.5, label='3')
ax0.set_title('Front Distance')
ax0.legend()

ax1.plot(x_dist_right, dist_right_1, 'b', linewidth=1.5, label='1')
ax1.plot(x_dist_right, dist_right_2, 'g', linewidth=1.5, label='2')
ax1.plot(x_dist_right, dist_right_3, 'r', linewidth=1.5, label='3')
ax1.set_title('Right Distance')
ax1.legend()

ax2.plot(x_dist_left, dist_left_1, 'b', linewidth=1.5, label='1')
ax2.plot(x_dist_left, dist_left_2, 'g', linewidth=1.5, label='2')
ax2.plot(x_dist_left, dist_left_3, 'r', linewidth=1.5, label='3')
ax2.set_title('Left Distance')
ax2.legend()

ax3.plot(x_dist_back, dist_back_1, 'b', linewidth=1.5, label='1')
ax3.plot(x_dist_back, dist_back_2, 'g', linewidth=1.5, label='2')
ax3.plot(x_dist_back, dist_back_3, 'r', linewidth=1.5, label='3')
ax3.set_title('Back Distance')
ax3.legend()

# Turn off top/right axes
for ax in (ax0, ax1, ax2, ax3):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()
plt.show()
'''

'''
if the distance at the front is close, turn to the direction with the the most far distance
if the distance at the front-right is close, turn to the left
if the distance at the front-left is close, turn to the right
if the distance at the front, left, and right is close, go backward
'''

while True:
    sensor_left = randrange(1, MAX_DISTANCE)
    sensor_front = randrange(1, MAX_DISTANCE)
    sensor_right = randrange(1, MAX_DISTANCE)
    sensor_back = randrange(1, MAX_DISTANCE)

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

    left_motor_lo = np.fmin(np.fmin(dist_front_1_level, dist_left_1_level), speed_left_1)
    left_motor_mid = np.fmin(np.fmin(dist_front_2_level, dist_left_2_level), speed_left_2)
    left_motor_hi = np.fmin(np.fmin(dist_front_3_level, dist_left_3_level), speed_left_3)

    right_motor_lo = np.fmin(np.fmin(dist_front_1_level, dist_right_1_level), speed_left_1)
    right_motor_mid = np.fmin(np.fmin(dist_front_2_level, dist_right_2_level), speed_left_2)
    right_motor_hi = np.fmin(np.fmin(dist_front_3_level, dist_right_3_level), speed_right_3)

    left_aggregated = np.fmax(left_motor_lo, np.fmax(left_motor_mid, left_motor_hi))
    right_aggregated = np.fmax(right_motor_lo, np.fmax(right_motor_mid, right_motor_hi))

    left_speed = fuzz.defuzz(x_speed_left, left_aggregated, 'mom')
    right_speed = fuzz.defuzz(x_speed_right, right_aggregated, 'mom')

    print('++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('Left Sensor: %d | Front Sensor : %d | Right Sensor : %d' % (sensor_left, sensor_front, sensor_right))
    print('Left Motor : %d | Right Motor : %d' % (left_speed, right_speed))
    print('----------------------------------------------------')
    time.sleep(1)