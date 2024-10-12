# Natalie Gates ; passcode/combination game

import RPi.GPIO as GPIO

# Define LED and button locations
LED1 = 5
LED2 = 6
LED3 = 7
LED4 = 8

BUTTON1 = 11
BUTTON2 = 12
BUTTON3 = 13
BUTTON4 = 14

LED_CORRECT = 9
LED_WRONG = 10
BUTTON_ENTER = 4
BUTTON_CHANGE_MODE = 15

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

while True:
    # Reset all LEDs
    GPIO.output(LED1, GPIO.LOW)
    GPIO.output(LED2, GPIO.LOW)
    GPIO.output(LED3, GPIO.LOW)
    GPIO.output(LED4, GPIO.LOW)
    GPIO.output(LED_CORRECT, GPIO.LOW)
    GPIO.output(LED_WRONG, GPIO.LOW)

    