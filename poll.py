#!/usr/bin/python
#coding: utf8

from serial import Serial
from serial import SerialException
from time import sleep
from datetime import datetime, time, date
import sys

class Arduino(Serial):
    def poll(self, t, pin=3):
        self.write("POLL " + str(pin))
        try:
            return t(self.readline()[:-2])
        except:
            return self.poll(self, t, pin)

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print "usage: poll.py tty_port wait_time"
        sys.exit()

    l = []
    ard = Arduino(sys.argv[1], 9600)
    try:
        while True:
            l.append(ard.poll(str))
            sleep(float(sys.argv[2]))

    except KeyboardInterrupt:
        filename = "data/" + str(date.today()) + "_" + str(datetime.time(datetime.now())) + "_" + sys.argv[2] + ".txt"
        print "Ok, writing to " + filename
        f = open(filename, 'w')
        f.write('\n'.join(l))
        f.close()
        print "wrote " + str(len(l)) + " lines"
