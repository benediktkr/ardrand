# -*- coding: utf-8 -*-
import sys, time
from serial import Serial
from serial.serialutil import SerialException
from collections import defaultdict
from time import sleep

# TODO: pull form ard, not get pushed


def pull(stream, n, returnlist):               # Generator?
    stream.open()

    l = []                              # 'l' for list of numbers
    #while True:
    for i in xrange(n):
        sys.stderr.write("\b")
        try:
            val = stream.readline()[:-2] # ends with \r\n
            if returnlist: l.append(int(val))  # keep in memory to get stats.
            sys.stderr.write("\b")
        except ValueError as ve:
            sys.stderr.write("%d: Value error at reading \'%s\' (%s)\n" % (i, val, ve))
            sleep(1)
            continue
        except SerialException as se:
            sys.stderr.write("Serial: %s. Value: %s\n" % (se, val))
            sleep(5)
            continue
        except KeyboardInterrupt as k:
            sys.stderr.write("KeyboardInterrupt\n")
            break
        except Exception as E:
            sys.stderr.write(str(E) + "\n")
            sleep(5)
            continue


        # Be a little verbose
        sys.stderr.write("\n%c" % ['/', '-', '\\', '|'][i%4])
        #if i%300 == 0: sys.stderr.write("#")
        sys.stderr.flush()              # bad placement

        print val

    stream.close()
    return l

def getstats(l):
    o = defaultdict(int) # 'o' for occurances
    for x in l:
        o[x] += 1

    mean = float(sum(l))/len(l)
    s = [(a, o[a]) for a in sorted(o.keys(), key=o.__getitem__, reverse=True)]

    return (mean, s)

if __name__ == '__main__':
    if "-f" in sys.argv:
        ard = file(sys.argv[1])
    else:
        ard = Serial(sys.argv[1], 9600)

    # Start the timer
    t0 = time.time()

    ardnums = pull(ard, 10000, bool("-s" in sys.argv))

    # Stop timer
    t = time.time() - t0


    if "-s" in sys.argv:             # -s for stats
        m, s = getstats(map(int, ardnums))
        print "Ran for:\t%f secs" % t
        print "Sample size:\t%d" % len(ardnums)
        print "N.o. values:\t%d" % len(s)
        print "Uniques:\t%d" % len([a for a in s if a[1] == 1])
        print "Mean:\t\t%f" % m

