# andrew welling
from raid import RAID
import drive


# RAID 0
class RAID0(RAID):
    def __init__(self, num_drives, blocks,prob=0.0):
        """
        num_drives (int): num drives to build
        blocks (int): block size for each drive
        prob (int): probability of failure on read/write
        """
        drives = [drive.Drive(blocks) for _ in range(num_drives)]
        super().__init__(blocks, drives,num_drives,"RAID0",prob=prob)

    def write(self, block_ind, data):
        """
        write striped data to all drives
        block_ind (int): block index to write to on all drives
        data (list): data to write
        """
        self.random_fail()
        wrote = False
        stripped = self.strip(data)  # strip the data across all drives
        for i, drive in enumerate(self.drives):
            if not drive.is_failed():
                drive.write(block_ind, stripped[i])
                wrote = True
            else:
                wrote = False

        if not wrote:
            raise IOError("write failure, a drive failed")

    def strip(self, data):
        """strip data to fit on n drives"""
        if len(data) % len(self.drives) != 0:
            raise ValueError("len of data is not divisible by len of drives")
        chunk = len(data) // len(self.drives)

        stripped = []
        for i in range(len(self.drives)):
            start = i * chunk
            end = start + chunk
            stripped.append(data[start:end])

        return stripped

    def read(self, block_ind):
        """
        read data at block ind
        block_ind (int): block index to read from

        returns data read from all drives at block ind
        """
        self.random_fail()
        data = []
        for drive in self.drives:
            if not drive.is_failed():
                data.append(drive.read(block_ind))
        return data

    def rebuild(self,failed_ind):
        """rebuild is not possible on raid0"""
        pass
