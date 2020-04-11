from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
from time import sleep

# Standby pin
PIN_STANDBY = 21

# Left pins
PIN_LEFT_PWM = 19
PIN_LEFT_FORWARD = 5
PIN_LEFT_BACKWARD = 6

# Right pins
PIN_RIGHT_PWM = 13
PIN_RIGHT_FORWARD = 27
PIN_RIGHT_BACKWARD = 17

# PWM initialisation
left_intensity = PWMOutputDevice(PIN_LEFT_PWM, True, 0, 255)
right_intensity = PWMOutputDevice(PIN_RIGHT_PWM, True, 0, 255)

# H-Bridge objects initialisation
left_forward = DigitalOutputDevice(PIN_LEFT_FORWARD)
left_backward = DigitalOutputDevice(PIN_LEFT_BACKWARD)
right_forward = DigitalOutputDevice(PIN_RIGHT_FORWARD)
right_backward = DigitalOutputDevice(PIN_RIGHT_BACKWARD)

# standby
standby_pin = DigitalOutputDevice(PIN_STANDBY)

def stop():
    left_forward.value = False
    left_backward.value = False
    right_forward.value = False
    right_backward.value = False
    left_intensity.value = 0
    right_intensity.value = 0
    standby_pin.value = False
    
def forward():
    standby_pin.value = True
    left_forward.value = True
    left_backward.value = False
    right_forward.value = True
    right_backward.value = False
    left_intensity.value = 1.0
    right_intensity.value = 1.0
    
def backward():
    standby_pin.value = True
    left_forward.value = False
    left_backward.value = True
    right_forward.value = False
    right_backward.value = True
    left_intensity.value = 0.1
    right_intensity.value = 0.1
    
def left(intensity):
    standby_pin.value = True
    left_forward.value = True
    left_backward.value = False
    right_forward.value = True
    right_backward.value = False
    left_intensity.value = intensity
    right_intensity.value = 1.0
    
def right(intensity):
    standby_pin.value = True
    left_forward.value = True
    left_backward.value = False
    right_forward.value = True
    right_backward.value = False
    left_intensity.value = 1.0
    right_intensity.value = intensity
    
def main():
    stop()
    print('Forward')
    forward()
    sleep(3)
    print('Left')
    left(0.2)
    sleep(3)
    print('Right')
    right(0.2)
    sleep(3)
    #print('backward')
    #backward()
    #sleep(1)
    print('Stop')
    stop()
    
if __name__ == '__main__':
    main()