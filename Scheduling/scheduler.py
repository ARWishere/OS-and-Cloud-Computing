'''
Andrew Welling
Project 2
Op Systems/Cloud Computing
'''
import scheduler


class Scheduler:
    # non pre-emptive methods
    def FCFS_scheduler(self, processes, ready, cpu, time=0, verbose=True, waiting_queue=[],queues=[[]]):
        """
        FCFS Scheduler

        Args:
            processes (list): List of process objects.
            ready (list): List of processes ready for execution.
            cpu (list): List tracking executed processes and their statistics.
            time (int, optional): Current time in the scheduler. Defaults to 0.
            verbose (bool, optional): If True, prints execution details. Defaults to True.
            waiting_queue (list, optional): Processes waiting for I/O. Defaults to [].
            queues (list, optional): Multi-level queue structure.

        Returns:
            int: new time after running
        """
        # set start time to time
        start_time = time
        # pick process with lowest arrival time and remove it from ready
        if len(ready) == 0:  # if ready is empty, were in an idle state
            # so just add 1 to time and see if we have the next ready process
            time += 1
            self.add_ready(processes, ready, time)
            self.decrement_waiting(waiting_queue, queues) # this line is used for the mfq
        else:
            cur_process_ind = self.find_lowest_arrival(ready)
            cur_process = ready.pop(cur_process_ind)
            if cur_process.get_status() != 'running':
                cur_process.set_status('running')
            # while process is not finished
            while cur_process.get_burst_time() != 0:
                cur_process.set_burst_time(cur_process.get_burst_time() - 1)
                time += 1
                # add processes that arrived now to ready queue
                self.add_ready(processes, ready, time)
                self.decrement_waiting(waiting_queue, queues)
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
            cur_duty = self.get_current_duty_ind(p)
            if cur_duty is not None and cur_duty % 2 == 0:
                if p.get_arrival_time() == time and p not in ready and p.get_burst_time(cur_duty) > 0:
                    ready.append(p)

    def SJF_scheduler(self, processes, ready, cpu, time=0, verbose=True, waiting_queue=[],queues=[[]]):
        """
        SJF Scheduler

        Args:
            processes (list): List of process objects.
            ready (list): List of processes ready for execution.
            cpu (list): List tracking executed processes and their statistics.
            time (int, optional): Current time in the scheduler. Defaults to 0.
            verbose (bool, optional): If True, prints execution details. Defaults to True.
            waiting_queue (list, optional): Processes waiting for I/O. Defaults to [].
            queues (list, optional): Multi-level queue structure.

        Returns:
            int: new time after running
        """
        # set start time to time
        start_time = time
        # pick process with lowest arrival time and remove it from ready
        if len(ready) == 0:  # if ready is empty, were in an idle state
            # so just add 1 to time and see if we have the next ready process
            time += 1
            self.add_ready(processes, ready, time)
            self.decrement_waiting(waiting_queue, queues)
        else:
            # pick process with shortest job time in ready queu
            cur_process_ind = self.find_shortest_job(ready)
            cur_process = ready.pop(cur_process_ind)
            if cur_process.get_status() != 'running':
                cur_process.set_status('running')
            # while process is not finished
            while cur_process.get_burst_time() != 0:
                cur_process.set_burst_time(cur_process.get_burst_time() - 1)
                time += 1
                # add processes that arrived now to ready queue
                self.add_ready(processes, ready, time)
                self.decrement_waiting(waiting_queue, queues)
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

    # helper method to find shortest job in ready queue
    def find_shortest_job(self, ready):
        return min(range(len(ready)), key=lambda i: ready[i].get_burst_time())

    def priority_scheduler(self, processes, ready, cpu, time=0, verbose=True,waiting_queue=[],queues=[[]]):
        """
        Priority Scheduler

        Args:
            processes (list): List of process objects.
            ready (list): List of processes ready for execution.
            cpu (list): List tracking executed processes and their statistics.
            time (int, optional): Current time in the scheduler. Defaults to 0.
            verbose (bool, optional): If True, prints execution details. Defaults to True.
            waiting_queue (list, optional): Processes waiting for I/O. Defaults to [].
            queues (list, optional): Multi-level queue structure.

        Returns:
            int: new time after running
        """
        # set start time to time
        start_time = time
        if len(ready) == 0:  # if ready is empty, were in an idle state
            # so just add 1 to time and see if we have the next ready process
            time += 1
            self.add_ready(processes, ready, time)
            self.decrement_waiting(waiting_queue, queues)
        else:
            # pick process with shortest job time in ready queu
            cur_process_ind = self.find_priority_job(ready)
            cur_process = ready.pop(cur_process_ind)
            if cur_process.get_status() != 'running':
                cur_process.set_status('running')
            # while process is not finished
            while cur_process.get_burst_time() != 0:
                cur_process.set_burst_time(cur_process.get_burst_time() - 1)
                time += 1
                # add processes that arrived now to ready queue
                self.add_ready(processes, ready, time)
                self.decrement_waiting(waiting_queue, queues)
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

    # helper method to find job with highes priority
    def find_priority_job(self, ready):
        return max(range(len(ready)), key=lambda i: ready[i].get_priority())

    # preemptive methods follow from here
    def round_robin_scheduler(self, processes, ready, cpu, quant, time=0, verbose=True,waiting_queue=[],queues=[[]]):
        """
        Round Robin Scheduler

        Args:
            processes (list): List of process objects.
            ready (list): List of processes ready for execution.
            cpu (list): List tracking executed processes and their statistics.
            quant (int): Time slice each process will run for
            time (int, optional): Current time in the scheduler. Defaults to 0.
            verbose (bool, optional): If True, prints execution details. Defaults to True.
            waiting_queue (list, optional): Processes waiting for I/O. Defaults to [].
            queues (list, optional): Multi-level queue structure.

        Returns:
            int: new time after running
        """
        # set start time to time
        start_time = time
        # pick process with lowest arrival time and remove it from ready
        if len(ready) == 0:  # if ready is empty, were in an idle state
            # so just add 1 to time and see if we have the next ready process
            time += 1
            self.add_ready(processes, ready, time)
            self.decrement_waiting(waiting_queue,queues)
        else:
            cur_process = ready.pop(0) # use the val at front of queue
            if cur_process.get_status() != 'running':
                cur_process.set_status('running')
            t_slice = min(quant,cur_process.get_burst_time())
            # update process time accordingly
            for _ in range(t_slice):
                cur_process.set_burst_time(cur_process.get_burst_time() - 1, self.get_current_duty_ind(cur_process))
                time += 1
                # add processes that have newly arrived
                self.add_ready(processes, ready, time)
                self.decrement_waiting(waiting_queue, queues)

            if cur_process.get_burst_time() > 0 and not self.check_completion(cur_process):
                ready.append(cur_process)

            # set end time to time
            end_time = time
            if verbose:
                print(str(len(cpu)) + ": process " + str(cur_process.get_id()) + " started at " + str(
                    start_time) + " finished at " + str(end_time))

            # add processID, start, end to CPU (this will be useful later)
            cpu.append(dict(process=cur_process.get_id(),
                            Start=start_time,
                            Finish=end_time,
                            Priority=cur_process.get_priority()))

        # return time
        return time

    def srt_scheduler(self, processes, ready, cpu, time=0, verbose=True, waiting_queue=[],queues=[[]]):
        """
        SRT Scheduler

        Args:
            processes (list): List of process objects.
            ready (list): List of processes ready for execution.
            cpu (list): List tracking executed processes and their statistics.
            time (int, optional): Current time in the scheduler. Defaults to 0.
            verbose (bool, optional): If True, prints execution details. Defaults to True.
            waiting_queue (list, optional): Processes waiting for I/O. Defaults to [].
            queues (list, optional): Multi-level queue structure.

        Returns:
            int: new time after running
        """
        # set start time to time
        start_time = time
        if len(ready) == 0:  # if ready is empty, were in an idle state
            # so just add 1 to time and see if we have the next ready process
            time += 1
            self.add_ready(processes, ready, time)
            self.decrement_waiting(waiting_queue, queues)
        else:
            cur_process_ind = self.find_lowest_time(ready)
            cur_process = ready[cur_process_ind]
            if cur_process.get_status() != 'running':
                cur_process.set_status('running')
            # while process is not finished or a new process came into the queue with lower burst
            while cur_process.get_burst_time() > 0:
                if cur_process_ind != self.find_lowest_time(ready):  # check for pre emption
                    break
                cur_process.set_burst_time(cur_process.get_burst_time() - 1)
                time += 1
                # add processes that arrived now to ready queue
                self.add_ready(processes, ready, time)
                self.decrement_waiting(waiting_queue, queues)

            # if process is done, remove it from ready
            if cur_process.get_burst_time() == 0:
                ready.pop(cur_process_ind)

            end_time = time # set end time to time

            if verbose:
                print(str(len(cpu)) + ": process " + str(cur_process.get_id()) + " started at " + str(
                    start_time) + " finished at " + str(end_time))

            # add processID, start, end to CPU (this will be useful later)
            cpu.append(dict(process=cur_process.get_id(),
                            Start=start_time,
                            Finish=end_time,
                            Priority=cur_process.get_priority()))

        # return time
        return time

    # helper method to find processes in the ready queue with the lowest remaining burst time
    def find_lowest_time(self, ready):
        return min(range(len(ready)), key=lambda i: ready[i].get_burst_time())


    def preemptive_priority_scheduler(self, processes, ready, cpu, time=0, verbose=True, waiting_queue=[],queues=[[]]):
        """
        Preemptive Priority Scheduler

        Args:
            processes (list): List of process objects.
            ready (list): List of processes ready for execution.
            cpu (list): List tracking executed processes and their statistics.
            time (int, optional): Current time in the scheduler. Defaults to 0.
            verbose (bool, optional): If True, prints execution details. Defaults to True.
            waiting_queue (list, optional): Processes waiting for I/O. Defaults to [].
            queues (list, optional): Multi-level queue structure.

        Returns:
            int: new time after running
        """
        # set start time to time
        start_time = time
        if len(ready) == 0:  # if ready is empty, were in an idle state
            # so just add 1 to time and see if we have the next ready process
            time += 1
            self.add_ready(processes, ready, time)
            self.decrement_waiting(waiting_queue, queues)
        else:
            cur_process_ind = self.find_priority_job(ready)
            cur_process = ready[cur_process_ind]
            if cur_process.get_status() != 'running':
                cur_process.set_status('running')
            # while process is not finished or a new process with higher priority isnt ready
            while cur_process.get_burst_time() != 0:
                if cur_process_ind != self.find_priority_job(ready):  # check for pre emption
                    break
                cur_process.set_burst_time(cur_process.get_burst_time() - 1)
                time += 1
                # add processes that arrived now to ready queue
                self.add_ready(processes, ready, time)
                self.decrement_waiting(waiting_queue, queues)
            if cur_process.get_burst_time() == 0: # if process is done, remove it from ready
                ready.pop(cur_process_ind)
            end_time = time # set end time to time
            if verbose:
                print(str(len(cpu)) + ": process " + str(cur_process.get_id()) + " started at " + str(
                    start_time) + " finished at " + str(end_time))


            # add processID, start, end to CPU (this will be useful later)
            cpu.append(dict(process=cur_process.get_id(),
                            Start=start_time,
                            Finish=end_time,
                            Priority=cur_process.get_priority()))

        # return time
        return time

    # decrement the waiting queue
    def decrement_waiting(self, waiting_queue, queues):
        for process in waiting_queue[:]:  # iter over a copy to modify and replace it
            if process.get_status() != 'waiting':
                process.set_status('waiting')

            duty = process.get_duty()
            duty_ind = self.get_current_duty_ind(process)
            if duty_ind is None: # remove from waiting on this case
                waiting_queue.remove(process)

            if duty[duty_ind] > 0:
                duty[duty_ind] -= 1  # decrement i/o
                process.set_duty(duty)
                if duty[duty_ind] <= 0:
                    waiting_queue.remove(process)
                    if not self.check_completion(process): # if process still is not finished
                        queues[process.get_queue()].append(process)  # return it to its queue
            else: # remove it
                waiting_queue.remove(process)
                if not self.check_completion(process):  # if process still is not finished
                    queues[process.get_queue()].append(process)  # return it to its queue

    # helper functions for the mfq:
    # gets the current i/o or cpu time that a process should be running
    def get_current_duty_ind(self, process):
        duty = process.get_duty()
        for d_ind in range(len(process.get_duty())):
            if duty[d_ind] > 0:
                return d_ind

    # move a process into a lower queue
    def move_to_lower(self, process, queues):
        cur_queue = process.get_queue()
        if process in queues[cur_queue]: # remove from cur queue
            queues[cur_queue].remove(process)
        queues[cur_queue+1].append(process) # add to lower one

    # move a process into waiting
    def move_to_waiting(self, process, waiting_queue, queues):
        if not self.check_completion(process):
            waiting_queue.append(process)
            process.set_queue(process.get_queue())  # remember which queue it was in
            if process in queues[process.get_queue()]: # remove it from the queue (in case its still in there)
                queues[process.get_queue()].remove(process)

    # check if a process is completed
    def check_completion(self,process):
        return sum(process.get_duty()) == 0

    # returns a new queue with only unfinished processes
    def remove_finished_processes(self,queue):
        return [p for p in queue if not self.check_completion(p)]


    # check if all queues above some queue are empty
    # this is to check if
    def upper_queues_clear(self, i, queues):
        return sum(1 for q_ind in range(0,i-1) if len(queues[q_ind]) == 0) == 0
    def multilevel_feedback_queue(self, processes, ready, cpu, time=0, verbose=True, schedulers=[[]],queues=[[]],waiting_queue=[]):
        """
        multilevel feedback queue

        Args:
            processes (list): List of process objects.
            ready (list): List of processes ready for execution.
            cpu (list): List tracking executed processes and their statistics.
            time (int, optional): Current time in the scheduler. Defaults to 0.
            verbose (bool, optional): If True, prints execution details. Defaults to True.
            schedulers (list, options): list of schedulers to be used, if none run assignment program
            queues (list, optional): Multi-level queue structure.
            waiting_queue (list, optional): Processes waiting for I/O. Defaults to [].

        Returns:
            int: new time after running
        """
        if len(schedulers[0]) == 0:
        # ORIGINAL CODE FOR THE ASSIGNMENT STARTS HERE
            self.add_ready(processes, queues[0], time)

            if queues[0]: # first round robin scheduler
                cur_process = queues[0][0]
                duty = cur_process.get_duty()
                cur_duty = self.get_current_duty_ind(cur_process)
                if cur_duty % 2 == 0: # on even duty, use cpu time, if its not, it should be waiting (which is handled seperate)
                    time = self.round_robin_scheduler(processes, queues[0], cpu, quant=2, time=time, verbose=verbose,waiting_queue=waiting_queue,queues=queues)

                    if queues[0] and duty[cur_duty] > 0:  # process is unfinished, so move it lower
                        self.move_to_lower(cur_process, queues)

                    if len(duty) > cur_duty - 1 and duty[cur_duty] == 0: # if process still has i/o
                        self.move_to_waiting(cur_process,waiting_queue,queues)

            elif queues[1]: # second round robin scheduler
                cur_process = queues[1][0]
                duty = cur_process.get_duty()
                cur_duty = self.get_current_duty_ind(cur_process)
                if cur_duty % 2 == 0:
                    time = self.round_robin_scheduler(processes, queues[1], cpu, quant=10, time=time, verbose=verbose,waiting_queue=waiting_queue,queues=queues)

                    if queues[1] and duty[cur_duty] > 0:
                        self.move_to_lower(cur_process, queues)

                    if len(duty) > cur_duty - 1 and duty[cur_duty] == 0:
                        self.move_to_waiting(cur_process, waiting_queue, queues)

            elif queues[2]: # final fcfs scheduler
                cur_process = queues[2][0]
                duty = cur_process.get_duty()
                cur_duty = self.get_current_duty_ind(cur_process)
                if cur_duty % 2 == 0:
                    time = self.FCFS_scheduler(processes, queues[2], cpu, time=time, verbose=verbose,waiting_queue=waiting_queue,queues=queues)

                    if len(duty) > cur_duty - 1 and duty[cur_duty] == 0:
                        self.move_to_waiting(cur_process, waiting_queue, queues)

            if not any(queues) and waiting_queue:  # idle state if only waiting processes exist
                time += 1
                self.add_ready(processes, queues[0], time)
                self.decrement_waiting(waiting_queue,queues)

            return time, queues, waiting_queue

        else:
            # EXTENSION CODE BEGINS HERE
            # set up queues

            self.add_ready(processes, queues[0], time)
            # iterate over schedulers
            for i,s in enumerate(schedulers):
                queues[i] = self.remove_finished_processes(queues[i])
                sched = s[0]
                if i == 0 and queues[0]: # the first queue and scheduler
                    cur_process = queues[0][0]
                    duty = cur_process.get_duty()
                    cur_duty = self.get_current_duty_ind(cur_process)

                    if cur_duty % 2 == 0:  # on even duty, use cpu time, if its not, it should be waiting (which is handled seperate
                        if sched.__func__ is self.round_robin_scheduler.__func__:
                            time = self.round_robin_scheduler(processes, queues[0], cpu, quant=s[1], time=time,
                                                              verbose=verbose, waiting_queue=waiting_queue,
                                                              queues=queues)
                        else:
                            time = sched(processes, queues[0], cpu, time=time, verbose=verbose, waiting_queue=waiting_queue, queues=queues)

                        if queues[0] and duty[cur_duty] > 0:  # process is unfinished, so move it lower
                            self.move_to_lower(cur_process, queues)

                        if len(duty) > cur_duty - 1 and duty[cur_duty] == 0:
                            self.move_to_waiting(cur_process, waiting_queue, queues)

                elif i == len(schedulers)-1 and queues[i]: # this means were at the last scheduler
                    cur_process = queues[i][0]
                    duty = cur_process.get_duty()
                    cur_duty = self.get_current_duty_ind(cur_process)
                    if cur_duty % 2 == 0:
                        if sched.__func__ is self.round_robin_scheduler.__func__:
                            time = self.round_robin_scheduler(processes, queues[i], cpu, quant=s[1], time=time,
                                                              verbose=verbose, waiting_queue=waiting_queue,
                                                              queues=queues)
                        else:
                            time = sched(processes, queues[i], cpu, time=time, verbose=verbose, waiting_queue=waiting_queue, queues=queues)

                        if len(duty) > cur_duty - 1 and duty[cur_duty] == 0:
                            self.move_to_waiting(cur_process, waiting_queue, queues)

                else: # this means were somewhere in the middle
                    # check if the current queue is the one we should be using and that the queue is not empty
                    if self.upper_queues_clear(i,queues) and queues[i]:
                        cur_process = queues[i][0]
                        duty = cur_process.get_duty()
                        cur_duty = self.get_current_duty_ind(cur_process)

                        if cur_duty % 2 == 0:  # on even duty, use cpu time, if its not, it should be waiting (which is handled seperate
                            if sched.__func__ is self.round_robin_scheduler.__func__:
                                time = self.round_robin_scheduler(processes, queues[i], cpu, quant=s[1], time=time,
                                                                  verbose=verbose, waiting_queue=waiting_queue,
                                                                  queues=queues)
                            else:
                                time = sched(processes, queues[i], cpu, time=time, verbose=verbose,
                                             waiting_queue=waiting_queue, queues=queues)

                            if queues[i] and duty[cur_duty] > 0:  # process is unfinished, so move it lower
                                self.move_to_lower(cur_process, queues)

                            if len(duty) > cur_duty - 1 and duty[cur_duty] == 0:
                                self.move_to_waiting(cur_process, waiting_queue, queues)

                        if cur_duty % 2 == 1: # should be in waiting, not here
                            self.move_to_waiting(cur_process, waiting_queue, queues)


            if not any(queues) and waiting_queue:  # idle state if only waiting processes exist
                time += 1
                self.add_ready(processes, queues[0], time)
                self.decrement_waiting(waiting_queue,queues)

            return time, queues, waiting_queue
