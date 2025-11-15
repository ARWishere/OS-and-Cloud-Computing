# andrew welling
from raid import RAID
import drive


class RAID4(RAID):
    def __init__(self, num_drives, blocks, prob=0.0):
        """
        num_drives (int): num drives to build
        blocks (int): block size for each drive
        prob (int): probability of failure on read/write
        """
        drives = [drive.Drive(blocks) for _ in range(num_drives)]

        super().__init__(blocks, drives, num_drives, raid_model="RAID4", prob=prob)

    def write(self, block_ind, data):
        """
        write bits from some data to all drives
        block_ind (int): block index to write to
        data (list): data to write to a block
        """
        self.random_fail()
        parity = 0
        for i, value in enumerate(data):
            if self.drives[i].is_failed():
                raise IOError('a drive failed, rebuild if possible')
            self.drives[i].write(block_ind, value)
            parity ^= value

        self.drives[-1].write(block_ind, parity)

    def read(self, block_ind):
        """
        read data at a block index across all drives
        block_ind (int): block index to get data from
        returns: data across all drives at a block
        """
        self.random_fail()
        data = []
        for i in range(self.num_drives-1):
            if self.drives[i].is_failed():
                raise IOError('a drive failed, rebuild if possible')
            else:
                data.append(self.drives[i].read(block_ind))

        return data

    def rebuild(self, failed_ind):
        """
        rebuild failed drive at drive index using parity drive
        """
        for block_index in range(self.num_blocks):
            if failed_ind == self.num_drives - 1:
                # for parity
                parity = 0
                for i in range(self.num_drives - 1):
                    parity ^= self.drives[i].read(block_index)
                self.drives[failed_ind].write(block_index, parity)
                self.drives[failed_ind].recover()
            else:
                # for a data drive
                parity = self.drives[-1].read(block_index)
                for i in range(self.num_drives - 1):
                    if i != failed_ind:
                        parity ^= self.drives[i].read(block_index)
                self.drives[failed_ind].write(block_index, parity)
                self.drives[failed_ind].recover()
