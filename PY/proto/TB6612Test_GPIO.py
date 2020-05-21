import RPi.GPIO as GPIO
from time import sleep

# init
GPIO.setmode(GPIO.BCM)
MAX_SPEED = 25

# Standby pin
PIN_STANDBY = 26
GPIO.setup(PIN_STANDBY, GPIO.OUT)

# Left pins
PIN_LEFT_FORWARD = 19
PIN_LEFT_BACKWARD = 6
GPIO.setup(PIN_LEFT_FORWARD, GPIO.OUT)
GPIO.setup(PIN_LEFT_BACKWARD, GPIO.OUT)

# Right pins
PIN_RIGHT_FORWARD = 13
PIN_RIGHT_BACKWARD = 17
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

def stop():
    left_forward_intensity.ChangeDutyCycle(0)
    right_forward_intensity.ChangeDutyCycle(0)
    left_backward_intensity.ChangeDutyCycle(0)
    right_backward_intensity.ChangeDutyCycle(0)
    GPIO.output(PIN_LEFT_FORWARD, False)
    GPIO.output(PIN_LEFT_BACKWARD, False)
    GPIO.output(PIN_RIGHT_FORWARD, False)
    GPIO.output(PIN_RIGHT_BACKWARD, False)
    
def backward(intensity):
    left_forward_intensity.ChangeDutyCycle(0)
    right_forward_intensity.ChangeDutyCycle(0)
    left_backward_intensity.ChangeDutyCycle(intensity)
    right_backward_intensity.ChangeDutyCycle(intensity)
    GPIO.output(PIN_LEFT_FORWARD, False)
    GPIO.output(PIN_LEFT_BACKWARD, True)
    GPIO.output(PIN_RIGHT_FORWARD, False)
    GPIO.output(PIN_RIGHT_BACKWARD, True)
    
def left(intensity):
    left_forward_intensity.ChangeDutyCycle(0)
    right_forward_intensity.ChangeDutyCycle(intensity)
    left_backward_intensity.ChangeDutyCycle(intensity)
    right_backward_intensity.ChangeDutyCycle(0)
    GPIO.output(PIN_LEFT_FORWARD, False)
    GPIO.output(PIN_LEFT_BACKWARD, True)
    GPIO.output(PIN_RIGHT_FORWARD, True)
    GPIO.output(PIN_RIGHT_BACKWARD, False)
    
def right(intensity):
    left_forward_intensity.ChangeDutyCycle(intensity)
    right_forward_intensity.ChangeDutyCycle(0)
    left_backward_intensity.ChangeDutyCycle(0)
    right_backward_intensity.ChangeDutyCycle(intensity)
    GPIO.output(PIN_LEFT_FORWARD, True)
    GPIO.output(PIN_LEFT_BACKWARD, False)
    GPIO.output(PIN_RIGHT_FORWARD, False)
    GPIO.output(PIN_RIGHT_BACKWARD, True)

def forward(intensity):
    left_forward_intensity.ChangeDutyCycle(intensity)
    right_forward_intensity.ChangeDutyCycle(intensity)
    left_backward_intensity.ChangeDutyCycle(0)
    right_backward_intensity.ChangeDutyCycle(0)
    GPIO.output(PIN_LEFT_FORWARD, True)
    GPIO.output(PIN_LEFT_BACKWARD, False)
    GPIO.output(PIN_RIGHT_FORWARD, True)
    GPIO.output(PIN_RIGHT_BACKWARD, False)

def main():
    GPIO.output(PIN_STANDBY, GPIO.HIGH)
    print('Right')
    right(10)
    sleep(3)
    stop()
    sleep(1)
    print('Left')
    left(10)
    sleep(3)
    stop()
    sleep(1)
    print('Forward')
    forward(10)
    sleep(3)
    stop()
    sleep(1)
    print('Backward')
    backward(10)
    sleep(3)
    stop()
    sleep(1)
    print('Stop')
    
    
    GPIO.output(PIN_STANDBY, False)
    GPIO.cleanup()
    
if __name__ == '__main__':
    main()