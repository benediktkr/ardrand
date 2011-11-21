from arduino import StatTests
st = StatTests(''.join([a for a in "11100 01100 01000 10100 11101 11100 10010 01001" if a != ' ']*4))
if len(st) is not 160:
    print "bla"
print st.poker(3)
