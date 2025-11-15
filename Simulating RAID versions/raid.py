# andrew welling
import random

import drive

# this is a RAID superclass to enable multiple raid implementations
class RAID:
    def __init__(self, blocks, drives, num_drives, raid_model, prob=0.0):
        """
        drives (list of drive): drives in the raid implementation
        blocks (int): num blocks on each drive
        num_drives (int): num drives
        raid_model (str): name of raid model (i.e. raid0, raid1)
        prob (float): probability of failure during an operation
        """
        self.num_blocks = blocks
        self.drives = drives
        self.name = raid_model
        self.num_drives = num_drives
        self.prob = prob
        self.failed = False # whether the system has completely failed

    def write(self, block_index, data):
        """
        write data to a block on some drives, depends on raid implementation
        """
        pass

    def read(self, block_index):
        """
        read data for a block index, depends on raid implementation
        """
        pass

    def rebuild(self, failed_drive_index):
        """
        rebuild a failed drive, depends on raid implementation
        """
        pass

    def drive_statuses(self):
        """
        get failure status of all drive
        """
        return [drive.is_failed() for drive in self.drives]

    def failed_drives(self):
        """get indices of current failed drives"""
        return [i for i, val in enumerate(self.drive_statuses()) if val]

    def fail_drive(self, index):
        """
        fail a drive
        """
        self.drives[index].fail()

    def recover_drive(self, index):
        """
        recover a drive
        """
        self.drives[index].recover()

    def random_fail(self):
        """a random failure during operations using probability"""
        # use self.prob on each drive to see if it fails,
        for drive in self.drives:
            if random.random() < self.prob:
                drive.fail()

    def get_writes(self):
        return sum([drive.get_writes() for drive in self.drives])

    def get_failures(self):
        return sum([drive.get_failures() for drive in self.drives])

    def __str__(self):
        # rewrite my str method as it is faulty
        # drive.read() returns the block data across all drives
        # i want to print the data for each drive in a readable way

        output = []
        output.append(f"{self.name} status:")
        for i, drive in enumerate(self.drives):
            status = "fail" if drive.is_failed() else "alive"
            output.append(f"drive {i} "
                          f"[{status}]: "
                          f"{[drive.read(block) for block in range(self.num_blocks)]}")
        output.append('\n')
        return "\n".join(output)