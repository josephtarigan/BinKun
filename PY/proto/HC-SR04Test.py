import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# constant
HC_SR04_RIGHT = 1
HC_SR04_FRONT = 2
HC_SR04_LEFT = 3
HC_SR04_BACK = 4
HC_SR04_MAX_TIMEOUT = 0.4

# right HC_SR04
PIN_TRIG_RIGHT = 22
PIN_ECHO_RIGHT = 25
GPIO.setup(PIN_TRIG_RIGHT, GPIO.OUT)
GPIO.setup(PIN_ECHO_RIGHT, GPIO.IN)

# front HC_SR04
PIN_TRIG_FRONT = 5
PIN_ECHO_FRONT = 12
GPIO.setup(PIN_TRIG_FRONT, GPIO.OUT)
GPIO.setup(PIN_ECHO_FRONT, GPIO.IN)

# left HC_SR04
PIN_TRIG_LEFT = 24
PIN_ECHO_LEFT = 16
GPIO.setup(PIN_TRIG_LEFT, GPIO.OUT)
GPIO.setup(PIN_ECHO_LEFT, GPIO.IN)

# back HC_SR04
PIN_TRIG_BACK = 21
PIN_ECHO_BACK = 20
GPIO.setup(PIN_TRIG_BACK, GPIO.OUT)
GPIO.setup(PIN_ECHO_BACK, GPIO.IN)

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

def main():
    GPIO.output(PIN_TRIG_RIGHT, GPIO.LOW)
    GPIO.output(PIN_TRIG_FRONT, GPIO.LOW)
    GPIO.output(PIN_TRIG_LEFT, GPIO.LOW)
    GPIO.output(PIN_TRIG_BACK, GPIO.LOW)
    
    print('Waiting for sensor to settle')
    time.sleep(2)
    
    try:
        while True:
            dist_right = distance(HC_SR04_RIGHT)
            dist_front = distance(HC_SR04_FRONT)
            dist_left = distance(HC_SR04_LEFT)
            dist_back = distance(HC_SR04_BACK)
            print('Right : %2f' % (dist_right))
            print('Front : %2f' % (dist_front))
            print('Left : %2f' % (dist_left))
            print('Back : %2f' % (dist_back))
            print('')
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

if __name__ == '__main__':
    main()