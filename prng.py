'''Class containing wrapper-esque methods for PRNGs to be tesed, with
the same interace as the Arudino-algorithms.'''

import avrlibcrandom
from os import urandom

class Prng:
    def urandom(self, n):
        '''/dev/urandom
        Produce n//8 bytes (~n bits) from urandom in binary. To
        conform with the rest of the algs (and keeping all.py pretty)
        it has to input the number of bits requested.'''

        k = n//8          # Its only going to be used for 2500bytes(20000) bits anyways
        # let b be 1 byte from /dev/urandom
        b = [format(ord(c), '08b') for c in urandom(k)]

        # Conform to expectations of all.py
        for bit in b:
            yield bit

    def avrrandom(self, n, seed=1):
        '''avr-libc PRNG
        According to http://arduino.cc/en/Reference/Long a long on
        arduino (and therefor avr) is 4 bytes. Produces n//(8*4) bytes (~n
        bits) from the avr-libc prng'''

        for i in range(n//(8*4)):
            # let b be 4 bytes from the prng
            b = format(avrlibcrandom.random(), '032b')
            yield ''.join(b)

    def avrseed(self, x):
        avrlibcrandom.srand(x)
            
        
    
