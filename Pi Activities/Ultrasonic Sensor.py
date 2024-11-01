from time import sleep, time
from random import random

# Set USING_SENSOR to False if we are simulating
# Set to True if you're using the sensor to pick up times
USING_SENSOR = False
DEBUG = False  # False to not print some messages, True to print some (debug) messages
SETTLE_TIME = 2  # 2 seconds to settle the sensor from when the program starts running
CALIBRATIONS = 5
CALIBRATION_DELAY = 1  # pause for 1 seconds between calibrations
TRIG_DURATION = 0.00001  # seconds
SPEED_OF_SOUND = 343  # m/s

if USING_SENSOR:
    # sensor setup
    import RPi.GPIO as GPIO

    # pins
    TRIG = 25
    ECHO = 24

    # pin setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

# functions
def get_travel_time():
    """
    Gets the time in seconds that it takes for a signal to travel from the sensor to an object and back
    """

def calculate_raw_distance(travel_time):
    """
    :param travel_time: Takes in the travel time of a signal
    :return: Returns the distance in cm between the ultrasonic sensor and another object
    """

def calibrate():
   """
    Calibrates the sensor
    :return: Returns a correction factor for our measurements
   """

def settle():
    """
    Allows the sensor to settle for the specified `SETTLE_TIME`
    """

##### Main Code #####
if USING_SENSOR:
    settle()
    correction_factor = calibrate()
else:
    # in the case of just simulating it
    correction_factor = 1

input('Press enter to begin...')  # To pause program until user hits enter
print('Getting measurements...')

while True:
    if USING_SENSOR:
        # get the actual travel time of the sound wave
        print('\tMeasuring with Sensor')  # \t is like \n but for indent/tabs instead of new lines
        travel_time = get_travel_time()
    else:
        # make up a travel time since we are simulating it (poorly lol)
        travel_time = random()  # generates a float from 0 to 1

    # determine how far it traveled
    raw_distance = calculate_raw_distance(travel_time)

    # adjust with the correction factor
    true_distance = raw_distance * correction_factor

    # output some info about what just happened
    print(f'\t\tTravel Time: {travel_time:.4f}sec')
    print(f'\t\tDistance: {true_distance:.4f}cm')

    # prompt for another
    i = input("Continue? (Y/n) ")
    if i in ['n', 'N', 'No', 'NO', 'stop']:
        break

print('done')
if USING_SENSOR:
    GPIO.cleanup()