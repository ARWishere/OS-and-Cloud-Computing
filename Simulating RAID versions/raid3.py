# andrew welling
from raid import RAID
import drive


class RAID3(RAID):
    def __init__(self, num_drives, blocks, prob=0.0):
        """
        num_drives (int): num drives to build
        blocks (int): block size for each drive
        prob (int): probability of failure on read/write
        """
        drives = [drive.Drive(blocks) for _ in range(num_drives)]

        super().__init__(blocks, drives, num_drives, raid_model="RAID3", prob=prob)

    def int_to_bits(self, n):
        # Convert integer to bits of len 4
        return [int(b) for b in format(n, '04b')]

    def bits_to_int(self, bits):
        return int("".join(str(b) for b in bits), 2)

    def write(self, block_ind, data):
        """
        write bits from some data to all drives
        block_ind (int): block index to begin to write to, 4 blocks will be used for 4 bits
        data (int): int to write to a block
        """
        self.random_fail()
        bits = self.int_to_bits(data)
        parity = 0
        for i, bit in enumerate(bits):
            if self.drives[i].is_failed():
                raise IOError('a drive failed, rebuild if possible')
            self.drives[i].write(block_ind, bit)
            parity ^= bit # repeatedly use xor on each to get the parity bit
        self.drives[-1].write(block_ind, parity) # write parity to parity drive

    def read(self, block_ind):
        """
        read data at a block index across all drives
        block_ind (int): block index to get data from
        returns (list): bit data across the block
        """
        self.random_fail()
        data = []
        for drive in self.drives:
            if drive.is_failed():
                raise IOError('a drive failed, rebuild if possible')
            else:
                data.append(drive.read(block_ind))

        return data

    def get_values(self):
        """
        read data across all blocks
        block_ind (int): block index to get data from
        returns: int data across all block
        """
        vals = []
        for block in range(self.drives[0].cur_size):
            vals.append(self.bits_to_int(self.read(block)[0:4]))
        return vals

    def rebuild(self, failed_ind):
        """rebuild a drive using bit/xors"""
        for block in range(self.drives[0].cur_size): # iterate over currently full blocks
            bits = []
            parity = 0
            for i in range(self.num_drives - 1):
                bit = self.drives[i].read(block) if not self.drives[i].is_failed() else None
                bits.append(bit)
                if i != failed_ind and bit is not None:
                    parity ^= bit

            if failed_ind == self.num_drives - 1:
                self.drives[-1].write(block, parity) # write to parity drive
                self.drives[-1].recover()
            else:
                recovered_bit = parity ^ self.drives[-1].read(block)
                self.drives[failed_ind].write(block, recovered_bit)
                self.drives[failed_ind].recover()
