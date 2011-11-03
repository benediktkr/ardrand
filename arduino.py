from serial import Serial
from serial import SerialException
from collections import defaultdict
from math import floor, ceil

class Arduino(Serial):
    """The Arduino class communicates with the arduino board and
    builds a string of random bits. Hold the state of the algs"""
    
    bufsize = 100
    buffer = [0]*bufsize
    meanval = 0.0
    pin = 3

    def __init__(self, p=3):
        pin = p
        for i range len(buffer):
            past[i] = self.readint()

        meanval = float(sum(buffer))/bufsize

    def readint(self):
        self.write("POLL " + str(pin))
        return int(self.readline()[:-2])

    def poll(self):
        self.write("POLL " + str(pin))
        return self.readline()[:-2]

    def meanrand(self, n):
        """Generator that generates n supposedly random bits"""
        for i in xrange(n):
            # Remove the old value, adjust mean, read new val, adjust again
            meanval -= buffer[i%bufsize]/bufsize
            buffer[i%bufsize] = self.readint()
            meanval += buffer[i%bufsize]/bufsize
            m = int(math.ceil(meanval))

            """The von Neumann box. 00/11 → discard, 10 → 1, 01 → 0"""
            while True:
                b0 = 1 if self.readint() > m else 0
                b1 = 1 if self.readint() > 0 else 0
                if b0 == b1:
                    continue
                else:
                    break
            if b0 == 1:
                yield 1
            else:
                yield 0

class Data:
    def __init__(self, l):
        self.data = l
        self.count = len(self.data)
        self.mean = float(sum(self.data))/self.count
            
    def freq(self):
        freqs = defaultdict(int)
        for x in self.data:
            freqs[x] += 1

        # The uniformity factor is how many of the numbers are AT the mean or below
        m = int(floor(self.mean))
        factor = float(sum([freqs[a] for a in freqs if a <= m]))/self.count
        return (freqs, factor)
    
    def correlation(self):
        corr = []
        for i in range(1, len(self.data)):
            # Absolute value?
            corr.append(self.data[i] - self.data[i-1]) 
        return corr
