# Natalie Gates ; passcode/combination game

import random
import RPi.GPIO as GPIO
from time import sleep

# Define LED and button locations
LED1 = 4
LED2 = 5
LED3 = 6
LED4 = 12
LEDs1 = [LED1, LED2, LED3, LED4]

BUTTON1 = 23
BUTTON2 = 22
BUTTON3 = 21
BUTTON4 = 20

LED_CORRECT = 13
LED_WRONG = 16
BUTTON_ENTER = 19
BUTTON_CHANGE_MODE = 18

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
amount_of_modes = 4

def flash_LED_random(LED, min_time, max_time):
    GPIO.output(LED, GPIO.HIGH)
    sleep(random.uniform(min_time, max_time))
    GPIO.output(LED, GPIO.LOW)
    # sleep(random.uniform(min_time, max_time))

def flash_LEDs(time):
    # Mode 2: Flash all LEDs at a given speed
    GPIO.output(LED1, GPIO.HIGH)
    GPIO.output(LED2, GPIO.HIGH)
    GPIO.output(LED3, GPIO.HIGH)
    GPIO.output(LED4, GPIO.HIGH)
    sleep(time)

    GPIO.output(LED1, GPIO.LOW)
    GPIO.output(LED2, GPIO.LOW)
    GPIO.output(LED3, GPIO.LOW)
    GPIO.output(LED4, GPIO.LOW)
    sleep(time)

def success_protocol():
    # execute protocol based on the current mode
    if mode == 1:
        # Mode 1: Turn on all LEDs
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.output(LED3, GPIO.HIGH)
        GPIO.output(LED4, GPIO.HIGH)
    elif mode == 2:
        # Mode 2: Flash all LEDs slowly
        flash_LEDs(1)
    elif mode == 3:
        # Mode 2: Flash all LEDs fast
        flash_LEDs(0.05)
    elif mode == 4:
        flash_LED_random(LEDs1[random.randint(0,3)], 0.01, 1.5)

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
            GPIO.output(LED_CORRECT, GPIO.HIGH)
            GPIO.output(LED_WRONG, GPIO.HIGH)
            mode += 1
            if mode > amount_of_modes:
                mode = 1
            sleep(time_between_inputs)
            # GPIO.output(LED_CORRECT, GPIO.LOW)
            GPIO.output(LED_WRONG, GPIO.LOW)

        if is_solved:
            success_protocol()
except KeyboardInterrupt:
    # debugging
    print(inputs)

    # (attempt to) reset everything
    GPIO.output(LED1, GPIO.LOW)
    GPIO.output(LED2, GPIO.LOW)
    GPIO.output(LED3, GPIO.LOW)
    GPIO.output(LED4, GPIO.LOW)
    GPIO.output(LED_CORRECT, GPIO.LOW)
    GPIO.output(LED_WRONG, GPIO.LOW)
    GPIO.cleanup()