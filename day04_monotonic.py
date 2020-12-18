# 20201217 : I see that 111122 is acceptable in part 2. I don't know why!
# My code accepts 353, which is too few. Quite possibly I am missing...
# Does it mean that in 1111 the regex search would find 11, then again 11,
# so pairs are good and 4 in a row is good, but triples ar not?
# Then 5 in a row is not OK? But 6 is fine?
# write hnzz version that counts that all sequences of 0's are odd.

def nms(l,m,n): # number of monotone sequences of length l, range(n,m).
    if l == 0:
        return 1
    return sum([nms(l-1,k,n) for k in range(m,n+1)])

def fs(l,m): # fixd-sum: sequences of l integers with sum at most m.
    if l == 0:
        return []
    if l == 1:
        return [[i] for i in range(m+1)]
    else:
        return [[i] + x for i in range(m+1) for x in fs(l-1,m-i)]

def hz(y): # has_zero
    for x in y[1:]:
        if x == 0:
            return 1
    return 0

def hnzz(y): # has_no_zero followd by a zero.
    for i in range(1,len(y)-1):
        if y[i:i+2] == [0,0]:
            if i+2 in range(len(y)):
                if y[i+2] != 0:
                    return 0
    return 1

def epitct(y): # Not every pair is in a triple.s
    mult = [1]
    for x in y[1:]:
        if x == 0:
            mult[-1] += 1
        if x != 0:
            mult += [1]
    return mult

def epit(y): # Not every pair is in a triple.s
    mult = [1]
    for x in y[1:]:
        if x == 0:
            mult[-1] += 1
        if x != 0:
            mult += [1]
    if mult.count(2) > 0:
        return 1
    return 0

def mono(y):
    y = [y[0]+2]+y[1:]
    z = [sum(y[:i]) for i in range(1,len(y)+1)]
    return z

def sti(y): # sequence to integer
    if y == []:
        return 0
    return 10*sti(y[:-1])+y[-1]

ste = fs(6,7)
stz = [x for x in ste if hz(x)]
st = [mono(x) for x in stz]
se = [sti(y) for y in st]
sf = [y for y in se if y >= 272091 and y <= 815432]
print("part 1", len(sf))
stz = [x for x in ste if hz(x) and epit(x)]
st = [mono(x) for x in stz]
se = [sti(y) for y in st]
sf = [y for y in se if y >= 272091 and y <= 815432]
print("part 2", len(sf))

