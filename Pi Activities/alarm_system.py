# Natalie Gates; Pi Activity 4; 11/6/24 - 11/7/24
import RPi.GPIO as GPIO


# GPIO Pins
SENSOR = 17
LED = 16

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)


# Main
try:
    while True:
        if GPIO.input(SENSOR):
            print('Motion Detected')
            GPIO.output(LED, GPIO.HIGH)
        else:
            print('No Motion')
            GPIO.output(LED, GPIO.LOW)
except KeyboardInterrupt:
    GPIO.cleanup()

print('Goodbye. Ciao. Adios. Au Revoir.')