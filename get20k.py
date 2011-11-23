from arduino import Arduino, StatTests, FipsTests

import sys

if len(sys.argv) == 1:
    print "missing alg"
    sys.exit()
    
algorithm = sys.argv[1]
k = int(sys.argv[2])
ard = Arduino()

print algorithm

# ...
if algorithm == 'meanrand':
    s = ''.join(ard.meanrand(k))
elif algorithm == 'updownrand':
    s = ''.join(ard.updownrand(k))
elif algorithm == 'mix':
    s = ''.join(ard.mixmeanupdown(k))
elif algorithm == 'leastsig':
    s = ''.join(ard.leastsigrand(k))
elif algorithm == 'twol':
    s = ''.join(ard.twoleastsignrand(k))

if "-p" in sys.argv:
    print s


st = StatTests(s)
print st.monobit()
print st.poker()
fips = FipsTests(s)
print fips.monobit()
print fips.poker()
save = (sys.argv[3] if len(sys.argv) >= 4 else "") or raw_input("Save to: ")
if save:
    f = open(save, 'w')
    f.write(s)
    f.close()

