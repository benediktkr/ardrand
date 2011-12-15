# Test the seedfinder
# Should probably be threaded and whatnot, but i dont have time right now. Dammit. 
import random # :3
from seedfind import Seedfinder
from avrlibcrandom import random as avrrand
from avrlibcrandom import srandom as avrsrand
from time import time
from sys import argv, exit

if len(argv) < 2:
    print "python", argv[0], "k"
    exit(1)

random.seed() # uses system time
sf = Seedfinder() # use default sample source
samples = open("samples.txt", "r").read().split('\n')

sendValues = 100

# Iterations
k = int(argv[1])
# How many values can we skip at the most before we send in the sequence? Max depth
l = 1000
# How well do we want to estimate C?
est = 0.8

meant = []

giveups = 0

for i in range(k):
    start = time()
    
    # Pick random seed
    seed = int(samples[random.randint(0, len(samples))])
    avrsrand(seed)

    # skip randomly many values up to l
    depth = random.randint(1, l)
    
    # genrate sequence
    seq = [avrrand() for _ in range(depth+sendValues+1)]

    # Here C = depth. 
    m = int(est*depth)

    foundSeed = sf.findseed(seq, m)
    t = time() - start

    if foundSeed == -1:
        # We gave up
        giveups += 1
        print "Gave up",
    else:
        print "Success",

    meant.append(t)
    print "Seq len: %d, Depth: %d, Time: %f, Count: %d, Giveups: %d" % (len(seq), depth, t, i, giveups)


print "Mean time:", sum(meant, 0.0)/k
print "Giveups:", giveups

