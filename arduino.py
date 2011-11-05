#coding: utf-8

from serial import Serial
from serial import SerialException
from collections import defaultdict
from math import floor, ceil
from time import sleep 

class Arduino(Serial):
    """The Arduino class communicates with the arduino board and
    builds a string of random bits. Hold the state of the algs"""


    def __init__(self, port="/dev/ttyUSB0", baudrate=9600, p=3):
        Serial.__init__(self, port, baudrate)
        self.pin = p

    def readint(self):
        """Catch OSError because the Arudino tends to be become 'unavailible' and
        check if we read a digit because we sometimes get malformed strings.
        TODO: fix this"""
        self.write("POLL " + str(self.pin))
        while True:
            try:
                i = self.readline()[:-2]
                if i.isdigit():
                    return int(i)
            except OSError as e:
                print "OSError sleeping for 10 secs \n", e
                sleep(10)
    def poll(self):
        self.write("POLL " + str(self.pin))
        return self.readline()[:-2]

    def meanrand(self, n):
        """The Mean-RAND algorithm. Generates a 0-bit if the value read is below the mean
        of the last b values. Two bits are generated and ran through a Neumann box"""
        bufsize = 100                   # b
        buf = [0]*bufsize

        # Fill buffer with initial values
        for i in range(len(buf)):
            buf[i] = self.readint()

        meanval = float(sum(buf))/bufsize
        for i in xrange(n):
            if i%50==0:
                print i
            # Remove the old value, adjust mean, read new val, adjust again
            meanval -= buf[i%bufsize]/bufsize
            buf[i%bufsize] = self.readint()
            meanval += buf[i%bufsize]/bufsize
            m = int(ceil(meanval))

            """Generate two bits and run them through a von Neumann box.
            00/11 → discard, 10 → 1, 01 → 0"""
            while True:
                b0 = 1 if self.readint() > m else 0
                b1 = 1 if self.readint() > m else 0
                if b0 == b1:
                    continue
                else:
                    break
            if b0 == 1:
                yield '1'
            else:
                yield '0'

class StatTests:
    def __init__(self, bitstring):
        self.s = bitstring
    def monobit(self):
        n = len(self.s)
        n0 = len([a for a in self.s if a == '0'])
        n1 = n-n0
        print n, n0, n1
        return float((n0-n1)**2)/n
    def twobit(self):
        pass
    def poker(self):
        pass
    def runs(self):
        pass
    def autocorrelation(self):
        pass

class RawData:
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
