# Natalie Gates ; rpi passcode game

import RPi.GPIO as GPIO
from time import sleep
import atexit

# classes for components
class led:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    # Methods to turn LED on and off
    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

class button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_pressed(self):
        return GPIO.input(self.pin)

# Initialize components
GPIO.setmode(GPIO.BCM)

leds = {
    # First set of LEDs
    "LED_G1": led(4),  # green
    "LED_B1": led(5),  # blue
    "LED_Y1": led(6),  # yellow
    "LED_R1": led(12), # red

    "LED_G3": led(13), # green
    "LED_R2": led(16), # red
    "LED_Y2": led(27), # yellow
    "LED_B2": led(26), # blue
}

buttons = {
# First set of LEDs
    "BUTTON_1": button(23),  # green
    "BUTTON_2": button(22),  # blue
    "BUTTON_3": button(21),  # yellow
    "BUTTON_4": button(20), # red

    "BUTTON_5": button(19), # green
    "BUTTON_6": button(18), # red
}

# Exit handler
@atexit.register
def on_exit():
    print("Closing!")
    GPIO.cleanup()

# Main Code
print("Starting!")

while True:
    if buttons["BUTTON_1"].is_pressed():
        exit()