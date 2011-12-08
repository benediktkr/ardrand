#coding: utf-8
'''Let C be the number of calls that a program has made to the
avr-libc random() function (the Arduino is equipped with it). This
program finds the seed value with reasonable guessing-time (runs in
O(C)).

Since the analogRead() function is heavily biased, we use a sampling
to create a probability distribution that we select from. The idea is
to supply a standard sample space as well as enable the option of
supply a stream of values, either live or from a file. 
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

        self.p = self._makefreq(samplesource)


    def findseed(self, sequence):
        '''Let k be the number of calls a program has made to the
        avr-libc random() function.  Ignoring the break-statement,
        the worst case scenario is that we make 1024*k calls to the
        function oursevles.

        This function then runs in O(k) time, where k is the length
        of the given sequence.''

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

        # This should never happen, but i sleep so much better knowing
        # all my functions always have a defined return value :3
        return None 
                

    def _makefreq(self, source, n=20000):
        '''Builds the probability distribution from n samples from
        source. If source is a FileSamples object, n is finite and we
        force it to be the number of lines in the file'''
        if type(source) == type(ArdFile):
            n = len(source) if len(source) > n else n  # Not possible on file objects
            
        freqs = defaultdict(int)
        for x in xrange(n):
            freqs[source.readint()] += 1

        # Let f be a list of keys (values read from arduino) sorted
        # by their items (the frequency of a given key), in asc order (we
        # want to pop the value with the highest avail freq form this list)
        f = sorted(freqs.keys(), key=freqs.__getitem__, reverse=False)

        # Let d be the set difference between the set {0..1023} and f
        d = set(range(1023)) - set(f)

        # And return a sorted list that first contains the values in probability
        # order (poppable) and then the rest of the values, the set d as a list
        return list(d) + f
        

 
