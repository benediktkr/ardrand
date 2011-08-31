#coding: utf8
from serial import Serial
from serial import SerialException
from time import sleep
import sys

# Inherit serial when im not sitting in a cramped coach
class Arduino(Serial):
    def poll(self, pin=3):
        self.write("POLL " + str(pin))
        return int(self.readline()[:-2])

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "usage: poll.py tty_port n"
        sys.exit()
    port = "/dev/ttyUSB0"
    pin = 4

    ard = Arduino(sys.argv[1], 9600)
    # while True:
    for i in xrange(0, int(sys.argv[2])):
        print ard.poll()
        sleep(0.5)

