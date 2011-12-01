'''Read the FIPS-140-1 20 000 bits from /dev/urandom on linux and runs
the FipsTests class on it. Resides in separate file because we dont
actually need to have an Arduino plugged in for this one'''

from stattests import StatTests, FipsTests
from os import urandom 

# 20 000 bits are 25 000 bytes

def urandomtest(n):
    '''/dev/urandom
    Produce n bits from urandom in binary. To conform with the rest of
    the algs (and keeping all.py pretty) it has to input the number of
    bits requested.'''

    k = n/8          # Its only going to be used for 2500bytes(20000) bits anyways
    b = [format(ord(c), '08b') for c in urandom(k)]

    # Conform to expectations of all.py
    for bit in b:
        yield bit

    #return ''.join(b)
    

if __name__ == "__main__":
    fips = FipsTests(''.join(urandomtest(20000)))
    print fips.monobit()
    print fips.poker()
    print fips.runs()
