'''A program that runs all rand-algorithms three times, collects mean, prints
results prettily and runs some more'''

from arduino import Arduino, FipsTests
import time

ard = Arduino(debug=True, dbglevel=50)
#algs = [ard.vanilla, ard.leastsigrand, ard.meanrand, ard.updownrand, ard.mixmeanupdown, ard.twoleastsignrand]
#algs = [ard.leastsigrand, ard.vanilla, ard.updownrand, ard.mixmeanupdown, ard.twoleastsignrand]
algs = [ard.leastsigrand]

k = 20000

for alg in algs:
    print "[ ]", alg.__doc__.split('\n')[0]
    Xmeanl = []
    for i in range(3):
        print "  [+] Run", i, ":"
        # Generate the bitstring
        start = time.time()
        b = ''.join(alg(k))
        end = time.time()
        print "    [ ] Birtrate:", k/(end-start), "bits/second"
        print "    [ ] Time:", end-start, "seconds"
        fips = FipsTests(b)

        mono, X1, n1 = fips.monobit()
        poker, X3 = fips.poker()
        runs, X4, G, B = fips.runs()
        
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
        
    #print "  [+] Mean over the X statistics:", sum(Xmeanl, 0.0)/len(Xmeanl)
    
        
