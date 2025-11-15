# created by Andrew Welling
# Buffer threading example with the consumer/producer problem
import semaphore
import threading
import time
import random

class Buffer:
    def __init__(self):
        self.S = semaphore.Semaphore(1) # mutex
        self.E = semaphore.Semaphore(10) # size
        self.F = semaphore.Semaphore(0) # currently full spots
        self.buffer = []

    def produce_data(self):
        return len(self.buffer)

    def consume_data(self):
        self.buffer.pop()

    def producer(self):
        data = self.produce_data()
        self.E.acquire()
        self.S.acquire()
        self.buffer.append(data)
        print(f"buffer is len {len(self.buffer)}")
        self.S.release()
        self.F.release()

    def consumer(self):
        self.F.acquire()
        self.S.acquire()
        self.consume_data()
        print(f"buffer is len {len(self.buffer)}")
        self.S.release()
        self.E.release()

    def consumer_loop(self):
        while True:
            time.sleep(random.uniform(0.1, 0.5))
            self.consumer()

    def producer_loop(self):
        while True:
            time.sleep(random.uniform(0.1, 0.5))
            self.producer()

b = Buffer()
t1 = threading.Thread(target=b.producer_loop)
t2 = threading.Thread(target=b.consumer_loop)

t1.start()
t2.start()

t1.join()
t2.join()