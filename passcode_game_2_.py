# Natalie Gates ; rpi passcode game

import RPi.GPIO as GPIO
from time import sleep
import atexit

# classes for components
class Led:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    # Methods to turn LED on and off
    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

class Button:
    def __init__(self, pin, led_md1=None):
        """

        :param pin:
        :param led_md1: Assign an LED to control during mode 1
        """
        self.pin = pin
        self.led_md1 = led_md1
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_pressed(self):
        return GPIO.input(self.pin)

    def on_press(self):
        if self.is_pressed():
            if self.led_md1:
                self.led_md1.on()
        else:
            if self.led_md1:
                self.led_md1.off()

# Initialize components
GPIO.setmode(GPIO.BCM)

leds = {
    # First set of LEDs
    'LED_G1': Led(4),  # green
    'LED_B1': Led(5),  # blue
    'LED_Y1': Led(6),  # yellow
    'LED_R1': Led(12), # red

    'LED_G3': Led(13), # green
    'LED_R2': Led(16), # red
    'LED_Y2': Led(27), # yellow
    'LED_B2': Led(26), # blue
}

buttons = {
# First set of LEDs
    'BUTTON_1': Button(23, led_md1=leds["LED_G1"]),  # green
    'BUTTON_2': Button(22, led_md1=leds["LED_B1"]),  # blue
    'BUTTON_3': Button(21, led_md1=leds["LED_Y1"]),  # yellow
    'BUTTON_4': Button(20, led_md1=leds["LED_R1"]), # red

    'BUTTON_5': Button(19), # green
    'BUTTON_6': Button(18), # red
}

# Exit handler
@atexit.register
def on_exit():
    print('Closing!')
    for led_ in leds.values():
        led_.off()
    GPIO.cleanup()

# Main Code
print('Starting!')

while True:
    # To turn off the program cleanly (without having to force quit it or keyboard interrupt etc.)
    i = 0
    for button in buttons.values():
        if button.is_pressed():
            i += 1
        if i >= 4:
            # Triggers if at least 4 buttons are pressed at once
            exit()

    pass