#coding: utf-8
'''Let C be the number of calls that a program has made to the
avr-libc random() function (the Arduino is equipped with it). This
program finds the seed value with reasonable guessing-time (runs in
O(C)).

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
            samplesource = ArdFile(fname='samples.txt')

        self.p, self.g = self._makefreq(samplesource)


    def fromcomplete(self, sequence):
        '''Find the seed when given the whole sequence.'''

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

            if lastk[i] == sequence:
                return i

        # Happens if the seed is larger than 2**10-1 or we have a bad sequence. 
        return None

    def findseed(self, sequence, m=1):
        '''Finds the seed given a sequcence that does not have to be
        complete from the seed.

        Let S_0 be the initial sequence of length k with s as seed,
        and S_n be the sequence with radom variables
        s_{n-k},..,s_k. Let S_1 be the observerd sequnce, also of
        length k.

        In each iteration, this program will generate all sequences
        S_i of s_{last},...,s{last+k+m}.

        Thus m is in a wayan estimation of C. One of those
        performance-tuning thingies.

        The program makes infinitely many iterations until it finds it
        unless the debug value is set. '''


        # Giveup option for testing purposes
        giveup = 50
        
        k = len(sequence)
        lastk = [deque([]) for i in self.p]

        # Expand all the deques by k elements from p[i] for each i.
        # => generate initial sequences. 
        # 1024*k operations → O(k)
        for i in self.p:
            srandom(i)
            #lastk[i] = deque([random() for _ in range(k)])
            for _ in xrange(k):
                lastk[i].append(random())

            # If we recieved a sequence dervied directly from the seed
            if list(lastk[i]) == sequence:
                return i
            
        #while True:
        for _ in xrange(giveup):
            # This has to be a little more sophisticated than a crude
            # bruteforce attack.
            #
            # This program has the rather curious property that it has
            # an essentially unknown running boundary. It is
            # completely dependent upon the number of calls made to
            # the PRNG before the sequence given to us appeared (until
            # we find the sequence, we stay inside the while loop. Let
            # C denote this value. Let m be our best estimation of C.
            #
            # For every value i, we have started with the intial sequnce
            # of length k. In each iteration we will check east of the
            # m+k sequential ques for a match. 
            
            for i in self.p: 
                for _ in range(m+k):
                    srandom(lastk[i][-1])
                    
                    v = random()
                    lastk[i].popleft()
                    lastk[i].append(v)
                    if list(lastk[i]) == sequence:
                        return i

            # If we haven't found anything yet, we stay in the while loop. This program
            # may never halt, if we are given a bad sequence (that originated from some
            # other PRNG or perhaps not from a PRNG at all).

        # Giving up
        return -1

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
        
