#coding: utf-8

from serial import Serial
from serial import SerialException
from collections import defaultdict, deque 
from math import floor, ceil
from time import sleep
from sys import stdout

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
        buf = deque([0]*bufsize)

        # Fill buffer with initial values
        print "Initializing..."
        for i in range(len(buf)):
            buf[i] = self.readint()

        meanval = float(sum(buf))/bufsize
        print "...done"
        
        for i in xrange(n):
            if i%50==0:
                print i

            """Generate two bits and run them through a von Neumann box.
            00/11 → discard, 10 → 1, 01 → 0"""
            while True:
                meanval -= float(buf.popleft())/bufsize
                buf.append(self.readint())
                meanval += float(buf[-1])/bufsize
                m = int(ceil(meanval))

                b0 = 1 if self.readint() > m else 0
                b1 = 1 if self.readint() > m else 0
                if b0 == b1:
                    #print b0, "discarded over", m, " or ", meanval, " fresh reading: ", self.readint()
                    continue
                else:
                    #print "accepted", b0
                    break
            if b0 == 1:
                yield '1'
            else:
                yield '0'

    def updownrand(self, n):
        """First read a value v_0. Then use it to determine if next bit v_1 is 1 or 0. If we have v_1 > v_0
        for the new value v_1 then we generate a 1, otherwise a 0. In order to determine v_1 we read two
        values and apply the vN box

        Thoughts:
        v_1 == v_0 → discard?

        20k 108m58.164s"""

        v0 = self.readint()
        for i in xrange(n):
            if i%50 == 0:
                print i

            # vN box. TODO: vN box function
            while True:
                #print v0, self.readint()
                b0 = 1 if self.readint() > v0 else 0
                b1 = 1 if self.readint() > v0 else 0
                v0 = self.readint()
                if b0 == b1:
                    continue
                else:
                    break

            v0 = b0
            yield str(v0)
                    
            
            
class StatTests:
    def __init__(self, bitstring):
        self.s = bitstring
        self.fips = len(bitstring) == 20000
    def monobit(self):
        n = len(self.s)
        n0 = len([a for a in self.s if a == '0'])
        n1 = n-n0
        print n1
        if (9654 < n) and (n < 10346):
            print "Monobit: within the FIPS 140-1 bounds!"
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
 
