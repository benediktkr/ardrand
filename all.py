'''A program that runs all rand-algorithms three times, collects mean, prints
results prettily and runs some more'''

from arduino import Arduino
from stattests import FipsTests
from time import time
from prng import Prng
from sys import argv, exit

if len(argv) < 2:
    print "python all.py port"
    exit(1)

port = argv[1]

ard = Arduino(port="/dev/ttyUSB" + port, debug=False, dbglevel=1500)
prng = Prng()

allalgs = [prng.urandom, ard.vanilla, ard.leastsigrand, ard.meanrand, ard.updownrand, ard.mixmeanupdown, ard.twoleastsignrand]
#algs = [urandomtest, ard.vanilla, ard.leastsigrand]

#algs = [ard.updownrand, ard.mixmeanupdown, ard.twoleastsignrand]
#algs = [ard.twoleastsignrand, ard.updownrand]

algs = [ard.leastsigrand, ard.twoleastsignrand]

#algs = [prng.urandom, ard.vanilla, ard.leastsigrand, ard.twoleastsignrand, ard.meanrand]


k = 20000

for alg in algs:
    print "[ ]", alg.__doc__.split('\n')[0]
    means = [[]]*3
    for i in range(3):
        print "  [+] Run", i, ":"
        # Generate the bitstring
        start = time()
        b = ''.join(alg(k))
        end = time()
        print "    [ ] Bitrate:", k/(end-start), "bits/second"
        print "    [ ] Time:", end-start, "seconds"
        fips = FipsTests(b)

        mono, X1, n1 = fips.monobit()
        poker, X3 = fips.poker()
        runs, X4, G, B = fips.runs()
        longruns = fips.longruns()

        means[i] = [X1, X3, X4, k/(end-start)]
        
        #Xmeanl.append((X1, X3, X4))
        print "    [ ] Monobit test"
        print "        [+] Passed" if mono else "        [!] Failed"
        print "        [ ] X1 =", X1, "n1 =", n1
        
        print "    [ ] Poker test"
        print "        [+] Passed" if poker else "        [!] Failed"
        print "        [ ] X3 =", X3

        print "    [ ] Runs test"
        print "        [+] Passed" if runs else "        [!] Failed"
        print "        [ ] X4 =", X4, "G =", G, "B =", B

        print "    [ ] Long runs test"
        print "        [+] Passed" if longruns else "        [!] Failed"




    
        
