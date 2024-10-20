# Natalie Gates ; rpi passcode game

import RPi.GPIO as GPIO
import atexit  # For exit handling

# Classes for components
from Led import Led
from Button import Button

from Code import Code

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
}

buttons = {
    # First set of Buttons
    'BUTTON_1': Button(23, led_md1=leds["LED_1"]),  # green
    'BUTTON_2': Button(22, led_md1=leds["LED_2"]),  # blue
    'BUTTON_3': Button(21, led_md1=leds["LED_3"]),  # yellow
    'BUTTON_4': Button(20, led_md1=leds["LED_4"]),  # red

    'BUTTON_5': Button(19),  # enter button
    'BUTTON_6': Button(18),  # change mode button
}

# Setup the code
code = Code(leds)

# Exit handler
@atexit.register
def on_exit():
    print('Closing!')
    for led_ in leds.values():
        led_.off()
    GPIO.cleanup()

# Main Code
print('Starting!')
# The current Mode, or State, of the program
state = 1  # Begin in mode 1

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

    # Run all the buttons' on_press() methods for the current state/mode
    for button_key in buttons.keys():
        buttons[button_key].while_pressed(state)

    # Update the code instance (for displaying the code)
    code.update(state)

    # Mode (state) 1 behavior
    # State 1 (Main state): Show, input, and guess code
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
                # TODO Flash green for feedback
                # Code is correct, enter success state (state 3)
                state = 3
                # TODO Success Protocol
            else:  # Request new code, or guess is wrong
                leds['LED_8'].flash(2)  # Flash red for feedback
                code.generate_code() # generate new code

                state = 2 # Enter display code state
                code.display_code() # display code

            inputs.clear() # reset inputs

    # Mode 2 behavior;
    # State 2: Show the code then return to main state (state 1)
    if state == 2:
        if code.display_finished: # Return to state 1 once the code has finshed being shown
            state = 1

    # Mode 3 behavior;
    # State 3: Success State
    if state == 3:
        #TODO Success Protocol
        #TODO 6th Button Functionality
        for i in range(5,9):
            leds[f'LED_{i}'].flash(1)
        state = 1