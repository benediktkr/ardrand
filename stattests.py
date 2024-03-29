#coding: utf-8
from collections import defaultdict
from math import floor
from itertools import groupby

class StatTests:
    def __init__(self, bitstring):
        self.s = bitstring
        self.n = len(self.s)
        self.fips = (self.n == 20000)

    def __len__(self):
        return len(self.s)

    def monobit(self):
        '''Returns 2-tuple (X1, n1)'''
        n0 = len([a for a in self.s if a == '0'])
        n1 = self.n-n0
        X1 = float((n0-n1)**2)/self.n

        return (X1, n1)

    def twobit(self):
        pass

    def poker(self, m=4):
        '''Divide the sequence s into k non-overlapping parts, each of length m
        Let N[i] count the number of occurances of the ith type of sequnce
        There are 2^m possible strings so we have that 0 < i <= 2^m'''
        k = int(self.n//m)              # Floored division

        if not k >= 5*2**m:
            print "Lower your m! (Or write this code)"
            return False

        S = [self.s[a:a+m] for a in range(0, self.n, m)][:k]
        N = [0]*2**m

        # *twich*
        for i in S:
            N[int(i, 2)] += 1
        
        X3 = float(2**m)/k * sum(map(lambda x: x**2, N)) - k
            
        return X3
    
    def runs(self, k=9):
        ''' e_i is the number of caps of length i
            Let k be the largest i for which we have e_i >= 5
              [Methinks it should be calculated on the fly or something]
         
           For n=20000, we have 
              >>> e = lambda i, n: float(n-i+3)/2**(i+2); e(9, 20000)
               9.7626953125      
             >>> e(10, 20000)
               4.881103515625

           It then follows that that the largest i for which we have
           e(9) => 5. At i=10, e(10) = 4.8 < 5, it goes below 5 there.

           Returns a 3-tuple of
              - statistic X4 which follows X^2 with df=2k-2
              - number of gaps
              - number of blocks'''
        
        # Count 1..k runs
        B = [0]*(k+1)
        G = B[:]

        # Count all groups
        # Let c be the length of the longest group
        #c = max([len(''.join(a[1])) for a in groupby(self.s)])
        #B = [0]*(c+1)
        #G = B[:]
        # If so happens that c > k, we get IndexErrors below when we calculate X4
        #k = c if c > k else k
        
        # Maður lifandi, þetta er sniðugt!
        # for groupname, group in groupby(self.s):
        #     i = len(''.join(group))
        #     if i >= k:
        #         continue
        #     #elif groupname == '1':
        #     if groupname == '1':
        #         B[i] += 1
        #     else:
        #         G[i] += 1

        runs = [(groupname, len(''.join(group))) for groupname, group in groupby(self.s)]
        for i in range(1, k):
            # Hm. 
            B[i] = len([a for a in runs if a[1] == i and a[0] == '1'])
            G[i] = len([a for a in runs if a[1] == i and a[0] == '0'])
        

        e = lambda i: float(self.n-i+3)/2**(i+2) # Returns a float


        X4 = sum([((B[i] - e(i))**2 + (G[i] - e(i))**2)/e(i) for i in range(1, k+1)])
        
        return (X4, G, B)
                
    def autocorrelation(self):
        pass

class FipsTests():
    """All tests return at least a 2-tuple, where the 0-index element is if the
    test was passed, the 1-index is the statistic and the rest is additional
    info."""
    def __init__(self, bitstring):
        self.n = len(bitstring)
        if not self.n == 20000:
            # Uhm. Not really sure how to do a proper excetion
            # raising, this'll have to do
            print "n != 20000"
            raise Exception
        self.s = bitstring
        # HACK: Create instance of class so we can use same names. 
        self.st = StatTests(self.s)     

    def monobit(self):
        X1, n1 = self.st.monobit()
        # 9.654 < X1 < 10.346
        if (9654 < n1) and (n1 < 10346):
            return (True, X1, n1)
        return (False, X1, n1)

    def poker(self):
        X3 = self.st.poker(4)
        if (X3 > 1.03) and (X3 < 57.4):
            return (True, X3)
        return (False, X3)

    def runs(self):
        '''See table on p. 183 in Menezes. There are limits for all 1<=i<=6.
        For the purposes of this test, longer runs than 6 are considered to have
        a length of 6.

        NOTE: StatTests.runs() only counts runs of length up to k. Easily changed
              by commenting the line out'''
        X4, G, B = self.st.runs(10)

        B[6] += sum(B[7:])
        G[6] += sum(G[7:])

        limits = [ [],
                   [2267, 2733],
                   [1079, 1421],
                   [502, 748],
                   [223, 402],
                   [90, 223],
                   [90, 223]
            ]

        #all((l[0] < G[i] < l[1] for i,l in enumerate(limits))

        for i in range(1, 7):
            # Gaps and blocks separately so we can tell the diff
            if not limits[i][0] < G[i] < limits[i][1]:
                return (False, X4, G[1:7], B[1:7])
            if not limits[i][0] < B[i] < limits[i][1]:
                return (False, X4, G[1:7], B[1:7])
            
        return (True, X4, G[1:7], B[1:7])

    def longruns(self):
        '''The long runs test is passed if there are no runs of length
        34 or more. Return a 1-tuple to keep style'''

        X4, G, B = self.st.runs(10)
        # We use 0 based indexing, so a run of length 34 implies that
        # G or B has length 34+1 or greater
        if len(G) >= 34+1 or len(B) >= 34+1:
            return (False)
        else:
            return (True)
        
class RawData:
    def __init__(self, l):
        self.data = l
        self.count = len(self.data)
        self.mean = float(sum(self.data))/self.count
            
    def freq(self):
        freqs = defaultdict(int)
        for x in self.data:
            freqs[x] += 1

        # The uniformity factor is how many of the numbers are AT the mean or below
        m = int(floor(self.mean))
        factor = float(sum([freqs[a] for a in freqs if a <= m]))/self.count
        return (freqs, factor)
    
    def correlation(self):
        corr = []
        for i in range(1, len(self.data)):
            # Absolute value?
            corr.append(self.data[i] - self.data[i-1]) 
        return corr
 

