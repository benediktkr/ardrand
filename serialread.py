# -*- coding: utf-8 -*-
import sys, time
from serial import Serial
from serial.serialutil import SerialException

# TODO: pull form ard, not get pushed

ard = Serial(sys.argv[1], 9600)
ard.open()

# Start the timer
t0 = time.time()

o = {} # 'o' for occurances

try:
    while True:
        val = int(ard.readline()[:-2])
        if val in o:
            o[val] += 1
            print "%d (%d)" % (val, o[val])
        else:
            o[val] = 1
            print val, "(new)"
        

except ValueError as v:
    print v
    print "type(v): ", type(v)
    print "v.args", v.args

except KeyboardInterrupt:
    print "KeyboardInterrupt!"


except SerialException as se:
    print se

except Exception as E:
    print E
# Stop timer
t = time.time() - t0

# Present the values in a sorted manner
s = [(a, o[a]) for a in sorted(o.keys(), key=o.__getitem__, reverse=True)]

print
print
print s
print
print
print "Ran for:\t%f secs" % t
print "Sample size:\t%d" % sum([a[1] for a in s])
print "N.o. values:\t%d" % len(s)
print "Uniques:\t%d" % len([a for a in s if a[1] == 1])

