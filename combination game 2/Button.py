import RPi.GPIO as GPIO

class Button:
    def __init__(self, pin, led_md1=None):
        """
        Mode 1: Assign an led to turn on and off

        :param pin:
        :param led_md1: Assign an LED to control via mode 1
        """
        self.was_pressed = False

        self.pin = pin
        self.led_md1 = led_md1
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_pressed(self):
        return GPIO.input(self.pin)

    # Press and Unpress behavior
    def on_press(self):
        if self.is_pressed():
            if self.led_md1:  # Turn md1 led on
                self.led_md1.on()
        else:
            if self.led_md1:  # Turn md1 led off
                self.led_md1.off()

    # Checks for, and registers input
    def register_input(self):
        """
        :return: Returns true if button is pressed, and this is the first frame it has been pressed; otherwise false
        """
        if self.is_pressed():
            # Only register input if this is the first frame it has been pressed for
            if not self.was_pressed:
                self.was_pressed = True
                return True
            else:
                return False
        else:
            # If button is up, then reset the state
            self.was_pressed = False