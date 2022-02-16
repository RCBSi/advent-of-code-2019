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

tnew = ['@#?', '###', '>#='] # [[64, 35, 63], [35, 35, 35], [62, 35, 61]]

#t[40][40] == '@'
for i in range(3):
    t[39+i] = t[39+i][:39] + tnew[i] + t[39+i][42:]

# walk the maze.
def opt(i,j,dir): # where can we go from (i,j) -- forward in direction dir or right or left of dir?
    ne = [(i,j+1),(i-1,j),(i,j-1),(i+1,j)]
    thr = [(ne[k],k) for k in [(dir-1)%4, dir, (dir+1)%4]]
    return [((m,n),dir) for ((m,n),dir) in thr if t[m][n]!='#']

#if '\n'.join(t).index('@') == 40*82+40: #kdp = {} #keys to doors, predecessor.
#    co = [39,41]
#    kfd = {((w,x),(y,z)):abs(w-y)+abs(x-z) for x in co for y in co for z in co for w in co if abs(w-y)+abs(x-z) > 0 and w*100+x <= y*100+z} #keys and forks, distance.
#else:

kfd = {}
kds = {x:[] for lin in t for x in lin if ord(x) in range(61,91)} #keys behind doors, successorr.
ddp = {} #doors to doors, predecessor.

def ru(i,j,dir,dis,doo,foo):
    if islowercase(t[i][j]):
        kfd[(t[i][j],foo)]= dis
        dis= 0
        foo= t[i][j]
        if t[i][j] not in kds[doo]:
            kds[doo].append(t[i][j])
    if ord(t[i][j]) in range(61,91):
        ddp[t[i][j]]= doo
        doo = t[i][j]
    oop= opt(i,j,dir)
    if len(oop) > 1:
        kfd[((i,j),foo)]= dis
        dis= 0
        foo= (i,j)
    for ((i1,j1),dir1) in oop:
        ru(i1,j1,dir1,dis+1,doo,foo)

if 1==1:
    ru(39,38,2,1,chr(64), (39,39))
    ru(39,42,0,1,chr(63),(39,41))
    ru(41,38,2,1,chr(62),(41,39))
    ru(42,41,3,1,chr(64),(41,41))

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

d[chr(64)] = d[(39,39)]
d[chr(63)] = d[(39,41)]
d[chr(62)] = d[(41,39)]
d[chr(61)] = d[(41,41)]

dd = {f:{e:d[f][e] for e in d[f].keys() if len(e)==1} for f in d.keys() if len(f)==1}

dds = {x:[] for x in ddp.values()}
for k in ddp:
    dds[ddp[k]].append(k)

pos, lp, llp =' '.join([chr(i) for i in range(61,65)])+' ',2, 0
while lp > llp:
    for i in range(len(pos)-1):
        c,nex,c_fin = pos[i],pos[i+1], chr(ord(pos[i])-30)
        if (ord(c) in range(61,91)) and nex != '[':
            new = ''
            if c in kds:
                new+= ''.join(kds[c])
            if c in dds:
                new+= ''.join(dds[c])
            if len(new)>0:
                pos = pos[:i+1]+'['+new+c_fin+']'+pos[i+1:]
    lp, llp = len(pos), lp


def accessible_keys(pos):
    acc = []
    i = 0
    while i < len(pos):
        if ord(pos[i]) in range(97,123):
            acc.append(pos[i])
        elif pos[i] == '[':
            i = pos.index(chr(ord(pos[i-1])-30),i)+1
        i+=1
    return acc

def open_door(pos, d):
    pos = pos.replace(
            d.upper()+'[',''
        ).replace(
            chr(ord(d.upper())-30)+']',''
        ).replace(d.lower(),'')
    return pos

for i in range(61,65):
    pos = open_door(pos,chr(i))
    # ['@', '?', '>', '=']

def edo(ct, locv, pos, seq, oeo): 
    global mindist, tries
    ac = accessible_keys(pos)
    if len(ac) == 0:
        if ct < mindist:
            mindist = ct
    if ct < mindist:
        for a in ac:
            moves = [a in dd[l] for l in locv ].index(True)
            pos1 = open_door(pos, a)
            ct1 = ct + dd[locv[moves]][a]
            locv1 = [l for l in locv]
            locv1[moves] = a
            indexme = pos1 + ''.join(locv1)
            if indexme not in seen or oeo:
                seen[indexme] = (seq+a,ct1)
                edo(ct1, locv1, pos1, seq+a,oeo)
            elif indexme in seen and seen[indexme][1] > ct1:
                seen[indexme] = (seq+a,ct1)
                edo(ct1, locv1, pos1, seq+a,oeo)

import time
start = time.time()
mindist = 10**30
locv = [chr(i) for i in range(64,60,-1)] 
seen = {}
edo(0,locv,pos, '', 0) 
s0 = {k:seen[k] for k in seen} #has oeo==0
print('\n'.join([x[-30:][:30] for x in t[-4:]]))
print(mindist, time.time()-start)

todo_comment = '''
add the four initial spots to dd. 
in edo the pos is now not connected. If you chose to go next to key a,
... is there any sense in going partway to a, pausing, then finishing?
I think not. We can assume that each step is "from loc to a key."
'''
