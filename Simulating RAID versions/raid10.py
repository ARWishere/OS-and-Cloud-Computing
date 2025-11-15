# andrew welling
from raid import RAID
import drive

# RAID 10
class RAID10(RAID):
    def __init__(self, num_drives, blocks, prob=0.0):
        """
        num_drives (int): num drives to build
        blocks (int): block size for each drive
        prob (int): probability of failure on read/write
        """
        if num_drives % 2 != 0 or num_drives < 4:
            raise ValueError("num drives must be a multiple of 2 and have at least 4 drives")
        drives = [drive.Drive(blocks) for _ in range(num_drives)]
        super().__init__(blocks, drives,num_drives,"RAID10", prob=prob)

    def write(self, block_ind, data):
        """
        write striped data to all drives
        block_ind (int): block index to write to on all drives
        data (list): data to write
        """
        stripped = self.strip(data)
        wrote = True
        for i, chunk in enumerate(stripped):
            drive_left = self.drives[2*i] # even drive indexes are a left drive in the pair
            drive_right = self.drives[2*i+1] # odd drive indexes are right, ex [d0,d1] is a pair
            if drive_left.is_failed() and drive_right.is_failed():
                wrote = False
                break # both drives failed, exit loop and raise an error
            if not drive_left.is_failed():
                drive_left.write(block_ind, chunk)
            if not drive_right.is_failed():
                drive_right.write(block_ind, chunk)

        if not wrote:
            raise IOError("write failure, a pair failed")

    def strip(self, data):
        """strip data to fit on n drives"""
        if len(data) % (len(self.drives) // 2) != 0:
            raise ValueError("len of data is not divisible by len of drive pairs")

        self.random_fail()
        num_pairs = len(self.drives) // 2
        chunk = len(data) // num_pairs

        stripped = []
        for i in range(num_pairs):
            start = i * chunk
            end = start + chunk
            stripped.append(data[start:end])

        return stripped

    def read(self, block_ind):
        """
        read data at block ind
        block_ind (int): block index to read from

        returns data read from all drives at a block
        """
        self.random_fail()
        data = []
        for drive in self.drives:
            if drive.is_failed():
                raise IOError('a drive failed, rebuild if possible')
            else:
                data.append(drive.read(block_ind))

        return data

    def rebuild(self,failed_ind):
        """
        rebuild a drive
        failed_ind (int): failed drive index to rebuild
        """
        for src in self.drives:
            if not src.is_failed():
                self.drives[failed_ind].blocks = src.blocks
                self.drives[failed_ind].recover()
                return
        raise IOError("all drives failed, unable to rebuild")


