'''
Andrew Welling
Project 2
Op Systems/Cloud Computing
'''

class Process:
    def __init__(self, id, duty, arrival_time, priority):
        '''
        :param int id: process id
        :param list duty: list of cpu and i/o times, formatted alternating
        :param int arrival_time: process arrival time
        :param int priority: process priority value
        '''
        self.id = id
        self.duty = duty
        self.arrival_time = arrival_time
        self.priority = priority
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = 0
        self.status = 'running'
        self.queue = 0 # queue number

    def get_id(self):
        return self.id
    def get_duty(self):
        return self.duty
    def get_burst_time(self,i=0):
        # i is the of value in duty that is changed
        return self.duty[i]
    def get_arrival_time(self):
        return self.arrival_time
    def get_priority(self):
        return self.priority
    def get_wait_time(self):
        return self.wait_time
    def get_turnaround_time(self):
        return self.turnaround_time
    def get_response_time(self):
        return self.response_time
    def get_status(self):
        return self.status
    def get_queue(self):
        return self.queue

    def set_duty(self, l):
        self.duty = l
    def set_burst_time(self,t,i=0):
        # i is the of value in duty that is changed
        self.duty[i] = t
    def set_arrival_time(self, t):
        self.arrival_time = t
    def set_priority(self, p):
        self.priority = p
    def set_wait_time(self, t):
        self.wait_time = t
    def set_turnaround_time(self, t):
        self.turnaround_time = t
    def set_response_time(self, t):
        self.response_time = t
    def set_status(self, s):
        self.status = s
    def set_queue(self, n):
        self.queue = n
