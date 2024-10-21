# Natalie Gates ; Button class

import RPi.GPIO as GPIO

class Button:
    def __init__(self, pin, led_st1=None):
        """
        State 1: Assign an led to turn on and off

        :param pin:
        :param led_st1: Assign an LED to control during state 1
        """
        self.was_pressed = False

        self.pin = pin
        self.led_md1 = led_st1
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_pressed(self):
        return GPIO.input(self.pin)

    # Define continuous behavior while up or down for each state
    def while_pressed(self, state):
        if self.is_pressed():
            if state == 1 and self.led_md1:  # Turn md1 led on
                # May interfere with flashing LEDs
                self.led_md1.on()
        else:
            if state == 1 and self.led_md1:  # Turn md1 led off
                self.led_md1.off()

    # Checks for, and registers "press" input
    def register_input(self):
        """
        :return: Returns true if button is pressed, and this is the first frame it has been pressed; otherwise false
        """
        if self.is_pressed() and (not self.was_pressed):
            # Only register input if this is the first frame it has been pressed for
            self.was_pressed = True
            return True
        elif self.is_pressed():
            return False
        else:
            # If button is up, then reset the state
            self.was_pressed = False
            return False