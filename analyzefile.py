from arduino import Arduino
from stattests import StatTests
import sys

if len(sys.argv) != 2:
    print "usage: python analyze.py <file>"
    sys.exit()

st = StatTests(open(sys.argv[1]).read())
st.monobit()
