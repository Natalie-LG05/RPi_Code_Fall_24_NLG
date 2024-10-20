# Natalie Gates ; Queue class

class Queue:
    def __init__(self, leds):
        self.queue = []  # Acts as a queue/stack; furthest right element ([-1]) is considered first/on top
        self.queue_times = []  # Store the flash durations for each led in queue (in the same order)
        # ^ Could just use a tuple with 3 elements instead

        self.leds = leds

    def update(self, state):
        # Flash LEDs when previous is finished
        # If the previous led has finished, flash the next one (if there is a next one)
        if self.previous_finished() and (not self.queue_empty()):
            # print(f'Flashing LED: {self.queue[0]}')
            if hasattr(self.queue[0], '__len__'):
                # If a list of LEDs was queued:
                for led in self.queue[0]:
                    led.flash(self.queue_times[0][0], self.queue_times[0][1])
            else:
                # If only 1 LED was queued:
                self.queue[0].flash(self.queue_times[0][0], self.queue_times[0][1])

            self.pop()

    def previous_finished(self):
        """ Checks if any LEDs are currently in the middle of flashing """
        for led in self.leds.values():
            if led.flashing:
                return False
        # print('No LED is flashing')
        return True

    def queue_empty(self):
        return len(self.queue) == 0

    def queue_add(self, leds, time, end_time = 0):
        """ Adds LED to the end of the queue """
        self.queue.append(leds)
        self.queue_times.append((time, end_time))

    def pop(self):
        # print(self.queue)
        self.queue.pop(0)
        self.queue_times.pop(0)
        # print(self.queue)