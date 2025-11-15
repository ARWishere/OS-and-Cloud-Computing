'''
Andrew Welling
Project 1
Op Systems/Cloud Computing
'''

class scheduler:
    def FCFS_scheduler(self, processes, ready, cpu, time=0, verbose=True):
        ''' non-preemptive FCFS scheduler '''
        # set start time to time
        start_time = time
        # pick process with lowest arrival time and remove it from ready
        if len(ready) == 0:  # if ready is empty, were in an idle state
            # so just add 1 to time and see if we have the next ready process
            time += 1
            self.add_ready(processes, ready, time)
        else:
            cur_process_ind = self.find_lowest_arrival(ready)
            cur_process = ready.pop(cur_process_ind)
            # while process is not finished
            while cur_process.get_burst_time() != 0:
                cur_process.set_burst_time(cur_process.get_burst_time() - 1)
                time += 1
                # add processes that arrived now to ready queue
                self.add_ready(processes, ready, time)
                # set end time to time
            end_time = time
            if verbose:
                print(str(len(cpu)) + ": process " + str(cur_process.get_id()) + " started at " + str(
                    start_time) + " finished at " + str(end_time))

            # update wait and turnaround times for the process
            cur_process.set_wait_time(start_time - cur_process.get_arrival_time())
            cur_process.set_turnaround_time(cur_process.get_wait_time() + (end_time - start_time))

            # add processID, start, end to CPU (this will be useful later)
            cpu.append(dict(process=cur_process.get_id(),
                            Wait=cur_process.get_wait_time(),
                            Turnaround=cur_process.get_turnaround_time(),
                            Start=start_time,
                            Finish=end_time,
                            Priority=cur_process.get_priority()))

        # return time
        return time

    def find_lowest_arrival(self, ready):
        return min(range(len(ready)), key=lambda i: ready[i].get_arrival_time())

    def add_ready(self, procs, ready, time):
        for p in procs:
            if p.get_arrival_time() == time and p not in ready:
                ready.append(p)

    def SJF_scheduler(self, processes, ready, cpu, time=0, verbose=True):
        ''' non-preemptive SJF scheduler '''
        # set start time to time
        start_time = time
        # pick process with lowest arrival time and remove it from ready
        if len(ready) == 0:  # if ready is empty, were in an idle state
            # so just add 1 to time and see if we have the next ready process
            time += 1
            self.add_ready(processes, ready, time)
        else:
            # pick process with shortest job time in ready queu
            cur_process_ind = self.find_shortest_job(ready)
            cur_process = ready.pop(cur_process_ind)
            # while process is not finished
            while cur_process.get_burst_time() != 0:
                cur_process.set_burst_time(cur_process.get_burst_time() - 1)
                time += 1
                # add processes that arrived now to ready queue
                self.add_ready(processes, ready, time)
            # set end time to time
            end_time = time
            if verbose:
                print("process " + str(cur_process.get_id()) + " started at " + str(start_time) + " finished at " + str(
                    end_time))

            # update wait and turnaround times for the process
            cur_process.set_wait_time(start_time - cur_process.get_arrival_time())
            cur_process.set_turnaround_time(cur_process.get_wait_time() + (end_time - start_time))

            # add processID, start, end to CPU (this will be useful later)
            cpu.append(dict(process=cur_process.get_id(),
                            Wait=cur_process.get_wait_time(),
                            Turnaround=cur_process.get_turnaround_time(),
                            Start=start_time,
                            Finish=end_time,
                            Priority=cur_process.get_priority()))

        # return time
        return time

    def find_shortest_job(self, ready):
        return min(range(len(ready)), key=lambda i: ready[i].get_burst_time())

    def priority_scheduler(self, processes, ready, cpu, time=0, verbose=True):
        ''' non-preemptive SJF scheduler '''
        # set start time to time
        start_time = time
        # pick process with lowest arrival time and remove it from ready
        if len(ready) == 0:  # if ready is empty, were in an idle state
            # so just add 1 to time and see if we have the next ready process
            time += 1
            self.add_ready(processes, ready, time)
        else:
            # pick process with shortest job time in ready queu
            cur_process_ind = self.find_priority_job(ready)
            cur_process = ready.pop(cur_process_ind)
            # while process is not finished
            while cur_process.get_burst_time() != 0:
                cur_process.set_burst_time(cur_process.get_burst_time() - 1)
                time += 1
                # add processes that arrived now to ready queue
                self.add_ready(processes, ready, time)
                # set end time to time
            end_time = time
            if verbose:
                print("process " + str(cur_process.get_id()) + " started at " + str(start_time) + " finished at " + str(
                    end_time))

            # update wait and turnaround times for the process
            cur_process.set_wait_time(start_time - cur_process.get_arrival_time())
            cur_process.set_turnaround_time(cur_process.get_wait_time() + (end_time - start_time))

            # add processID, start, end to CPU (this will be useful later)
            cpu.append(dict(process=cur_process.get_id(),
                            Wait=cur_process.get_wait_time(),
                            Turnaround=cur_process.get_turnaround_time(),
                            Start=start_time,
                            Finish=end_time,
                            Priority=cur_process.get_priority()))

        # return time
        return time

    def find_priority_job(self, ready):
        return max(range(len(ready)), key=lambda i: ready[i].get_priority())
