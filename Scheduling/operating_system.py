'''
Andrew Welling
Project 2
Op Systems/Cloud Computing
'''

import process
import scheduler
import pandas as pd
class Operating_System:

    def processes_completed(self, procs, is_mfq):
        # if all processes have relevenat duty <= 0, return true
        if is_mfq:
            return sum(1 for p in procs if sum(p.get_duty()) == 0) == len(procs)
        else:
            return sum(1 for p in procs if p.get_burst_time() == 0) == len(procs)

    def kernel(self, sched, procs, quant=-1, verbose=True, mfq_schedulers=[[]]):
        '''
        :param Schedule sched: Scheduler object to be ran
        :param [] Process process: list of processes to run on scheduler
        :param (optional) boolean verbose: verbose mode, default true
        :param (optional) int quant: quant value passed to round robin scheduler
        :param (optional) mfq_schedulers: 2d list of schedulers and quantum values (if necessary)
        '''
        cpu = []
        ready = []
        time = 0
        # start with all processes with the lowest arrival time
        ready.extend([p for p in procs if p.get_arrival_time() == min(p.get_arrival_time() for p in procs)])
        time = ready[0].get_arrival_time() # if first proc does not start at 0, skip to its arrival time
        if len(mfq_schedulers[0]) == 0: # no provided mfq schedulers
            queues = [[] for _ in range(3)]
        else:
            queues = [[] for _ in range(len(mfq_schedulers))]
        waiting = []
        while self.processes_completed(procs, (sched.__func__ == scheduler.Scheduler.multilevel_feedback_queue)) is False:
            if len(ready) == 0: # if ready queue is empty, we need to add the next incomplete process
                for p in procs:
                    if p.get_arrival_time() >= time:
                        ready.append(p)
                        time = p.get_arrival_time()
            if sched.__func__ == scheduler.Scheduler.round_robin_scheduler:
                if quant > 0:
                    time = sched(procs, ready, cpu, quant, time, verbose)
                else:
                    raise Exception("quant value must be > 0") # no valid quant valid detected
            else:
                if sched.__func__ == scheduler.Scheduler.multilevel_feedback_queue:
                    time,queues,waiting = sched(procs, ready, cpu, time, verbose, mfq_schedulers,queues,waiting)
                else:
                    time = sched(procs, ready, cpu, time, verbose)
        df = pd.DataFrame(cpu)
        df.to_csv("results.csv", index=False)
        # calculate wait, turnaround, response here
        total_wt = 0
        total_rt = 0
        total_tt = 0
        # wt = (start[0]-arrival_time) + loop(start[x]-finish[x-1]
        # tt = wt + burst
        # rt = first_start_time - arrival_time

        for p in procs:
            wait_time = 0
            turnaround_time = 0
            response_time = -1
            prev_finish = p.get_arrival_time() # used for wait time calculations
            burst = 0
            for c in cpu:
                #print(cpu)
                if c['process'] == p.get_id():
                    wait_time += c['Start'] - prev_finish
                    burst += c['Finish'] - c['Start']
                    prev_finish = c['Finish']
                    if response_time == -1:
                        response_time = c['Start'] - p.get_arrival_time()

            turnaround_time = wait_time + burst
            print(f'stats for for {p.get_id()}: \n wait: {wait_time}    turnaround: {turnaround_time}    response: {response_time}')
            total_wt += wait_time
            total_tt += turnaround_time
            total_rt += response_time

        print('---------------------------------------------------------------------------------------------------------------------')
        print(f"average wait time: {total_wt/len(procs)}")
        print(f"average turnaround time: {total_tt/len(procs)}")
        print(f"average response time: {total_rt/len(procs)}")




#operating_system.kernel(0,True) # 0 = FCFS, 1 = SJF, 2 = priority