import RPi.GPIO as GPIO
from random import randint


class EightBitAdder:
    def __init__(self, output_pins, debug_on=False):
        self.output_pins = output_pins
        self.debug_on = debug_on
        self.setup_gpio()

    def debug(self, message):
        """ If debug is on, print the provided message."""
        if self.debug_on:
            print(message)

    def setup_gpio(self):
        """Setup the I/O pins and pin layout"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.output_pins, GPIO.OUT)
        self.debug(f'GPIO setup on pins {self.output_pins}')

    def run(self):
        bit_list_1 = self.generate_bits()
        bit_list_2 = self.generate_bits()
        sum_bit_list = self.add(bit_list_1, bit_list_2)

        self.illuminate(sum_bit_list)
        self.wait_to_cleanup()

    def generate_bits(self):
        """Generates a list of 8 random 1s and 0s, that is, a byte as a list"""
        bit_list = []
        for _ in range(8):
            random_bit = randint(0, 1)
            bit_list.append(random_bit)
        self.debug(f'Generated list {bit_list}')
        return bit_list

    def add(self, bit_list_1, bit_list_2):
        sum_bit_list = [0,0,0,0, 0,0,0,0]
        position = len(bit_list_1) - 1

        carry_out = 0
        while position >= 0:
            carry_in = carry_out
            input_a = bit_list_1[position]
            input_b = bit_list_2[position]

            sum_bit, carry_out = self.full_adder(carry_in, input_a, input_b)
            self.debug(f'Added Column: {carry_in} {input_a} {input_b}')
            self.debug(f'Got sum: {sum_bit} and carry: {carry_out}')
            sum_bit_list[position] = sum_bit

            position -= 1

        sum_bit_list.insert(0, carry_out)

        self.debug(f'Finished Adding:\n\t   {bit_list_1}\n + \t   {bit_list_2}')
        self.debug(f'Result:\t{sum_bit_list}')

        return sum_bit_list

    def half_adder(self, input_a, input_b):
        """Takes in A and B, returns S and C by applying half adder logic using bitwise operators"""

        sum_bit = input_a ^ input_b
        carry_bit = input_a & input_b

        return sum_bit, carry_bit

    def full_adder(self, carry_in, input_a, input_b):
        """
        Takes in Cin, A, and B. Applies Full Adder Logic
        using bitwise operators (and a half adder function) to produce the sum bit and the carry bit
        """
        sum_bit_1, carry_bit_1 = self.half_adder(input_a, input_b)
        sum_bit_2, carry_bit_2 = self.half_adder(sum_bit_1, carry_in)
        carry_bit = carry_bit_1 | carry_bit_2

        return sum_bit_1, carry_bit

    def illuminate(self, bit_list):
        """Lights up the corresponding LEDs for the list"""

        for index, bit in enumerate(bit_list):
            if bit == 1:
                GPIO.output(self.output_pins[index], GPIO.HIGH)
            else:
                GPIO.output(self.output_pins[index], GPIO.LOW)

        self.debug("Illuminated LEDs")

    def wait_to_cleanup(self):
        input('Press ENTER to terminate')
        GPIO.cleanup()


# main
output_pins = [17, 18, 27, 22,
               26, 12, 16, 20, 21]

adder = EightBitAdder(output_pins, debug_on=True)
adder.run()