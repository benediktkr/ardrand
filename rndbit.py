#coding: utf-8
"""A short program that runs the Menezes described tests on a bitstring s. Can either be read from
stdin or directly generated. It currently has no input sanitation or anything. """

from arduino import Arduino
from sys import stdin, argv


# FIPS 140-1 demands a bitstring s of length 20 000. 
l = int(argv[1]) if len(argv) > 1 else 20000
s = stdin.readlines()


