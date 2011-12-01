from stattests import StatTests, FipsTests

b = ''.join([a for a in "11100 01100 01000 10100 11101 11100 10010 01001" if a != ' ']*4)

st = StatTests(b)
if len(st) is not 160:
    print "bla"

#print st.poker(3)


t = '1110001100010001010011101111001001001001001'
print st.runs(3)
