#!/usr/bin/python
#coding: utf8

from time import sleep
from datetime import datetime, time, date
import sys
from arduino import Arduino

# Pull indefintely until KeyboardException

def infrange(n=0, inf=False):
    '''Generator to generate a sequence up to n or inf'''
    if inf:
        while True:
            yield True
    else:
        i=0
        while i < n:
            yield i
            i+=1
        
if __name__ == "__main__":

    #Edit to both collect and poll

    if len(sys.argv) < 3:
        print "usage: poll.py tty_port wait_time [n]"
        sys.exit()

    # Assume an infinite collector as default
    n = 0
    pollEndlessly = True
    
    if len(sys.argv) == 4:
        n = int(sys.argv[3])
        pollEndlessly = False

    prefix = "/home/benedikt/hr/loka"

    # Store values in memory, we write to disk once. 
    l = []
    ard = Arduino(sys.argv[1], 9600)
    t = float(sys.argv[2])
    fname = "%s/data/%s_%s_%s.txt" % (prefix, date.today(), datetime.time(datetime.now()), sys.argv[2])
    
    for x in infrange(n, inf=pollEndlessly):
        try:
            # By first applying the int-function to the numbers we
            # throw exceptions when the arduino sends a malformed
            # string. This happens in about 0.2% of the time. I
            # should perhaps look into this?
            if "-v" in sys.argv:
                r = int(ard.poll())
                l.append(r)
                print r
            else:
                l.append(int(ard.poll()))
            
            sleep(t)
        except KeyboardInterrupt:
            break
        except Exception as E:
            sys.stdout.write(str(E) + "\n")

    # Write to timestamped file
    print fname
    f = open(fname, 'w')
    f.write('\n'.join(map(str, l)) + '\n') # back to str
    f.close()
    print "done. I wrote %d lines" % len(l)
