'''The Wiring-functions random() and randomSeed() can be found in
    arduino-0022/hardware/arduino/cores/arduino/WMath.cpp
but they turn out to be wrapper functions around the avr-libc functions
random() and srandom() from
        libc/stdlib/random.c.
        
This program is implemented after that file in avr-libc-1.7.1.

Written in a classless C-manner to be as like the original possible.'''

# python doesn't have constants, right?
RANDOM_MAX = 0x7FFFFFFF

# Since lists in python are mutable, it can service as a interger pointer thingy
next = [1L]

def do_random(ctx):
    '''(Comment lifted from random.c)
    Compute x = (7^5 * x) mod (2^31 -1)
    without overflowing 31 bits:
         (2^31 - 1) = 12773 * (7^5) + 2836
    From "Random number generators: good ones are hard to find",
    Park and Miller, Communications of the ACM, vol. 31, no 10.
    October 1988, p. 1195. 
    '''

    x = ctx[0]
    # Can't be initialized with 0, so use another value
    if (x == 0):
        x = 123459876L
    hi = x / 127773L
    lo = x % 127773L
    x = 16807 * lo - 2836 * hi
    if (x < 0):
        x += 0x7fffffffL
    ctx[0] = x
    return x % (RANDOM_MAX + 1)

def random():
    return do_random(next)

def srandom(seed):
    next[0] = seed


if __name__ == '__main__':
    srandom(1908)
    for i in range(10):
        print random()
