# Natalie Gates ; passcode/combination game

import RPi.GPIO as GPIO
from time import sleep

# Define LED and button locations
LED1 = 13
LED2 = 16
LED3 = 6
LED4 = 12

BUTTON1 = 20
BUTTON2 = 19
BUTTON3 = 22
BUTTON4 = 21

LED_CORRECT = 5
LED_WRONG = 4
BUTTON_ENTER = 18
BUTTON_CHANGE_MODE = 23

# Setup components
# GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)

GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(LED_CORRECT, GPIO.OUT)
GPIO.setup(LED_WRONG, GPIO.OUT)
GPIO.setup(BUTTON_ENTER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_CHANGE_MODE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Logic variable initialization
time_between_inputs = 0.25

code = [1, 4, 3, 2]
inputs = []
is_solved = False

mode = 1
amount_of_modes = 3

def success_protocol():
    sleep(time_between_inputs)

    # execute protocol based on the current mode
    match mode:
        case 1:
            # Mode 1: Turn on all LEDs
            GPIO.output(LED1, GPIO.HIGH)
            GPIO.output(LED2, GPIO.HIGH)
            GPIO.output(LED3, GPIO.HIGH)
            GPIO.output(LED4, GPIO.HIGH)
        case 2:
            flash_time = 1
            # Mode 2: Flash all LEDs slowly
            GPIO.output(LED1, GPIO.HIGH)
            GPIO.output(LED2, GPIO.HIGH)
            GPIO.output(LED3, GPIO.HIGH)
            GPIO.output(LED4, GPIO.HIGH)
            sleep(flash_time)

            GPIO.output(LED1, GPIO.LOW)
            GPIO.output(LED2, GPIO.LOW)
            GPIO.output(LED3, GPIO.LOW)
            GPIO.output(LED4, GPIO.LOW)
            sleep(flash_time)
        case 3:
            flash_time = 0.05
            # Mode 2: Flash all LEDs fast
            GPIO.output(LED1, GPIO.HIGH)
            GPIO.output(LED2, GPIO.HIGH)
            GPIO.output(LED3, GPIO.HIGH)
            GPIO.output(LED4, GPIO.HIGH)
            sleep(flash_time)

            GPIO.output(LED1, GPIO.LOW)
            GPIO.output(LED2, GPIO.LOW)
            GPIO.output(LED3, GPIO.LOW)
            GPIO.output(LED4, GPIO.LOW)
            sleep(flash_time)
        case _:
            #error probably
            pass

try:
    while True:
        if not is_solved:
            # Reset all LEDs
            GPIO.output(LED1, GPIO.LOW)
            GPIO.output(LED2, GPIO.LOW)
            GPIO.output(LED3, GPIO.LOW)
            GPIO.output(LED4, GPIO.LOW)
            GPIO.output(LED_CORRECT, GPIO.LOW)
            GPIO.output(LED_WRONG, GPIO.LOW)

            # When a button is pressed, light up its corresponding LED and save the input
            if GPIO.input(BUTTON1):
                GPIO.output(LED1, GPIO.HIGH)
                inputs.append(1)
                sleep(time_between_inputs)
            if GPIO.input(BUTTON2):
                GPIO.output(LED2, GPIO.HIGH)
                inputs.append(2)
                sleep(time_between_inputs)
            if GPIO.input(BUTTON3):
                GPIO.output(LED3, GPIO.HIGH)
                inputs.append(3)
                sleep(time_between_inputs)
            if GPIO.input(BUTTON4):
                GPIO.output(LED4, GPIO.HIGH)
                inputs.append(4)
                sleep(time_between_inputs)
        elif is_solved:
            success_protocol()

        if GPIO.input(BUTTON_ENTER):
            if not is_solved:
                # Debugging
                print(inputs)

                # When the enter button is pressed, check if the code is correct
                if inputs == code:
                    # code is right, flash green and then activate success protocol
                    GPIO.output(LED_CORRECT, GPIO.HIGH)
                    is_solved = True # Enter the solved state
                else:
                    # code is wrong, flash red
                    GPIO.output(LED_WRONG, GPIO.HIGH)
                inputs = []
                sleep(time_between_inputs)
            else:
                is_solved = False # Exit the solved state
                sleep(time_between_inputs)

        if GPIO.input(BUTTON_CHANGE_MODE):
            mode += 1
            if mode > amount_of_modes:
                mode = 1
except KeyboardInterrupt:
    # debugging
    print(inputs)

    # reset everything
    GPIO.output(LED1, GPIO.LOW)
    GPIO.output(LED2, GPIO.LOW)
    GPIO.output(LED3, GPIO.LOW)
    GPIO.output(LED4, GPIO.LOW)
    GPIO.output(LED_CORRECT, GPIO.LOW)
    GPIO.output(LED_WRONG, GPIO.LOW)
    GPIO.cleanup()