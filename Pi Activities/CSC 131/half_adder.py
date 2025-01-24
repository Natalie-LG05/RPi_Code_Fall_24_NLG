import RPi.GPIO as GPIO

BUTTON_A = 5
BUTTON_B = 25
LED_S = 17
LED_C = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_A, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(BUTTON_B, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LED_S, GPIO.OUT)
GPIO.setup(LED_C, GPIO.OUT)

try:
    while True:
        A, B, S, C = 0, 0, 0, 0

        if GPIO.input(BUTTON_A):
            A = 1
        if GPIO.input(BUTTON_B):
            B = 1

        S = A ^ B
        C = A & B

        GPIO.output(LED_S, S)
        GPIO.output(LED_C, C)

except KeyboardInterrupt:
    GPIO.cleanup()
