# Natalie Gates; Pi Activity 3; 11/4/24 - 11/5/24

from time import sleep, time
from random import random

# Set USING_SENSOR to False if we are simulating
# Set to True if you're using the sensor to pick up times
USING_SENSOR = True
DEBUG = True  # False to not print some messages, True to print some (debug) messages
SETTLE_TIME = 2  # 2 seconds to settle the sensor from when the program starts running
CALIBRATIONS = 5  # amount of calibration tests to do
CALIBRATION_DELAY = 1  # pause for 1 seconds between calibrations
TRIG_DURATION = 0.00001  # seconds
SPEED_OF_SOUND = 343  # in m/s

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
def get_travel_time() -> float:
    """
    Gets the time in seconds that it takes for a signal to travel from the sensor to an object and back
    """

    # Trigger the sensor
    GPIO.output(TRIG, GPIO.HIGH)
    sleep(TRIG_DURATION)
    GPIO.output(TRIG, GPIO.LOW)

    if DEBUG:
        print('\t\tGetting travel time')

    # wait for the echo to start
    while GPIO.input(ECHO) == GPIO.LOW:
        start = time()

    # Wait for the echo to finish
    while GPIO.input(ECHO) == GPIO.HIGH:
        end = time()

    if DEBUG:
        print(f'\t\tMeasured travel time: {end - start}')

    duration = end - start
    return duration


def calculate_raw_distance(travel_time):
    """
    :param travel_time: Takes in the travel time of a signal
    :return: Returns the distance in cm between the ultrasonic sensor and another object
    """

    distance = travel_time * SPEED_OF_SOUND  # distance in meters
    distance /= 2  # divide by two since the sound traveled there and back
    distance *= 100  # convert to cm

    if DEBUG:
        print(f'\t\tMeasured raw distance: {distance}cm')

    return distance


def calibrate():
   """
    Calibrates the sensor
    :return: Returns a correction factor for our measurements
   """

   print('Calibrating...')
   print('\tPlace the sensor a measured distance away from an object')

   known_distance = float(input('\tWhat is the measured distance (cm)?: '))

   print('\tGetting calibration measurements...')

   distance_avg = 0
   for _ in range(CALIBRATIONS):  # note the _ used
       travel_time = get_travel_time()
       raw_distance = calculate_raw_distance(travel_time)
       distance_avg += raw_distance
       sleep(CALIBRATION_DELAY)

   distance_avg /= CALIBRATIONS

   correction_factor = known_distance / distance_avg

   if DEBUG:
       print(f'\t\tAverage distance: {distance_avg}')
       print(f'\t\tCorrection factor: {correction_factor}')

   print('Done Calibrating\n')
   return correction_factor


def settle():
    """
    Allows the sensor to settle for the specified `SETTLE_TIME`
    """

    print(f'Waiting for sensor to settle - {SETTLE_TIME}sec')
    GPIO.output(TRIG, GPIO.LOW)
    sleep(SETTLE_TIME)


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