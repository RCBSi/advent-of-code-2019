
def rp(x,n): #read n parameters as digits from n.
    if n==0:
        return []
    else:
        return [x%10] + rp(x//10,n-1)

def ron(pg, gi, vi, vo, reb, gem): #run one: program, index, value_in, value_out, relative base, global error-printing mode.
    op = pg[gi]%100 #opcode
    np = {1:3,2:3,3:1,4:1,5:2,6:2,7:3,8:3,9:1,99:0} # number of parameters
    try:
        mp = rp(pg[gi]//100,np[op]) #mode parameters
    except KeyError:
        print("HCF-mp",pg,gi,vi,vo,op)
    ao = [pg[gip] for gip in range(gi+1,gi+np[op]+1)] #parameters of the active opcode pg[gi]
    ar = []
    for i in range(len(ao)):
        if mp[i] == 1:
            ar.append(ao[i])
        elif mp[i] == 0:
            try:
                ar.append(pg[ao[i]])
            except KeyError:
                ar.append(0)
                if gem:
                    print("HCF-ar.append when mode = 0, gi=",gi,ao)
        elif mp[i] == 2:
            try:
                ar.append(pg[reb+ao[i]])
            except KeyError:
                ar.append(0)
                if gem:
                    print("HCF-ar.append when mode = 2, gi=",gi,ao)
    if gem and ao:
        wtm = str({1:ao[-1], 0:'.'}[{1:1, 2:1, 3:1, 4:0, 5:0, 6:0, 7:1, 8:1, 9:1, 99:0}[op]])
        print(f"Write:{wtm:4} gil:{gi:4}", 
            "op", op, ar, vi,
#            {True:vi, None:''}[vi[0] and True], 
            "found at:", ao  
        ) #references
#    if ao and (op==4) and ar == :
    if op == 1 and mp[-1] < 2:
        pg[ao[-1]] = ar[0] + ar[1]    
        return (pg, gi + np[op] + 1, vi, vo, reb)
    if op == 1 and mp[-1] == 2:
        pg[reb+ao[-1]] = ar[0] + ar[1]    
        return (pg, gi + np[op] + 1, vi, vo, reb)        
    if op == 2 and mp[-1] < 2:
        pg[ao[-1]] = ar[0] * ar[1]        
        return (pg, gi + np[op] + 1, vi, vo, reb)
    if op == 2 and mp[-1] == 2:
        pg[reb+ao[-1]] = ar[0] * ar[1]        
        return (pg, gi + np[op] + 1, vi, vo, reb)    
    if op == 3 and mp[-1] < 2:
#        print("op3", mp, vi)
        try:
            pg[ao[-1]] = vi[-1]
            vi = vi[:-1]
        except IndexError:
            print("HCF-3",gi,vi,op,mp,ao,ar)
        return (pg, gi + np[op] + 1, vi, vo, reb)
    if op == 3 and mp[-1] == 2:
        try:
            pg[reb+ao[-1]] = vi[-1]
            vi = vi[:-1]
        except IndexError:
            print("HCF-3",gi,vi,op,mp,ao,ar)
        return (pg, gi + np[op] + 1, vi, vo, reb)
    if op == 4:
        vo.append(ar[0])
        return (pg, gi + np[op] + 1, vi, vo, reb)
    if op == 5:
        return (pg, {True:ar[1], False:gi + np[op]+1}[ar[0] and True], vi, vo, reb)
    if op == 6:
        return (pg, {True:gi + np[op]+1, False: ar[1]}[ar[0] and True], vi, vo, reb)
    if op == 7 and mp[-1] < 2:
        pg[ao[-1]] = {True:1, False:0}[ar[0] < ar[1]]
        return (pg, gi + np[op] + 1, vi, vo, reb)    
    if op == 7 and mp[-1] == 2:
        pg[reb+ao[-1]] = {True:1, False:0}[ar[0] < ar[1]]
        return (pg, gi + np[op] + 1, vi, vo, reb)
    if op == 8 and mp[-1] < 2: 
        pg[ao[-1]] = {True:1, False:0}[ar[0] == ar[1]]
        return (pg, gi + np[op] + 1, vi, vo, reb)
    if op == 8 and mp[-1] == 2: 
        pg[reb+ao[-1]] = {True:1, False:0}[ar[0] == ar[1]]
        return (pg, gi + np[op] + 1, vi, vo, reb)        
    if op == 9:
        reb += ar[0]
        return (pg, gi + np[op] + 1, vi, vo, reb)
    if op == 99:
        return(pg,gi,vi,vo,reb)

def mou(xi,yi,cuo): # move xi,yi in direction cuo
    if cuo in [1,2]:
        return xi,yi+cuo*2-3 # cuo=1 => yi += -1, North. 
    if cuo in [3,4]:
        return xi+cuo*2-7,yi # cuo=3 => xi += -1, West.

def asco(maw):
    if min([x for (x,y) in maw]) >=0  and min([y for (x,y) in maw]) >= 0:
        for yi in range(max([y for (x,y) in maw])+1):
            row = ''
            for xi in range(max([x for (x,y) in maw])+1):
                if (xi,yi) in maw:
                    row += maw[(xi,yi)]
                else:
                    row += ' '
            print(row)

def dro(pg,vi,xi,yi,gem): #drone or robot search
    vinit = [hau for hau in vi]
    vi = [hau for hau in vinit]
    gi,reb, oi, ii = 0,0,0,len(vinit)-1 # oi = output index, input index
    vo = []
    map = {(xi,yi):'.'}
    while pg[gi] != 99 and not 2 in vo and not (len(vi) == 0 and len(vo)> oi) and ii > -1:
#        if joi and not vi:
#            vi = [joi[-1][0]]
#            joi = joi[:-1]
        (pg, gi, vi, vo, reb) = ron(pg, gi, vi, vo, reb, gem)
        if len(vo) > oi:
            if vo[-1] == 0:
                map[mou(xi,yi,vinit[ii])] = '#'
            if vo[-1] == 1:
                xi,yi = mou(xi,yi,vinit[ii])
                map[(xi,yi)] = '.'
            if vo[-1] == 2:
                xi,yi = mou(xi,yi,vinit[ii])
                map[(xi,yi)] = 'x'
            ii += -1
#            print(vo[-1])
            oi += 1
#            asco(map)
    return vo[-1], map

with open('y2019day15v1.txt', 'r') as file:
    t = [x.strip() for x in file.readlines()]
for u in t:
    pj = [int(x) for x in u.split(",")]

andi = {0:4,1:1,2:3,3:2}
dian = {andi[k]:k for k in andi}
rhr = [[(i+j)%4 for j in range(-1,3)]    for i in range(4)] #right hand rule
lhr = [[(i+j)%4 for j in range(1,-3,-1)] for i in range(4)]
#rir = [[andi[(dian[i]+j)%4] for j in range(-1,3)] for i in [4,1,2,3]]


def runrule(rule, xi, yi, ve, pa, lim):
    pat = [x for x in pa]
    fin, fn, ct = 1,1, 0 
    while ct < lim and fn == 1: #fin != 2: #   at 530 it repeats. (xi,yi,ve) != (23,20,1)
        ct += 1
        fn,di = 0,0
        while di < 4 and fn == 0:
            pg = {i:pj[i] for i in range(len(pj))}
            fin, maw = dro(pg,[andi[rule[ve][di]]]+pat,xi,yi,0)
            if fin == 1 or fin ==2:
                pat = [andi[rule[ve][di]]]+pat
                ve = rule[ve][di]
                fn = 1
            if fin == 0:
                di += 1
    #    
    #        if fin == 2:
    #            print(pat)
        if len(pat) % (106) == 0:
            asco(maw)
            print(len(pat), len(maw))
    return maw

maw = runrule(
    rhr, 23,20,3, [andi[3]], 800)|runrule(
    lhr, 23,20,3, [andi[3]], 800)

# len(pat) can increase arbitrarily, but len(maw) inc rases to 530 and stops. 

strategy='''
"always go right" is a strategy for exploring a maze.
You will go into every tunnel. You will then turn and come out of the tunnel.

This strategy works *only* if the labyrinth is tree-shaped. Otherwise, this strategy is llikely to get stuck in a cycle and *not* trace the whole tree. 

Check whether the maze is acyclic. 
Count the edges. If the number of vertices is 1 + the number of edges, then tree.

len(maw) == 786
'''

# count edges:

for k,v in list(maw.items()):
    if v == '#':
       del maw[k]

edg = {}
neighbours = {}
for (x,y) in maw:
    neighbours[(x,y)] = []
    for (a,b) in [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]:
        if (a,b) in maw:
            this_edge = [(a,b),(x,y)]
            this_edge.sort()
            edg[tuple(this_edge)] = 1
            neighbours[(x,y)].append((a,b))

disa = {0:0}
disg = {(23,20):0}
mawk = list(maw.keys())
for iul in range(1,len(mawk)):
    disa[iul] = disa[iul-1]+1
    (x,y) = mawk[iul]
    disg[(x,y)] = disa[iul-1]+1
    for (a,b) in [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]:
        if (a,b) in mawk[:iul]:
            disg[(x,y)] = min(disg[(x,y)],disg[(a,b)]+1)

if min([x for (x,y) in maw]) >=0  and min([y for (x,y) in maw]) >= 0:
    for yi in range(max([y for (x,y) in maw])+1):
        row = ''
        for xi in range(max([x for (x,y) in maw])+1):
            if (xi,yi) in maw:
                row += str(disg[(xi,yi)]%10)
            else:
                row += ' '
        print(row)

comment_labyrinth='''
   87654 654323456 2345678 65456 6545678 2
   9   3 7   1   7 1 5     7 3   7 3   9 1
   0 012 890 0 09890 6 21098 21098 210 0 0
   1 9 3   1 9 1     7 3             9 1 9
   2 8 4 432 8 2 098 8 4 654321012 678 2 8
     7 5 5   7   1 7   5     3 9   5   3 7
   456 6 678 65432 654 67890 4 876 432 456
   3       9         3     1     5   1   7
   2 6543210   23456 234 0 2 01234 890 098
   1 7         1   7 1 5 9 3 9 3   7   1  
   098     678 098 890 678 4 8 4 456 43234
           5 9   7         5 7 5 3        
   234 01234 0   65432109876 6 6 210987654
   1 5 9     1             7 5 7         3
   0 678 0 432 23456789012 8 4 89012345  2
   9     9 5   1         3 9 3           1
   8 210 876 21098 8 87654 012   234567890
   7 3 9 9       7 7 9           1   7    
   654 8 0123456 6 6 012345678   0 098 012
   7   7       7 5 5 1       9   9     9 3
   890 6 4321098 4 432 0 234 012 8 45678 4
   9   5       9 3 5   1 1     3 7 3     5
   0 234 21098 012 678 2 098765456 2 456 6
     1   3   7       9 3           1 3   7
   890 654 0 6543210 0 456789012 890 210 8
   7 1 7   9       9           3 7   3 9 9
   6 2 8 0987678 4 8 2109890 6 456 654 8 0
   5   9     5 9 3 7 3   7 1 5     7   7 1
   43210 01234 0 2 654 456 234 2109890 6 2
   5     9     1 1     3       3       5 3
   6 234 87654 2 09876 210987654 098 234 4
   7 1 5 9   3 3     5             7 1   5
   890 6 0 012 456 23456 21098765456 09876
       7 1 9     7 1   7         3 7      
   8 098 2 876 0 890 4 8901234 012 89012 2
   7 1       5 9     3       5 9       3 1
   6 23456 234 8 21012 2109876 876 234 4 0
   5     7 1   7 3 9   3         5 1   5 9
   432109890 87654 876545678901234 0987678
'''

for k,v in list(maw.items()):
    if v == 'x':
       print("pt1",disg[k])

def fillo(num):
    for k,v in list(maw.items()):
        if v == 'x':
            disg2 = {k:0}

    seen = list(disg2.keys())
    exha = 0
    while exha in range(len(seen)) and disg2[seen[exha]] < num:
        for (x,y) in neighbours[seen[exha]]:
            if (x,y) not in seen:
                seen.append((x,y))
                disg2[(x,y)] = disg2[seen[exha]]+1
        exha += 1
    print("pt2",max(disg2.values()))

    if min([x for (x,y) in maw]) >=0  and min([y for (x,y) in maw]) >= 0:
        for yi in range(max([y for (x,y) in maw])+1):
            row = ''
            for xi in range(max([x for (x,y) in maw])+1):
                if (xi,yi) in maw:
                    if (xi,yi) in disg2:
                        row += str(disg2[(xi,yi)]%10)
                    else:
                        row += '.'
                else:
                    row += ' '
            print(row)

fillo(440)

comment_on_speed_to_fill='''
fillo(440)
   45678 678901234 0123456 67890 6789012 6
   3   9 5   1   5 9 3     5 9   5 9   3 5
   2 210 432 2 87678 4 01234 01234 012 4 4
   1 3 1   1 3 9     5 9             3 5 3
   0 4 2 890 4 0 234 6 8 654321012 654 6 2
     5 3 7   5   1 5   7     3 9   7   7 1
   876 4 654 67890 678 65432 4 876 890 890
   9       3         9     1     5   1   1
   0 6789012   09876 012 8 0 01234 432 432
   1 5         1   5 1 3 7 9 9 3   5   5  
   234     654 234 432 456 8 8 4 876 87678
           7 3   5         7 7 5 9        
   098 21098 2   67890123456 6 6 012345678
   1 7 3     1             7 5 7         9
   2 654 6 890 09876543210 8 4 89012345  0
   3     5 7   1         9 9 3           1
   4 012 456 43234 0 45678 012   098765432
   5 9 3 3       5 9 3           1   7    
   678 4 2109876 6 8 210987654   2 098 210
   7   5       5 7 7 3       3   3     3 9
   890 6 0987654 8 654 2 678 210 4 87654 8
   9   7       3 9 7   1 5     9 5 9     7
   0 098 01234 210 890 0 432109876 0 234 6
     1   9   5       1 9           1 1   5
   432 678 4 6789012 2 876543210 432 012 4
   5 3 5   3       3           9 5   9 3 3
   6 4 4 4321012 8 4 0123456 2 876 678 4 2
   7   3     9 3 7 5 9   5 7 1     5   5 1
   89012 45678 4 6 678 876 890 0123456 6 0
   9     3     5 5     9       9       7 9
   0 678 21098 6 43210 012345678 432 098 8
   1 5 9 3   7 7     9             1 1   7
   234 0 4 456 890 67890 65432109890 23456
       1 5 3     1 5   1         7 1      
   2 432 6 210 4 234 8 2345678 456 23456 .
   1 5       9 3     7       9 3       7 5
   0 67890 678 2 65456 6543210 210 ... 8 4
   9     1 5   1 7 3   7         9 5   9 3
   876543234 21098 210989012345678 4321012
                                     '''
