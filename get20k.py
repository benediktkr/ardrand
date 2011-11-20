from arduino import Arduino, StatTests

import sys

if len(sys.argv) == 1:
    print "missing alg"
    sys.exit()
    
algorithm = sys.argv[1]
k = int(sys.argv[2])
ard = Arduino()


# ...
if algorithm == 'meanrand':
    s = ''.join(ard.meanrand(k))
elif algorithm == 'updownrand':
    s = ''.join(ard.updownrand(k))
elif algorithm == 'mix':
    s = ''.join(ard.mixmeanupdown(k))
elif algorithm == 'leastsig':
    s = ''.join(ard.leastsigrand(k))


st = StatTests(s)
print st.monobit()
save = (sys.argv[3] if len(sys.argv) >= 4 else "") or raw_input("Save to: ")
if "-p" in sys.argv:
    print s
elif save:
    f = open(save, 'w')
    f.write(s)
    f.close()

