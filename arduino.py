#coding: utf-8

from serial import Serial, SerialException
from collections import defaultdict, deque 
from math import floor, ceil
from time import sleep, time
from sys import stdout
from itertools import groupby

class Arduino(Serial):
    """The Arduino class communicates with the arduino board and
    builds a string of random bits. Hold the state of the algs.
    All algs take in excatly one paramter - n."""


    def __init__(self, port="/dev/ttyUSB0", baudrate=9600, p=3, debug = False, dbglevel = 100):
        Serial.__init__(self, port, baudrate)
        self.pin = p
        self.debug = debug
        self.dbglevel = dbglevel

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
        """Mean-RAND
        The Mean-RAND algorithm. Generates a 0-bit if the value read is below the mean
        of the last b values. Two bits are generated and ran through a Neumann box"""
        bufsize = 100                   # b
        buf = deque([0]*bufsize)

        # Fill buffer with initial values
        print "Initializing..."
        start = time()
        for i in range(len(buf)):
            buf[i] = self.readint()

        meanval = float(sum(buf))/bufsize
        print "...done (", time()-start, ") seconds"
        
        for i in xrange(n):
            #if i%50==0:
            #    print i

            #yield self.vnbox(lambda: 1 if self.readint() > m else 0)
            """Generate two bits and run them through a von Neumann box.
            00/11 → discard, 10 → 1, 01 → 0"""
            i = 0
            while True:
                meanval -= float(buf.popleft())/bufsize
                buf.append(self.readint())
                meanval += float(buf[-1])/bufsize
                m = int(ceil(meanval))

                
                b0 = 1 if self.readint() > m else 0
                b1 = 1 if self.readint() > m else 0

                
                if b0 == b1:
                    i += 1
                    if i % self.dbglevel == 0 and self.debug:
                        print "Board may be stuck. I have read", i, "values and this is what i get now:", self.readint()
                        print "DEBUG: My mean now:", m
                        # We just ded a readint(), no waiting 
                        start = time()
                        self.readint()
                        end = time()
                        print "DEBUG (meanrand): Time between readings:", end-start, "seconds"

                    continue
                else:
                    i = 0
                    break
            # TODO: alter to what lestsig-RAND does ASAP. Code beauty.
            if b0 == 1:
                yield '1'
            else:
                yield '0'

    def updownrand(self, n):
        """Updown-RAND
        First read a value v_0. Then use it to determine if the bit
        b is 1 or 0. If we have v_1 > v_0 for the new value v_1 then
        we have b=1, otherwise b=0. In order to determine b we read
        two values (or more) and apply the vN box.

        I can think of several variations of this algorithm. Now, we
        first determine v_0 and then take two or more readings with
        the vN-box. We could read v_0 on the fly and not fix it, so
        the vN-box reads four values in each run and not two:
        
           vNbox (idea):
              b0 = 1 if readint() < readint() else 0
           vNbox (now):
              b0 = 1 if readint() < v_0 else 0

        20k 108m58.164s"""

        for i in xrange(n):
            #if i%50 == 0:
            #    print i

            v0 = self.readint()
            b =  self.vnbox(lambda: 1 if self.readint() > v0 else 0)
            yield b
                    
    def mixmeanupdown(self, n):
        """MixMeanUpdown-RAND
        Generates a bit by calculating Mean-RAND XOR Updown-RAND"""
        m = self.meanrand(n)
        u = self.updownrand(n)
        
        for i in xrange(n):
            # Wasnt vnboxed
            yield self.vnbox(lambda: m.next()^u.next())

    def leastsigrand(self, n):
        """Leastsig-RAND
        For every analogRead(), use the least significant bit, and
        vN-box Ask ymir what site he was talking about"""
        for i in xrange(n):
            #if i%50 == 0:
            #    print i                 # Sigh..
            yield self.vnbox(lambda: self.readint()&1)

    def twoleastsignrand(self, n):
        """Twoleastsign-RAND
        For every two analogRead(), look at the XOR of the two
        least significant bits (of the latest two readings)"""
        for i in xrange(n):
            yield self.vnbox(lambda: self.readint()&1^self.readint()&2>>1)

    def vnbox(self, phi):
        i = 0
        while True:
            #start = time()
            b0 = phi()   # Can i do this in one line?
            b1 = phi()
            #end = time()


            #string = "Bitrate:", (end-start)/2, "bits/second"
            #sys.stdout.write('\b'*len(string))
            #stdout.write(string)
            #stdout.flush()
            
            if b0 == b1:
                i += 1
                if i % self.dbglevel == 0 and self.debug:
                    print "Board may be stuck. I have read", i, "values and this is what i get now:", self.readint()
                    # We just ded a readint(), no waiting 
                    start = time()
                    self.readint()
                    end = time()
                    print "DEBUG: Time between readings:", end-start, "seconds"
                continue
            else:
                i = 0
                return str(b0)
            
    def vanilla(self, n):
        '''Vanilla
        Reeads from analogRead() a total of n bits (reads 10-bit integer at a time)
        Yields 10 bits at a time instead of 1 like the others'''

        for i in xrange(n/10):
            b = bin(self.readint())[2:]
            m = 10 - len(b)
            if m > 0:
                b = '0'*m + b
            yield b

        bitsLeft = 10 - (n/10)*10
        b = bin(self.readint())[2:]
        yield b[:bitsLeft]
        
class StatTests:
    def __init__(self, bitstring):
        self.s = bitstring
        self.n = len(self.s)
        self.fips = (self.n == 20000)

    def __len__(self):
        return len(self.s)

    def monobit(self):
        '''Returns 2-tuple (X1, n1)'''
        n0 = len([a for a in self.s if a == '0'])
        n1 = self.n-n0
        X1 = float((n0-n1)**2)/self.n

        return (X1, n1)

    def twobit(self):
        pass

    def poker(self, m=4):
        '''Divide the sequence s into k non-overlapping parts, each of length m
        Let N[i] count the number of occurances of the ith type of sequnce
        There are 2^m possible strings so we have that 0 < i <= 2^m'''
        k = int(floor(self.n/m))

        if not k >= 5*2**m:
            print "Lower your m! (Or write this code)"
            return False

        S = [self.s[a:a+m] for a in range(0, self.n, m)][:k]
        N = [0]*2**m

        # *twich*
        for i in S:
            N[int(i, 2)] += 1
        
        X3 = float(2**m)/k * sum(map(lambda x: x**2, N)) - k
            
        return X3
    
    def runs(self, k=0):
        ''' e_i is the number of caps of length i
            Let k be the largest i for which we have e_i >= 5
              [Methinks it should be calculated on the fly or something]
         
           For n=20000, we have 
              >>> e = lambda i, n: float(n-i+3)/2**(i+2); e(9, 20000)
               9.7626953125      (approx 10)

           Returns a 3-tuple of
              - statistic X4 which follows X^2 with df=2k-2
              - number of gaps
              - number of blocks'''
        
        k = 10 if k == 0 else k
        B = [0]*(k+1)
        G = B[:]

        #for i in range(1, k+1):

        # Maður lifandi, þetta er sniðugt!
        for groupname, group in groupby(self.s):
            i = len(''.join(group))
            if i > k:
                # NOTE: Not sure if the FIPS specifications expect this behaviour. 
                continue
            elif groupname == '1':
                B[i] += 1
            else:
                G[i] += 1

        e = lambda i: float(self.n-i+3)/2**(i+2) # Returns a float
        E = [e(i) for i in range(1, k)]

        X4 = sum([((B[i] - e(i))**2 + (G[i] - e(i))**2)/e(i) for i in range(1, k+1)])
        
        return (X4, G, B)
                
    def autocorrelation(self):
        pass

class FipsTests():
    """All tests return at least a 2-tuple, where the 0-index element is if the
    test was passed, the 1-index is the statistic and the rest is additional
    info."""
    def __init__(self, bitstring):
        self.n = len(bitstring)
        if not self.n == 20000:
            raise Exception
        self.s = bitstring
        # HACK: Create instance of class so we can use same names. 
        self.st = StatTests(self.s)     

    def monobit(self):
        X1, n1 = self.st.monobit()
        if (9654 < n1) and (n1 < 10346):
            return (True, X1, n1)
        return (False, X1, n1)

    def poker(self):
        X3 = self.st.poker(4)
        if (X3 > 1.03) and (X3 < 57.4):
            return (True, X3)
        return (False, X3)

    def runs(self):
        '''See table on p. 183 in Menezes. There are limits for all 1<=i<=6.
        For the purposes of this test, longer runs than 6 are considered to have
        a length of 6.

        NOTE: StatTests.runs() only counts runs of length up to k. Easily changed
              by commenting the line out'''
        X4, G, B = self.st.runs(10)
        B[6] = sum(B[7:])
        G[6] = sum(G[7:])

        limits = [ [],
                   [2267, 2733],
                   [1079, 1421],
                   [502, 748],
                   [223, 402],
                   [90, 223],
                   [90, 223]
            ]

        #all((l[0] < G[i] < l[1] for i,l in enumerate(limits))


        for i in range(1, 7):
            # Gaps and blocks separately so we can tell the diff
            # TODO if not lower < G or B < upper. 
            if (G[i] < limits[i][0]) or (G[i] > limits[i][1]):
                return (False, X4, G[1:7], B[1:7])
            if (B[i] < limits[i][0]) or (B[i] > limits[i][1]):
                return (False, X4, G[1:7], B[1:7])
            
        return (True, X4, G[1:7], B[1:7])
        
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
 

