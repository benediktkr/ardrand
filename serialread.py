# -*- coding: utf-8 -*-
import sys, time
from serial import Serial

# TODO: pull form ard, not get pushed

ard = Serial(sys.argv[1], 9600)
ard.open()

# Start the timer
t0 = time.time()

o = {} # 'o' for occurances

try:
    while True:
        val = int(ard.readline()[:-2])
        print val
        if val in o:
            o[val] += 1
        else:
            o[val] = 1
        

except ValueError:
    print "ValueError: ", val

except KeyboardInterrupt:
    print "KeyboardInterrupt!"

# Stop timer
t = time.time() - t0

# Present the values in a sorted manner
s = [(a, o[a]) for a in sorted(o.keys(), key=o.__getitem__, reverse=True)]

print "Ran for:\t%f secs" % t
print "Sample size:\t%d" % sum([a[1] for a in s])

    
