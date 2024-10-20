# Natalie Gates ; Code class

from random import randint
from Led import Led

class Code:
    def __init__(self, leds):
        self.code = []
        self.generate_code()  # Generate a code automatically on creation

        self.leds = leds  # store the led list (hopefully should stay updated since it is a list of pointers)
        self.display_finished = True
        self.flash_queue = []  # Acts as a queue/stack; furthest right element ([-1]) is considered first/on top

    def update(self, state):
        if state == 2:
            # Flash LEDs when previous is finished
            previous_finished = True
            for led in self.leds:
                if led.flashing:  # If any of the leds are flashing, then the previous led hasn't finished yet
                    previous_finished = False

            # If the previous led has finished, flash the next one
            if previous_finished:
                self.flash_queue[-1].flash(1.3)
                self.flash_queue.pop()

            if previous_finished and len(self.flash_queue):
                # No items left in queue and all LEDs have finished flashing; Code display has finished
                self.display_finished = True

    def display_code(self):
        self.display_finished = False

        # Flash the first LED in the code and queue the rest
        self.leds[f'LED_{self.code[0]}'].flash(1.3)  # Flash the first LED in the code for 1.3 seconds

        for i in range(len(self.code), 0, -1):  # Iterate through the code starting at the end
            self.flash_queue.append(self.leds[f'LED_{self.code[i]}'])

    def check_code(self, code):
        return code == self.code

    def generate_code(self, length=4):
        """
        Generate a random code of a specified length
        :param length: defaults to 4
        """
        code = []
        for i in range(length):
            code.append(randint(1, 4))
        self.code = code