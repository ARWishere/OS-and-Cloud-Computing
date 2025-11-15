# andrew welling
from raid import RAID
import drive


from raid import RAID
import drive


class RAID5(RAID):
    def __init__(self, num_drives, blocks, prob=0.0):
        """
        num_drives (int): num drives to build
        blocks (int): block size for each drive
        prob (int): probability of failure on read/write
        """
        drives = [drive.Drive(blocks) for _ in range(num_drives)]
        super().__init__(blocks, drives, num_drives, raid_model="RAID5", prob=prob)

    def write(self, block_ind, data):
        """
        write bits from some data to all drives
        block_ind (int): block index to write to
        data (list): data to write to a block, must be num_drive-1 length
        """
        self.random_fail()
        parity_drive = self.num_drives - 1 - (block_ind % self.num_drives)
        parity = 0
        # we need to track current position in data list to continue writing despite parity block
        data_index = 0

        for i in range(self.num_drives):
            if i == parity_drive: # dont write to parity drive yet
                continue
            if self.drives[i].is_failed():
                raise IOError('a drive failed, rebuild if possible')
            block_value = data[data_index]
            self.drives[i].write(block_ind, block_value)
            parity ^= block_value
            data_index += 1

        self.drives[parity_drive].write(block_ind, parity)

    def read(self, block_ind):
        """
        read data at a block index across all drives
        block_ind (int): block index to get data from
        returns: data across all drives at a block
        """
        self.random_fail()
        data = []
        parity_drive = self.num_drives - 1 - (block_ind % self.num_drives)
        for i in range(self.num_drives):
            if self.drives[i].is_failed():
                raise IOError('a drive failed, rebuild if possible')
            else:
                if i != parity_drive:
                    data.append(self.drives[i].read(block_ind))

        return data

    def rebuild(self, failed_ind):
        """
        rebuild failed drive at drive index
        """
        for block_ind in range(self.num_blocks):
            parity_drive = self.num_drives - 1 - (block_ind % self.num_drives)
            if failed_ind == parity_drive:
                # rebuild parity drive
                parity = 0
                for i in range(self.num_drives):
                    if i != parity_drive:
                        parity ^= self.drives[i].read(block_ind)
                self.drives[failed_ind].write(block_ind, parity)
                self.drives[failed_ind].recover()
            else:
                # for data drives
                missing_data = self.drives[parity_drive].read(block_ind)
                for i in range(self.num_drives):
                    if i != parity_drive and i != failed_ind:
                        missing_data ^= self.drives[i].read(block_ind)
                self.drives[failed_ind].write(block_ind, missing_data)
                self.drives[failed_ind].recover()


