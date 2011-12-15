#coding: utf-8

'''The Arduino class, inherits Serial class and contains RAND algs.

For the kid playing space station on the schoolyard.'''

from serial import Serial, SerialException
from collections import deque 
from time import sleep, time
from sys import stdout
from math import ceil

class Arduino(Serial):
    """The Arduino class communicates with the arduino board and
    builds a string of random bits. Hold the state of the algs.
    All algs take in excatly one paramter - n."""


    def __init__(self, port="/dev/ttyUSB0", baudrate=115200, p=3, debug = False, dbglevel = 100):
        Serial.__init__(self, port, baudrate)
        self.pin = p
        self.debug = debug
        self.dbglevel = dbglevel

    def readint(self):
        """Catch OSError because the Arudino tends to be become
        'unavailible' and check if we read a digit because we
        sometimes get malformed strings.  Somtimes it raises a
        SerialException with the message 'device reports readiness to
        read but returned no data'

        TODO: What does 'unavailible mean?  Why do we get malformed
        strings?"""
        self.write("POLL " + str(self.pin))
        while True:
            try:
                i = self.readline()[:-2]
                if i.isdigit():
                    return int(i)
            except OSError as e:
                if self.debug:
                    print "OSError:", e, "arduino.py: sleeping for 10 sec"
                sleep(10)
            except SerialException as e:
                '''From the pyserial code, "Disconnected devices, at
                least on Linux, show the behavior that they are always
                ready to read immediately but reading returns nothing."

                http://www.java2s.com/Open-Source/Python/Development/pySerial/pyserial-2.5-rc2/serial/serialposix.py.htm

                Also, handling SerialException here? Handling
                exceptions here at all?'''
                if self.debug:
                    print "SerialException:", e, "arduino.py: sleeping for 1 sec"
                    sleep(1)
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

        if self.debug:
            print "Initializing..."
            start = time()
            
        for i in range(len(buf)):
            buf[i] = self.readint()

        if self.debug:
            print "...done (", time()-start, ") seconds"

        meanval = float(sum(buf))/bufsize

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
            # b = bin(self.readint())[2:]
            # m = 10 - len(b)
            # if m > 0:
            #     b = '0'*m + b
            b = format(self.readint(), '010b')
            yield b

        bitsLeft = 10 - (n/10)*10
        b = bin(self.readint())[2:]
        yield b[:bitsLeft]

    def onboardtlsr(self, n):
        '''Onboard Twoleastsign-RAND
        '''
        for i in xrange(n):
            self.write("TLSR " + str(self.pin))
            yield self.read(1)
        
        
        
class ArdFile(file):
    '''Interface to be able to call .readint() on a file object'''
    def __init__(self, fname, mode='r'):
        file.__init__(self, fname, mode)
        self.samples = self.read().split('\n')
        self.i = 0
        self.n = len(self.samples)

    def __len__(self):
        return self.n

    def readint(self):
        current = self.samples[self.i]
        self.i += 1
        return int(current)
