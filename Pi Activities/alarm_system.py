# Natalie Gates; Pi Activity 4; 11/6/24 - 11/7/24

import time
import RPi.GPIO as GPIO


DISARM_TIME = 3  # Time (in seconds) to press disarm the alarm before it goes off

# GPIO Pins
SENSOR = 17
LED = 16
BUTTON = 18

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(LED, GPIO.LOW)  # Make sure the LED starts off


# Main
print('Alarm Ready\n\n')
try:
    while True:
        if GPIO.input(SENSOR):
            print('Motion Detected')

            start_time = time.time()
            disarmed = False
            while time.time() - start_time < DISARM_TIME:
                if GPIO.input(BUTTON):
                    disarmed = True
                    print('\tDisarmed successfully')
                    break

            if not disarmed:
                GPIO.output(LED, GPIO.HIGH)
                print('\tIntruder Alert!!!!!!!')

            input('\tPress enter to re-arm ')
            print('Alarm Ready\n\n')

except KeyboardInterrupt:
    GPIO.cleanup()
    print('Goodbye. Ciao. Adios. Au Revoir.')