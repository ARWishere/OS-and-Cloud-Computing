# created by Andrew Welling
# A semaphore implementation using a condition variable
import threading

class Semaphore:
    def __init__(self, counter=1):
        self.counter = counter
        self.condition = threading.Condition()

    def acquire(self):
        with self.condition:
            self.counter -= 1
            if self.counter < 0:
                self.condition.wait()

    def release(self):
        with self.condition:
            self.counter += 1
            self.condition.notify()