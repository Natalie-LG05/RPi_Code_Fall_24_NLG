import RPi.GPIO as GPIO
from time import sleep
# import atexit

LED_R = 13
LED_Y = 16
LED_B = 6
LED_G = 12                                                      

BUTTON1 = 20
BUTTON2 = 19
BUTTON3 = 22
BUTTON4 = 21

GPIO.cleanup()
GPIO.setmode(GPIO.BCM) # sets config for gpio interface

GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_Y, GPIO.OUT)
GPIO.setup(LED_B, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)

GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    step1 = False
    step2 = False
    step3 = False
    step4 = False
    activated = False
    while True:
        b1 = GPIO.input(BUTTON1)
        b2 = GPIO.input(BUTTON2)
        b3 = GPIO.input(BUTTON3)
        b4 = GPIO.input(BUTTON4)

        GPIO.output(LED_R, GPIO.LOW)
        GPIO.output(LED_Y, GPIO.LOW)
        GPIO.output(LED_B, GPIO.LOW)
        GPIO.output(LED_G, GPIO.LOW)

        if b1 and b2:
            GPIO.output(LED_R, GPIO.HIGH)
        if b3 or b4:
            GPIO.output(LED_Y, GPIO.HIGH)

        if b1 : step1 = True
        if b3 and step1 : step2 = True
        if b4 and step2 : step3 = True
        if b2 and step3 : step4 = True
        if step4:
            activated = True
        if activated:
            GPIO.output(LED_R, GPIO.HIGH)
            GPIO.output(LED_Y, GPIO.HIGH)
            GPIO.output(LED_B, GPIO.HIGH)
            GPIO.output(LED_G, GPIO.HIGH)

            if b1 and b2 and b3 and b4:
                step1 = False
                step2 = False
                step3 = False
                step4 = False
                activated = False
        
except KeyboardInterrupt:
    GPIO.output(LED_R, GPIO.LOW)
    GPIO.output(LED_Y, GPIO.LOW)
    GPIO.output(LED_B, GPIO.LOW)
    GPIO.output(LED_G, GPIO.LOW)
    GPIO.cleanup()

# @atexit.register
# def on_close():
#         GPIO.output(LED_R, GPIO.LOW)
#         GPIO.output(LED_Y, GPIO.LOW)
#         GPIO.output(LED_B, GPIO.LOW)
#         GPIO.output(LED_G, GPIO.LOW)