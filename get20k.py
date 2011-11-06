from arduino import Arduino, StatTests

import sys

if len(sys.argv) == 1:
    print "missing alg"
    sys.exit()
    
algorithm = sys.argv[1]
ard = Arduino()
f = open('/home/benedikt/hr/loka/statusreport/' + algorithm + '20k.txt', 'w')

if algorithm == 'meanrand':
    s = ''.join(ard.meanrand(20000))
elif algorithm == 'updownrand':
    s = ''.join(ard.updownrand(20000))
f.write(s)

st = StatTests(s)
print s.monobit()

f.close()



