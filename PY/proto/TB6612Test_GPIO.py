import RPi.GPIO as GPIO
from time import sleep

# init
GPIO.setmode(GPIO.BCM)
MAX_SPEED = 30

# Standby pin
PIN_STANDBY = 21
GPIO.setup(21, GPIO.OUT)

# Left pins
PIN_LEFT_PWM = 19
PIN_LEFT_FORWARD = 5
PIN_LEFT_BACKWARD = 6
GPIO.setup(PIN_LEFT_PWM, GPIO.OUT)
GPIO.setup(PIN_LEFT_FORWARD, GPIO.OUT)
GPIO.setup(PIN_LEFT_BACKWARD, GPIO.OUT)

# Right pins
PIN_RIGHT_PWM = 13
PIN_RIGHT_FORWARD = 27
PIN_RIGHT_BACKWARD = 17
GPIO.setup(PIN_RIGHT_PWM, GPIO.OUT)
GPIO.setup(PIN_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(PIN_RIGHT_BACKWARD, GPIO.OUT)

# PWM initialisation
left_intensity = GPIO.PWM(PIN_LEFT_PWM, 255)
right_intensity = GPIO.PWM(PIN_RIGHT_PWM, 255)
left_intensity.start(0)
right_intensity.start(0)

def stop():
    GPIO.output(PIN_LEFT_FORWARD, False)
    GPIO.output(PIN_LEFT_BACKWARD, False)
    GPIO.output(PIN_RIGHT_FORWARD, False)
    GPIO.output(PIN_RIGHT_BACKWARD, False)
    left_intensity.ChangeDutyCycle(0)
    right_intensity.ChangeDutyCycle(0)
    
def forward():
    GPIO.output(PIN_LEFT_FORWARD, True)
    GPIO.output(PIN_LEFT_BACKWARD, False)
    GPIO.output(PIN_RIGHT_FORWARD, True)
    GPIO.output(PIN_RIGHT_BACKWARD, False)
    left_intensity.ChangeDutyCycle(MAX_SPEED)
    right_intensity.ChangeDutyCycle(MAX_SPEED)
    
def left(intensity):
    GPIO.output(PIN_LEFT_FORWARD, True)
    GPIO.output(PIN_LEFT_BACKWARD, False)
    GPIO.output(PIN_RIGHT_FORWARD, True)
    GPIO.output(PIN_RIGHT_BACKWARD, False)
    left_intensity.ChangeDutyCycle(intensity)
    right_intensity.ChangeDutyCycle(MAX_SPEED)
    
def right(intensity):
    GPIO.output(PIN_LEFT_FORWARD, True)
    GPIO.output(PIN_LEFT_BACKWARD, False)
    GPIO.output(PIN_RIGHT_FORWARD, True)
    GPIO.output(PIN_RIGHT_BACKWARD, False)
    left_intensity.ChangeDutyCycle(MAX_SPEED)
    right_intensity.ChangeDutyCycle(intensity)
    
def main():
    GPIO.output(PIN_STANDBY, GPIO.HIGH)
    #print('Forward')
    #forward()
    #sleep(5)
    #stop()
    print('Left')
    left(20)
    sleep(3)
    left(15)
    sleep(3)
    stop()
    #print('Right')
    #right(10)
    #sleep(5)
    stop()
    print('Stop')
    
    left_intensity.stop()
    right_intensity.stop()
    GPIO.output(PIN_STANDBY, False)
    GPIO.cleanup()
    
if __name__ == '__main__':
    main()