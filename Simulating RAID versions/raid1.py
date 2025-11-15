# andrew welling
from raid import RAID
import drive

# RAID 1
class RAID1(RAID):
    def __init__(self, num_drives, blocks, prob=0.0):
        """
        num_drives (int): num drives to build
        blocks (int): block size for each drive
        prob (int): probability of failure on read/write
        """
        drives = [drive.Drive(blocks) for _ in range(num_drives)]
        super().__init__(blocks, drives,num_drives,"RAID1",prob=prob)

    def write(self, block_ind, data):
        """
        write to all drives
        block_ind (int): block index to write to on all drives
        data: data to write
        """
        self.random_fail()
        wrote = False
        for drive in self.drives:
            if not drive.is_failed():
                drive.write(block_ind, data)
                wrote = True
        if not wrote:
            raise IOError("all drives failed")

    def read(self, block_ind):
        """
        read data at block ind
        block_ind (int): block index to read from

        returns data read from drive
        """
        self.random_fail()
        data = []
        for drive in self.drives:
            if not drive.is_failed():
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


