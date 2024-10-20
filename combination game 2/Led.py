# Natalie Gates ; Led class

import RPi.GPIO as GPIO
import time as Time

class Led:
    def __init__(self, pin):
        # Initialize instance variables
        self.flashing = False
        self.start_time = None
        self.flash_time = None

        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    # Function designed to be executed every frame
    def update(self, state):
        if self.flashing:
            # If the LED is currently flashing, turn it off once the correct amount of time has passed
            if (Time.time() - self.start_time) >= self.flash_time:
                self.off()
                self.start_time = None
                self.flashing = False

    # Start a flash (overriding any previous ones)
    def flash(self, time):
        self.flashing = True
        self.start_time = Time.time()
        self.flash_time = time
        self.on()

    # Methods to turn LED on and off
    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)