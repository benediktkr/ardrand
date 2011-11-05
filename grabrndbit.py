#coding: utf-8
"""Just a short program that grabs a bitstring s and writes to a file"""

from arduino import Arduino
from sys import stdin, argv

ard = Arduino()
# FIPS 140-1 demands a bitstring s of length 20 000. 
l = 20000
fname = argv[1] if len(argv) > 1 else 's.txt'
f = open(fname, 'w')
s = ''.join([a for a in ard.meanrand(l)])
f.write(s)
f.close()


