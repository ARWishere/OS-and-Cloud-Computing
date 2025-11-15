# andrew welling
# simulates a drive to store data

import random

class Drive:
    def __init__(self, size):
        """
        init a drive with size num of blocks
        size (int): num of blocks on the drive.
        """
        self.size = size
        self.blocks = [0] * size
        self.failed = False
        self.drive_writes = 0
        self.failures = 0
        self.cur_size = 0 # current full blocks in drive

    def get_blocks(self):
        return self.blocks

    def write(self, block_index, data):
        if 0 <= block_index < self.size:
            self.drive_writes += 1
            self.blocks[block_index] = data
            if not self.failed:
                self.cur_size += 1
        else:
            raise IndexError("cant write block, index out of range")

    def read(self, block_index):
        if 0 <= block_index < self.size:
            return self.blocks[block_index]
        else:
            raise IndexError("cant read block, index out of range")

    def fail(self):
        """force the drive to fail"""
        self.failed = True
        self.failures += 1
        self.blocks = [0] * self.size # reset blocks

    def recover(self):
        """recover data"""
        self.failed = False

    def is_failed(self):
        return self.failed

    def get_writes(self):
        """track drive writes for comparison"""
        return self.drive_writes

    def get_failures(self):
        """track drive failures for comparison"""
        return self.failures




