# Natalie Gates ; Pi Activity 2

import RPi.GPIO as GPIO
from time import sleep

# Set to wherever the LED is connected
LED = 6

# Set to wherever the button is connected
BUTTON = 20

# Constants for our pause times
TIME1 = 0.5
TIME2 = 0.1

# Setup components
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Run forever (no error catching)
while True:
    # Turn on LED then wait
    GPIO.output(LED, GPIO.HIGH)

    if GPIO.input(BUTTON) : sleep(TIME2) # If button is down, wait TIME2
    else : sleep(TIME1) # If button is up, wait TIME1

    # Turn off LED then wait
    GPIO.output(LED, GPIO.LOW)

    if GPIO.input(BUTTON) : sleep(TIME2)
    else : sleep(TIME1)