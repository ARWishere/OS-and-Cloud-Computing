'''
Andrew Welling
Project 1
Op Systems/Cloud Computing
'''

class process:
    def __init__(self, id, burst_time, arrival_time, priority):
        self.id = id
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.priority = priority
        self.wait_time = 0
        self.turnaround_time = 0

    def get_id(self):
        return self.id
    def get_burst_time(self):
        return self.burst_time
    def get_arrival_time(self):
        return self.arrival_time
    def get_priority(self):
        return self.priority
    def get_wait_time(self):
        return self.wait_time
    def get_turnaround_time(self):
        return self.turnaround_time

    def set_burst_time(self, t):
        self.burst_time = t
    def set_arrival_time(self, t):
        self.arrival_time = t
    def set_priority(self, p):
        self.priority = p
    def set_wait_time(self, t):
        self.wait_time = t
    def set_turnaround_time(self, t):
        self.turnaround_time = t
