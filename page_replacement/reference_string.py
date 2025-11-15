# andrew welling
# reference string generator
import random


class Reference_String:
    def __init__(self):
        self.ran = random.Random()

    def generate_nonlocal(self, length):
        #  generates a reference string without locality
        results = []
        while len(results) < length:
            val = self.ran.randint(0,length)
            results.append(val)
        return results

    def generate_local(self, length):
        #  generates a reference string with locality
        results = []
        for i in range(length):
            val = self.ran.randint(-3,3) + i
            if val < 0:
                val = 1
            if val >= length:
                val = length-1
            results.append(val)

        return results