# andrew welling
from raid import RAID
import drive

class RAID6(RAID):
    def __init__(self, num_drives, blocks, prob=0.0):
        """
        num_drives (int): num drives to build
        blocks (int): block size for each drive
        prob (int): probability of failure on read/write
        """
        if num_drives < 4:
            raise IOError("RAID 6 requires at least 4 drives")
        drives = [drive.Drive(blocks) for _ in range(num_drives)]
        super().__init__(blocks, drives, num_drives, raid_model="RAID6", prob=prob)

    def write(self, block_ind, data):
        """
        write numbers to all drives with two parity blocks
        data: list of (num_drives - 2) integers
        """
        if len(data) != self.num_drives - 2:
            raise ValueError("len of data must be num_drives - 2")

        self.random_fail()
        p_drive = self.num_drives - 2
        q_drive = self.num_drives - 1

        p = 0
        q = 0

        data_index = 0
        for i in range(self.num_drives):
            if i == p_drive or i == q_drive:
                continue

            if self.drives[i].is_failed():
                raise IOError('a drive failed, rebuild if possible')
            val = data[data_index]
            self.drives[i].write(block_ind, val)

            p += val # p is sum of blocks across all drives
            q += (data_index + 1) * val # use weighted value by index/a polynomial type thing with blocks * index+1 matrix
            data_index += 1

        self.drives[p_drive].write(block_ind, p)
        self.drives[q_drive].write(block_ind, q)

    def read(self, block_ind):
        """
        read data from all drives
        """
        self.random_fail()
        data = []
        for i in range(self.num_drives - 2):
            if self.drives[i].is_failed():
                raise IOError('a data drive failed, rebuild if possible')
            data.append(self.drives[i].read(block_ind))
        return data

    def rebuild(self, failed_ind):
        """rebuild one failed drive at drive index"""
        for block_ind in range(self.num_blocks):
            p_drive = self.num_drives - 2
            q_drive = self.num_drives - 1

            if failed_ind == p_drive:
                # rebuild p drive
                total = 0
                for i in range(self.num_drives):
                    if i != p_drive and i != q_drive:
                        total += self.drives[i].read(block_ind)
                self.drives[p_drive].write(block_ind, total)
                self.drives[p_drive].recover()

            elif failed_ind == q_drive:
                # rebuild q drive
                weighted = 0
                data_index = 0
                for i in range(self.num_drives):
                    if i != p_drive and i != q_drive:
                        val = self.drives[i].read(block_ind)
                        weighted += (data_index + 1) * val
                        data_index += 1
                self.drives[q_drive].write(block_ind, weighted)
                self.drives[q_drive].recover()

            else:
                # rebuild a data drive
                total = 0
                for i in range(self.num_drives):
                    if i != p_drive and i != q_drive and i != failed_ind:
                        total += self.drives[i].read(block_ind)
                p_val = self.drives[p_drive].read(block_ind)
                missing_val = p_val - total
                self.drives[failed_ind].write(block_ind, missing_val)
                self.drives[failed_ind].recover()

    def rebuild_multiple_drives(self, failed_drives):
        """rebuild multiple drives (2 for raid6)"""
        drive_1 = failed_drives[0]
        drive_2 = failed_drives[1]
        for block_ind in range(self.num_blocks):
            p_drive = self.num_drives - 2
            q_drive = self.num_drives - 1

            # on both parity drives
            if not (drive_1 != p_drive and drive_1 != q_drive) and not (drive_2 != p_drive and drive_2 != q_drive):
                # recompute both parity drives
                total = 0
                weighted = 0
                data_index = 0
                for i in range(self.num_drives):
                    if i != p_drive and i != q_drive:
                        val = self.drives[i].read(block_ind)
                        total += val
                        weighted += (data_index + 1) * val
                        data_index += 1
                self.drives[p_drive].write(block_ind, total)
                self.drives[q_drive].write(block_ind, weighted)
                self.drives[p_drive].recover()
                self.drives(q_drive).recover()

            # on just one parity drive and one data drive
            elif (drive_1 != p_drive and drive_1 != q_drive) != (drive_2 != p_drive and drive_2 != q_drive):
                data_drive = drive_1 if drive_1 != p_drive and drive_1 != q_drive else drive_2
                parity_drive = drive_2 if drive_1 != p_drive and drive_1 != q_drive else drive_1

                total = 0
                weighted = 0
                data_index = 0
                for i in range(self.num_drives):
                    if i != p_drive and i != q_drive and i != data_drive:
                        val = self.drives[i].read(block_ind)
                        total += val
                        weighted += (data_index + 1) * val
                        data_index += 1

                # rebuild missing data drive from other parity
                p_val = self.drives[p_drive].read(block_ind) if parity_drive != p_drive else total
                missing_val = p_val - total
                self.drives[data_drive].write(block_ind, missing_val)
                self.drives[data_drive].recover()

                # rebuild parity drive
                if parity_drive == p_drive:
                    # rebuild p
                    self.drives[p_drive].write(block_ind, p_val)
                    self.drives[p_drive].recover()
                else:
                    # rebuild q
                    data_vals = []
                    data_index = 0
                    for i in range(self.num_drives):
                        if i != p_drive and i != q_drive:
                            val = self.drives[i].read(block_ind)
                            data_vals.append((data_index + 1, val))
                            data_index += 1
                    q_val = sum(i * v for i, v in data_vals)
                    self.drives[q_drive].write(block_ind, q_val)
                    self.drives[q_drive].recover()

            # if both are data drives
            else:
                # get known values and recalculate p and q
                known_vals = []
                missing_indices = []
                data_index = 0
                for i in range(self.num_drives):
                    if i == p_drive or i == q_drive:
                        continue
                    if i != drive_1 and i != drive_2:
                        val = self.drives[i].read(block_ind)
                        known_vals.append((data_index + 1, val))
                    else:
                        missing_indices.append(data_index + 1)
                    data_index += 1

                sum_known = sum(val for _, val in known_vals)
                weighted_known = sum(i * val for i, val in known_vals)

                p_val = self.drives[p_drive].read(block_ind)
                q_val = self.drives[q_drive].read(block_ind)

                # x,y = vals at i,j
                i, j = missing_indices
                eq1 = p_val - sum_known  # x + y
                eq2 = q_val - weighted_known  # i*x + j*y

                # x + y = eq1
                # i*x + j*y = eq2
                # so x = (eq2 - j*eq1) / (i - j)
                x = (eq2 - j * eq1) // (i-j)
                y = eq1 - x

                # write back into failed drives
                written = 0
                for i in range(self.num_drives):
                    if i == drive_1 or i == drive_2:
                        val = x if written == 0 else y
                        self.drives[i].write(block_ind, val)
                        self.drives[i].recover()
                        written += 1
