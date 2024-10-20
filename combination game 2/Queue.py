# Natalie Gates ; Queue class

class Queue:
    def __init__(self, leds):
        self.queue = []
        self.queue_times = []

        self.leds = leds

    def update(self, state):
        # Flash LEDs when previous is finished
        # If the previous led has finished, flash the next one (if there is a next one)
        if self.previous_finished and len(self.queue):
            self.queue[0].flash(self.queue_times[0][0], self.queue_times[0][1])
            self.queue.pop()

    def previous_finished(self):
        """ Checks if any LEDs are currently in the middle of flashing """
        for led in self.leds.values():
            if led.flashing:
                return False
        return True

    def queue_empty(self):
        return len(self.queue) == 0

    def queue_add(self, led, time, end_time = 0):
        """ Adds LED to the end of the queue """
        self.queue.append(led)
        self.queue_times.append((time, end_time))

    def pop(self):
        self.queue.pop(0)
        self.queue_times.pop(0)