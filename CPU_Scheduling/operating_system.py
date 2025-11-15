'''
Andrew Welling
Project 1
Op Systems/Cloud Computing
'''

import process
import scheduler
import pandas as pd
class operating_system:
    def kernel(self, sched, procs, verbose=True):
        '''
        :param Schedule sched: Scheduler object to be ran
        :param [] Process process: list of processes to run on scheduler
        :param boolean verbose: verbose mode, default true
        '''
        cpu = []
        ready = []
        time = 0
        # start with all processes with the lowest arrival time
        ready.extend([p for p in procs if p.get_arrival_time() == min(p.get_arrival_time() for p in procs)])
        time = ready[0].get_arrival_time() # if first proc does not start at 0, skip to its arrival time
        while len(cpu) != len(procs):
            if len(ready) == 0: # if ready queue is empty, we need to add the next incomplete process
                for p in procs:
                    if p.get_arrival_time() >= time:
                        ready.append(p)
                        time = p.get_arrival_time()
            time = sched(procs,ready,cpu,time,verbose)
        print(cpu)
        df = pd.DataFrame(cpu)
        df.to_csv("results.csv", index=False)

#operating_system.kernel(0,True) # 0 = FCFS, 1 = SJF, 2 = priority