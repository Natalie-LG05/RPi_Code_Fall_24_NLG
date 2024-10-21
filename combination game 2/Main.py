# Natalie Gates ; rpi passcode game

import RPi.GPIO as GPIO
import atexit  # For exit handling

from time import sleep

# Classes for components
from Led import Led
from Button import Button

from Code import Code
from Queue import Queue

# Initialize components
GPIO.setmode(GPIO.BCM)

leds = {
    # First set of LEDs
    'LED_1': Led(4),   # green
    'LED_2': Led(5),   # blue
    'LED_3': Led(6),   # yellow
    'LED_4': Led(12),  # red

    # Second set of LEDs
    'LED_5': Led(13),  # green
    'LED_6': Led(16),  # blue
    'LED_7': Led(27),  # yellow
    'LED_8': Led(26),  # red

    # Extra red and green LED (for correct and incorrect / right and wrong)
    'LED_9': Led(25),   # red
    'LED_10': Led(24),  # green
}

buttons = {
    # First set of Buttons
    'BUTTON_1': Button(23, led_st1=leds["LED_1"]),  # green
    'BUTTON_2': Button(22, led_st1=leds["LED_2"]),  # blue
    'BUTTON_3': Button(21, led_st1=leds["LED_3"]),  # yellow
    'BUTTON_4': Button(20, led_st1=leds["LED_4"]),  # red

    'BUTTON_5': Button(19),  # enter button
    'BUTTON_6': Button(18),  # change mode button
}

# Setup the queue (used for flashing LEDs in sequence)
queue = Queue(leds)

# Setup the code
code = Code(leds, queue)
print(f'The first code is: {code.code}')

# Exit handler
@atexit.register
def on_exit():
    print('Closing!')
    for led_ in leds.values():
        led_.off()
    GPIO.cleanup()

# Main Code
print('Starting!')
# The current State of the program
state = 1  # Begin in state 1
mode = 1  # Begin in success protocol mode 1
modes_amount = 2  # Amount of modes

# Input tracking
inputs = []

while True:
    # To turn off the program cleanly (without having to force quit it or keyboard interrupt etc.)
    k = 0
    for button in buttons.values():
        if button.is_pressed():
            k += 1
        if k >= 4:
            # Triggers if at least 4 buttons are pressed at once
            exit()

    # Update all LEDs
    for led in leds.values():
        led.update(state)

    # Run all the buttons' on_press() methods for the current state
    for button_key in buttons.keys():
        buttons[button_key].while_pressed(state)

    # Update the code instance (for displaying the code)
    code.update(state)

    # Update the queue instance (for flashing LEDs in sequence)
    queue.update(state)

    # State 1 (Main state) Behavior: Show, input, and guess code
    if state == 1:
        # Track input for buttons 1-4
        for i in range(1,5):
            button_key = f'BUTTON_{i}'
            if buttons[button_key].register_input():
                # inputs.append(button_key)
                inputs.append(i)  # Add the button's number

        # When button 6 is pressed, check if the code is right and reset the input list
        if buttons['BUTTON_5'].register_input():
            inputs_debug = []
            for inp in inputs:
                inputs_debug.append(f'BUTTON_{inp}')
            print(inputs_debug)

            if code.check_code(inputs):
                # Code is correct, enter success state (state 3)
                leds['LED_1'].flash(1, 0.3)  # Flash green for feedback
                leds['LED_5'].flash(1, 0.3)  # Flash green for feedback
                leds['LED_10'].flash(1, 0.3)  # Flash green for feedback

                state = 3
            else:  # Request new code, or guess is wrong
                leds['LED_4'].flash(1, 0.3)  # Flash red for feedback
                leds['LED_8'].flash(1, 0.3)  # Flash red for feedback
                leds['LED_9'].flash(1, 0.3)  # Flash red for feedback

                code.generate_code() # generate new code

                state = 2 # Enter display code state
                code.display_code() # display code

            inputs.clear() # reset inputs

    # State 2 Behavior: Show the code then return to main state (state 1)
    if state == 2:
        if code.display_finished: # Return to state 1 once the code has finshed being shown
            state = 1

    # State 3: Success State Behavior
    if state == 3:
        if buttons['BUTTON_6'].register_input():
            mode += 1
            if mode > modes_amount:
                mode = 1

            queue.clear()

        # TODO Mode logic
        if queue.queue_empty():
            leds_list = []

            if mode == 1:
                for i in range(10):
                    for led in leds.values():
                        queue.queue_add(led, 0.025, 0.005)
                for i in range(10):
                    queue.queue_add(leds.values(), 0.075, 0.075)
            elif mode == 2:
                for i in range(5,9):
                    leds_list.append(leds[f'LED_{i}'])
                queue.queue_add(leds_list, 1, 0.3)

                leds_list.clear()
                for i in range(1, 5):
                    leds_list.append(leds[f'LED_{i}'])
                for i in range(9, 11):
                    leds_list.append(leds[f'LED_{i}'])
                queue.queue_add(leds_list, 1, 0.3)

        if buttons['BUTTON_5'].is_pressed() and buttons['BUTTON_6'].is_pressed():
            # Exit success state when button 5 and 6 are pressed at the same time
            queue.clear()

            # TODO figure out flashing between states
            state = 1