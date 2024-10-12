# Natalie Gates ; passcode/combination game

import RPi.GPIO as GPIO

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
GPIO.cleanup()
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
code = []
inputs = []
mode = 0

try:
    while True:
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
        if GPIO.input(BUTTON2):
            GPIO.output(LED2, GPIO.HIGH)
            inputs.append(2)
        if GPIO.input(BUTTON3):
            GPIO.output(LED3, GPIO.HIGH)
            inputs.append(3)
        if GPIO.input(BUTTON4):
            GPIO.output(LED4, GPIO.HIGH)
            inputs.append(4)
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