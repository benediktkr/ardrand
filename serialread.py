# -*- coding: utf-8 -*-
import sys, time
from serial import Serial
from serial.serialutil import SerialException
from collections import defaultdict
from time import sleep

# TODO: pull form ard, not get pushed


def pull(stream, n):                    # Generator?
    stream.open()

    l = []               # 'l' for list of numbers
    #while True:
    for i in xrange(n):
        try:
            val = stream.readline()[:-2] # ends with \r\n
        except SerialException as se:
            print se
            sleep(5)
            continue
        except KeyboardInterrupt as k:
            break
        except Exception as E:
            print E
            break
        
        l.append(int(val))
        print val

    stream.close()
    return l

def getstats(l):
    o = defaultdict(int) # 'o' for occurances
    for x in l:
        o[val] += x

    mean = float(sum(l))/len(l)
    s = [(a, o[a]) for a in sorted(o.keys(), key=o.__getitem__, reverse=True)]

    return (mean, s)

if __name__ == '__main__':
    ard = Serial(sys.argv[1], 9600)

    # Start the timer
    t0 = time.time()

    ardnums = pull(ard, 10000)

    # Stop timer
    t = time.time() - t0

    m, s = getstats(ardnums)
    
    print "Ran for:\t%f secs" % t
    print "Sample size:\t%d" % len(l)
    print "N.o. values:\t%d" % len(s)
    print "Uniques:\t%d" % len([a for a in s if a[1] == 1])
    print "Mean:\t\t%f" % m

