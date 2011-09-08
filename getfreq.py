import sys
from math import ceil, floor
from arduino import Data

# MTS: classes

def cleanlist(l):
    c = []
    fails = 0
    for x in l:
        try:
            c.append(int(x[:-1]))
        except:
            fails += 1
    return (c, fails)



if __name__ == "__main__":
    if "--clean" in sys.argv:
        input, fails = cleanlist(sys.stdin.readlines())
        print "Unparseable: %f" % (float(fails)/(len(input)+fails))
    else:
        input = [int(a[:-1]) for a in sys.stdin.readlines() if a[:-1]]

    d = Data(input)

    freqs, uniformity = d.freq()

    # Write the frequencies to a file in csv form
    f = open('temp.txt', 'w')
    for k in sorted(freqs):
        f.write("%d, %d\n" % (k, freqs[k]))
    print "Wrote frequncies to temp.txt"
    f.close()
    
    print "Mean: %f" % d.mean
    print "Uniformity %f" % uniformity
    print "Sample size: %d" % d.count



