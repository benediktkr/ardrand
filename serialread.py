# -*- coding: utf-8 -*-
import sys, time
from serial import Serial
from serial.serialutil import SerialException
from collections import defaultdict

# TODO: pull form ard, not get pushed


def pull(stream, n):
    stream.open()
    o = defaultdict(int) # 'o' for occurances
    l = []               # 'l' for list of numbers
    #while True:
    for i in xrange(n):
        try:
            val = stream.readline()[:-2] # ends with \r\n
        except SerialException as se:
            print se
            continue
        except KeyboardInterrupt as k:
            break
        except Exception as E:
            print E
            break
        
        l.append(int(val))
        o[val] += 1
        print val

    stream.close()
    return l, o

if __name__ == '__main__':
    ard = Serial(sys.argv[1], 9600)

    # Start the timer
    t0 = time.time()

    ardnums = pull(ard, 10000)

    # Stop timer
    t = time.time() - t0

    # Present the values in a sorted manner
    s = [(a, ardnums[1][a]) for a in sorted(ardnums[1].keys(), key=ardnums[1].__getitem__, reverse=True)]

    print
    print
    print s
    print
    print
    print "Ran for:\t%f secs" % t
    print "Sample size:\t%d" % sum([a[1] for a in s])
    print "N.o. values:\t%d" % len(s)
    print "Uniques:\t%d" % len([a for a in s if a[1] == 1])
    #print "Mean:\t\t%f" % sum(ardnums[0])/len(ardnums[0])

