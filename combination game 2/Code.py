# Natalie Gates ; Code class

from random import randint
# from Led import Led

class Code:
    def __init__(self, leds, queue):
        self.code = []
        self.generate_code()  # Generate a code automatically on creation

        self.leds = leds  # store the led list (hopefully should stay updated since it is a list of pointers)
        self.queue = queue

        self.display_finished = True

    def update(self, state):
        if state == 2:
            if self.queue.previous_finished() and self.queue.queue_empty():
                # No items left in queue and all LEDs have finished flashing; Code display has finished
                self.display_finished = True

    def display_code(self):
        self.display_finished = False
        print(f'Displaying Code: {self.code}')

        # Flash the first LED in the code and queue the rest
        # self.leds[f'LED_{self.code[0]}'].flash(1.3)  # Flash the first LED in the code for 1.3 seconds

        # Queue all the leds to flash (including the 1st one so that it waits for the red light to go off before flashing)
        for i in range(len(self.code) - 1, -1, -1):  # Iterate through the code starting at the end
            self.queue.queue_add(self.leds[f'LED_{self.code[i] + 4}'], 1.3, 0.3)  # Add 4 to i to get a # in range 5-8

    def check_code(self, code):
        """
        Check if the code is correct
        :param code: Code/inputs to check
        """

        return self.code == code

        # if len(self.code) != len(code) : return False

        # for i in range(len(self.code)):
        #     print(f'{i}: {self.code[i]}:{code[i]}')
        #     # Since the code uses LEDs 5-8, but the inputs are 1-4:
        #     if self.code[i] == 5:
        #         print(f'{i}: Correct')
        #         if code[i] == 1 : continue
        #     if self.code[i] == 6:
        #         print(f'{i}: Correct')
        #         if code[i] == 2 : continue
        #     if self.code[i] == 7:
        #         print(f'{i}: Correct')
        #         if code[i] == 3 : continue
        #     if self.code[i] == 8:
        #         print(f'{i}: Correct')
        #         if code[i] == 4 : continue
        #     print('Incorrect code')
        #     return False
        #
        # return True

    def generate_code(self, length=4):
        """
        Generate a random code of a specified length
        :param length: defaults to 4
        """
        code = []
        for i in range(length):
            code.append(randint(1, 4))
        self.code = code