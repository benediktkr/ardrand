#coding: utf-8
'''Let k be the number of calls that a program has made to the
avr-libc random() function (the Arduino is equipped with it). This
program finds the seed value with reasonable guessing-time (runs in
O(k)).

Since the analogRead() function is heavily biased, we use a sampling
to create a probability distribution that we select from. The idea is
to supply a standard sample space as well as enable the option of
supply a stream of values, either live or from a file. 

This code is heavily commented to make writing the section about it
easier. Oh, and if i ever have to read this mess again sometime.
'''

from collections import defaultdict, deque
from arduino import ArdFile, Arduino
from avrlibcrandom import random, srandom

class Seedfinder:
    def __init__(self, samplesource=None):
        '''FILL ME OUT'''
        # If samplesource is None, assume the default
        if samplesource == None:
            samplesource = ArdFile()

        self.p, self.g = self._makefreq(samplesource)


    def fromcomplete(self, sequence):
        '''This program finds the seed given a complete sequence from
        the seed. Let k be the number of calls a program has made to
        the avr-libc random() function (length of the sequence).

        Ignoring the break-statement, the worst case scenario is that
        we make 1024*k calls to the function oursevles.

        This function then runs in O(k) time, where k is the length
        of the given sequence.'''

        # Let's use lits
        #lastk = [deque()]*1024
        lastk = [[]]*1024
        k = len(sequence)

        while len(self.p) > 0:
            i = self.p.pop()
            srandom(i)
            for x in xrange(k):
                r = random()
                if r == sequence[x]:
                    lastk[i].append(r)
                else:
                    # We got the wrong value, pointless to go on
                    break

            #if list(lastk[i]) == sequence:
            if lastk[i] == sequence:
                # We have found the sequence, i is the seed
                return i

        # Happens if the seed is larger than 2**10-1 or we have a bad sequence. 
        return None

    def findseed(self, sequence, m=1):
        '''Finds the seed given a sequcence that does not have to be
        complete from the seed.
        
        m is how many extra iterations we want to spend on each
        que/possible seed beyond the length k. Thus m is an estimation
        of Cq'''

        k = len(sequence)
        lastk = [deque([]) for i in self.p]

        # Expand all the deques by k elements from p[i] for each i. 
        # 1024*k operations → O(k)
        for i in self.p:
            srandom(i)
            #lastk[i] = deque([random() for _ in range(k)])
            for _ in xrange(k):
                lastk[i].append(random())

            # If we recieved a sequence dervied directly from the seed
            if list(lastk[i]) == sequence:
                return i
            
        while True:
            # UPDATE THIS COMMENT
            # This has to be a little more sophisticated than a crude
            # bruteforce attack.
            # 
            # First try the first g values m*k times and as we move
            # down the prob dist go on to the rest of the values.
            #
            # This program has the rather curious property that it has
            # an essentially unknown running boundary. It is
            # completely dependent upon the number of calls made to
            # the PRNG before the sequence given to us appeared (until
            # we find the sequence, we stay inside the while loop. Let
            # C denote this value.
            #
            # After i edited the for loops, fix this comment section
            # So the worst case is (C/m)*k*m*k = C*k². That gives us a
            # running boundary of O(C*k^2) where C is
            # unknown. Techincally, it is a constant but the running
            # time of the program is highly dependent on it.
            #
            
            for i in self.p: # Adds O(1024) complexity, constant - no change. 
                # And we do this m*k times - we "flush" through the que.
                # We could just do this one time and move down the prob dist
                # but if we have a good enough sample, this will save us time
                # in practice.
                for _ in range(k+m):
                    srandom(lastk[i][-1])
                    
                    v = random()
                    lastk[i].popleft()
                    lastk[i].append(v)
                    if list(lastk[i]) == sequence:
                        return i
            # If we haven't found anything yet, we stay in the while loop. This program
            # may never halt, if we are given a bad sequence (that originated from some
            # other PRNG or perhaps not from a PRNG at all).


    def _makefreq(self, source, n=20000):
        '''Builds the probability distribution from n samples from
        source. If source is a FileSamples object, n is finite and we
        force it to be the number of lines in the file.

        Returns a 2-tuple, the full probabilty distribution and an integer
        g that represents how many different numbers were observed in the sample'''

        if type(source) == type(ArdFile):
            n = max(len(source), n)  # Not possible on file objects
            
        freqs = defaultdict(int)
        for x in xrange(n):
            freqs[source.readint()] += 1

        # {Value: count}
        f = sorted(freqs.keys(), key=freqs.__getitem__, reverse=False)

        d = set(range(1024)) - set(f) # Fill in unobserved values

        g = len(set(f))               # N.o. observerd values
        
        return (list(d) + f, g)
        
