import numpy
from scipy.stats import rankdata
import math

with open('y2019day12v1.txt', 'r') as file:
    tex = [x.strip() for x in file.readlines()]
pos = []
for roa in tex:
    lok = []
    sta = 0
    while '=' in roa[sta+1:]:
        sta = roa.index('=',sta+1)
        if ',' in roa[sta:]:
            end = roa.index(',',sta)
        else:
            end = roa.index('>',sta)
        lok.append(int(roa[sta+1:end]))
    pos.append(lok)

tio = lambda x: 3 - (x-1) * 2
veo = numpy.array([[0]*len(pos[0])]*len(pos))
ste = 0
while ste < 1000: # for ppart1
#    seen[tuple(map(tuple, numpy.concatenate([pos,veo], axis=1)))] = 1
    if ste%100 == 0:
        print("after",ste,"steps:")
        print(numpy.concatenate([pos,veo], axis=1))
    aks = tio(rankdata(pos, axis=0)).astype(int)
    veo = numpy.add(veo,aks)
    pos = numpy.add(pos,veo)
    ste += 1
print("after",ste,"steps:")
print(numpy.concatenate([pos,veo], axis=1))
abe = lambda x: abs(x)
print("pt1",numpy.dot(numpy.sum(abe(pos),axis=1),numpy.sum(abe(veo),axis=1)))

reu = []
for fac in range(len(['x','y','z'])):
    po = pos[:,fac]
    ve = veo[:,fac]
    seen = {}
    ste = 0
    while tuple(numpy.concatenate([po,ve])) not in seen:
        seen[tuple(numpy.concatenate([po,ve]))] = ste
        ste += 1
        aks = tio(rankdata(po)).astype(int)
        ve = numpy.add(ve,aks)
        po = numpy.add(po,ve) 
    reu.append([seen[tuple(numpy.concatenate([po,ve]))],ste])

if reu[0][0] == 0 and reu[1][0] == 0 and reu[2][0] == 0:
    print("pt2, math.lcm of ",[reu[i][1] for i in range(3)]) 

