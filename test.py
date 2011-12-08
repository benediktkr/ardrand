from stattests import StatTests, FipsTests
from seedfind import Seedfinder
from avrlibcrandom import random, srandom

f = open('samples.txt').read().split('\n')

seed = int(f[40987])

srandom(seed) 
seq = [random() for _ in range(10)]
s = Seedfinder()
print s.findseed(seq), seed

