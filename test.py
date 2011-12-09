#coding: utf-8

from stattests import StatTests, FipsTests
from seedfind import Seedfinder
from avrlibcrandom import random, srandom

f = open('samples.txt').read().split('\n')

seed = int(f[0])

seed = 526

srandom(seed) 
seq = [random() for _ in range(1000)][990:]

print "Ég sendi inn þessa runu", seq

s = Seedfinder()
print "Ég fann", s.findseed(seq, 0), "en þú gafst mér", seed

