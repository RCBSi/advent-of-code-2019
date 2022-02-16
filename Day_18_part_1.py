with open('y2019day18v1.txt', 'r') as file:
    t = [x.strip() for x in file.readlines()]

def iscap(c):
    return ord(c) in range(65,65+26) # 65=A

def islowercase(c):
    return ord(c) in range(97,97+26) # 97=a

# prune dead ends.
def enough_hash_neighbours(i,j):
    nsew = [[j,i+1],[j,i-1],[j+1,i],[j-1,i]]
    if t[j][i] == '.' or iscap(t[j][i]):
        return sum([t[l][k] == '#' for [l,k] in nsew]) >= 3

cou,nt = 1,0
while cou > 0:
    cou = 0 
    for j in range(1,len(t)-1):
        for i in range(1,len(t[j])-1):
            if enough_hash_neighbours(i,j):
                before = [x[i-1:i+2] for x in t[j-1:j+2]]
                t[j] = t[j][:i]+'#'+t[j][i+1:]
#                print(before, [x[i-1:i+2] for x in t[j-1:j+2]])
                cou += 1
    nt += cou

# walk the maze.
def opt(i,j,dir): # where can we go from (i,j) -- forward in direction dir or right or left of dir?
    ne = [(i,j+1),(i-1,j),(i,j-1),(i+1,j)]
    thr = [(ne[k],k) for k in [(dir-1)%4, dir, (dir+1)%4]]
    return [((m,n),dir) for ((m,n),dir) in thr if t[m][n]!='#']

if '\n'.join(t).index('@') == 40*82+40: #kdp = {} #keys to doors, predecessor.
    co = [39,41]
    kfd = {((w,x),(y,z)):abs(w-y)+abs(x-z) for x in co for y in co for z in co for w in co if abs(w-y)+abs(x-z) > 0 and w*100+x <= y*100+z} #keys and forks, distance.
else:
    kfd = {}

kds = {x:[] for lin in t for x in lin if iscap(x) or x == '@'} #keys behind doors, successorr.
ddp = {} #doors to doors, predecessor.

def ru(i,j,dir,dis,doo,foo):
    if islowercase(t[i][j]):
        kfd[(t[i][j],foo)]= dis
        dis= 0
        foo= t[i][j]
        if t[i][j] not in kds[doo]:
            kds[doo].append(t[i][j])
    if iscap(t[i][j]):
        ddp[t[i][j]]= doo
        doo = t[i][j]
    oop= opt(i,j,dir)
    if len(oop) > 1:
        kfd[((i,j),foo)]= dis
        dis= 0
        foo= (i,j)
    for ((i1,j1),dir1) in oop:
        ru(i1,j1,dir1,dis+1,doo,foo)

if '\n'.join(t).index('@') == 40*82+40:
    ru(39,38,2,1,'@',(39,39))
    ru(39,42,0,1,'@',(39,41))
    ru(41,38,2,1,'@',(41,39))
    ru(42,41,3,1,'@',(41,41))

test_cases_centers = [(1,1), (4,8),(3,6), (1,15), (1,5)]
for (i,j) in test_cases_centers:
    if i < len(t):
        if j < len(t[i]):
            if t[i][j] == '@':
                ru(i,j,0,0,'@', (i,j))
                ru(i,j,1,0,'@', (i,j))
                ru(i,j,2,0,'@', (i,j))
                ru(i,j,3,0,'@', (i,j))

d = {f:{e:kfd[(e,f)]} for e,f in kfd}|{e:{f:kfd[(e,f)]} for e,f in kfd}
for e,f in kfd:
    d[f][e] = kfd[(e,f)]
    d[e][f] = kfd[(e,f)]
    # d is K4 and then a tree.

for (e,f) in kfd:
    for g in d[f]:
        if g != e:
            if e not in d[g]:
                d[g][e] = d[f][g]+kfd[(e,f)]
            else: 
                d[g][e] = min(d[e][g],d[f][g]+kfd[(e,f)])
            if g not in d[e]:
                d[e][g] = d[f][g]+kfd[(e,f)]
            else:
                d[e][g] = min(d[e][g],d[f][g]+kfd[(e,f)])
    for g in d[e]:
        if g != f:
            if f not in d[g]:
                d[g][f] = d[e][g]+kfd[(e,f)]
            else: 
                d[g][f] = min(d[f][g],d[e][g]+kfd[(e,f)])
            if g not in d[f]:
                d[f][g] = d[e][g]+kfd[(e,f)]
            else:
                d[f][g] = min(d[f][g],d[e][g]+kfd[(e,f)])

d['@']={}
for e in kds['@']:
    if '\n'.join(t).index('@') == 40*82+40:
        d['@'][e] = 2+min([d[e][a] for a in [(x,y) for x in co for y in co]])
    for (i,j) in test_cases_centers:
        if i < len(t):
            if j < len(t[i]):
                if t[i][j] == '@':
                    d['@'][e] = d[(i, j)][e]

dd = {f:{e:d[f][e] for e in d[f].keys() if len(e)==1} for f in d.keys() if len(f)==1}

dds = {x:[] for x in ddp.values()}
for k in ddp:
    dds[ddp[k]].append(k)

pos, lp, llp ='@ ',2, 0
while lp > llp:
    for i in range(len(pos)-1):
        c,nex,c_fin = pos[i],pos[i+1], chr(ord(pos[i])-27)
        if (ord(c) >=64 and ord(c) <= 90) and nex != '[':
            new = ''
            if c in kds:
                new+= ''.join(kds[c])
            if c in dds:
                new+= ''.join(dds[c])
            if len(new)>0:
                pos = pos[:i+1]+'['+new+c_fin+']'+pos[i+1:]
    lp, llp = len(pos), lp
pos = pos[2:-3]

def accessible_keys(pos):
    acc = []
    i = 0
    while i < len(pos):
        if ord(pos[i]) in range(97,123):
            acc.append(pos[i])
        elif pos[i] == '[':
            i = pos.index(chr(ord(pos[i-1])-27),i)+1
        i+=1
    return acc

def open_door(pos, d):
    pos = pos.replace(
            d.upper()+'[',''
        ).replace(
            chr(ord(d.upper())-27)+']',''
        ).replace(d.lower(),'')
    return pos

def edo(ct, loc, pos, seq, oeo): 
    global mindist, tries
    ac = accessible_keys(pos)
    if len(ac) == 0:
        if ct < mindist:
            mindist = ct
    if ct < mindist:
        for a in ac:
            pos1 = open_door(pos, a)
            ct1 = ct + dd[loc][a]
            if pos1+a not in seen or oeo:
                seen[pos1+a] = (seq+a,ct1)
                edo(ct1, a, pos1, seq+a,oeo)
            elif pos1+a in seen and seen[pos1+a][1] > ct1:
                seen[pos1+a] = (seq+a,ct1)
                edo(ct1, a, pos1, seq+a,oeo)

import time
start = time.time()
mindist = 10**30
seen = {}
edo(0,'@',pos, '', 0) # Too slow! 
s0 = {k:seen[k] for k in seen} #has oeo==0
print('\n'.join([x[-30:][:30] for x in t[-4:]]))
print(mindist, time.time()-start)

'''seen:
 the state of the tree of doors and keys + the location : the length of the sequence that got here.
 'uA[e&]scaU[t:]i': ('bzwdglhpfnkjqxvromyi', 3790),
 'iA[e&]scI[a.]tu': ('bzwdglhpfnkjqxvromyu', 3756),
 'iuA[e&]cI[a.]U[t:]s': ('bzwdglhpfnkjqxvromys', 3212),
 'iuA[e&]sI[a.]U[t:]c': ('bzwdglhpfnkjqxvromyc', 3146),
 'uA[e&]saU[t:]i': ('bzwdglhpfnkjqxvromyci', 3870),
 'iA[e&]sI[a.]tu': ('bzwdglhpfnkjqxvromycu', 3836),
 'iuA[e&]I[a.]U[t:]s': ('bzwdglhpfnkjqxvromycs', 3292),
 'iuA[e&]xX[vV[rR[o7]O[mM[y2]Y[c>]4];]=]I[a.]U[t:]s': ('bzwdglhpfkjqns', 2408),
 'iuqA[e&]svV[rR[o7]O[mM[y2]Y[c>]4];]I[Q[a6].]U[t:]x': ('bzwdglhpfnkjx', 2198),
 'uqA[e&]svV[rR[o7]O[mM[y2]Y[c>]4];]Q[a6]U[t:]i': ('bzwdglhpfnkjxi', 2806),
 'iqA[e&]svV[rR[o7]O[mM[y2]Y[c>]4];]I[Q[a6].]tu': ('bzwdglhpfnkjxu', 2360),
 'iuA[e&]svV[rR[o7]O[mM[y2]Y[c>]4];]I[a.]U[t:]q': ('bzwdglhpfnkjxq', 2292),
 'iuqA[e&]vV[rR[o7]O[mM[y2]Y[c>]4];]I[Q[a6].]U[t:]s': ('bzwdglhpfnkjxs', 2904),
 'iuqA[e&]srR[o7]O[mM[y2]Y[c>]4]I[Q[a6].]U[t:]v': ('bzwdglhpfnkjxv', 2952),
'''
