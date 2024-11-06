# Natalie Gates; Pi Activity 3; 11/4/24 - 11/7/24
from time import sleep, time
from random import random


# Set USING_SENSOR to False if we are simulating
# Set to True if you're using the sensor to pick up times
USING_SENSOR = False
DEBUG = False  # False to not print some messages, True to print some (debug) messages
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
def insertion_sort(list_):
    """
    Sorts a list using insertion sort
    \nCode was written and tested in a different document
    \nHowever this version expects every value to end with 'cm'
    """
    for i in range(1, len(list_)):  # Iterate through from the 2nd item to the last item
        if DEBUG:
            print(f'\t\t\tPass {i}; Sorting {list_[i]}')

        for j in range(i-1, -1, -1):  # Increment backwards starting to the left of the item being sorted
            if DEBUG:
                print(f'\t\t\t\tj={j}')
                print(f'\t\t\t\tComparing {list_[j+1]} with {list_[j]}')

            if float(list_[j][:-2]) > float(list_[j+1][:-2]):  # Need to trim the cm off each string value to perform comparison
                # Move the item over if it isn't in place
                list_[j], list_[j+1] = list_[j+1], list_[j]

                if DEBUG:
                    print(f'\t\t\t\tSwapping {list_[j+1]} and {list_[j]}')
                    print(f'\t\t\t\tList: {list_}')

            else:  # Item is in place; It is sorted
                if DEBUG:
                    print('\t\t\t\tBreaking')
                    print(f'\t\t\t\tList: {list_}')
                break


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

distances = []  # Initialize the list

input('Press enter to begin...')  # To pause program until user hits enter
print('Getting measurements...')


while True:
    print('Measuring...')
    if USING_SENSOR:
        # get the actual travel time of the sound wave
        # print('\tMeasuring with Sensor')  # \t is like \n but for indent/tabs instead of new lines
        travel_time = get_travel_time()
    else:
        # make up a travel time since we are simulating it (poorly lol)
        travel_time = random()  # generates a float from 0 to 1

    # determine how far it traveled
    raw_distance = calculate_raw_distance(travel_time)

    # adjust with the correction factor
    true_distance = raw_distance * correction_factor

    # add the distance to the list
    distances.append(f'{true_distance:.4f}cm')

    # output some info about what just happened
    print(f'\tTravel Time: {travel_time:.4f}sec')
    print(f'\tDistance: {true_distance:.4f}cm')

    # prompt for another
    i = input('\tGet another measurement? (Y/n):')
    if i in ['n', 'N', 'No', 'NO', 'stop']:
        break


print('Done')

# Output and sort the distances
print(f'Unsorted measurements: \n{distances:}')
insertion_sort(distances)  # sort the list
print(f'Sorted measurements: \n{distances:}')

if USING_SENSOR:
    GPIO.cleanup()