# Natalie Gates ; rpi passcode game

import RPi.GPIO as GPIO
from time import sleep

# classes for components
class led:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

class button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize components

GPIO.setmode(GPIO.BCM)

# Main Code
