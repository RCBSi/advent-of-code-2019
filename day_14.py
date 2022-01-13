with open('y2019day14v1.txt', 'r') as file:
    tei = [x.strip() for x in file.readlines()]

def rad(rea, pre, pro, deg): #add a reagent as a predecessor/successor of a product, nth degree.
    if pro not in pre:
        pre[pro] = {rea:deg}
    if pro in pre:
        if rea not in pre[pro]:
            pre[pro][rea] = deg
        if rea in pre[pro]:
            pre[pro][rea] = max(pre[pro][rea],deg)
    return pre

pre = {}
rel = {}
suc = {}
for ul in tei: # with one pass through tei, compute the entire "lattice" or partially ordered set with distances.
    se = ul.index(' => ')
    mou = ul[:se].split(', ') + ul[se+4:].split(', ')
    mous = [xi.split(' ')[1] for xi in mou]
    rel[mous[-1]] = [xi.split(' ') for xi in mou]
    for che in mous[:-1]: # update predecessors.
        rad(che, pre, mous[-1], 1)
        rad(mous[-1], suc, che, 1)
        if che in pre:
            for rea in pre[che]:
                rad(rea, pre, mous[-1], pre[che][rea]+1)
                rad(mous[-1], suc, rea, pre[che][rea]+1)
        if mous[-1] in suc:
            for pro in suc[mous[-1]]:
                rad(pro, suc, che, suc[mous[-1]][pro]+1)
                rad(che, pre, pro, suc[mous[-1]][pro]+1)
        for rea in pre[mous[-1]]:
            if mous[-1] in suc:
                for pro in suc[mous[-1]]:
                    rad(pro, suc, rea, suc[mous[-1]][pro]+pre[mous[-1]][rea])
                    rad(rea, pre, pro, suc[mous[-1]][pro]+pre[mous[-1]][rea])

def cei(x,y):
    if x%y == 0:
        return x//y
    else:
        return x//y+1

def sat(pref,iin):
    nii = {xi:0 for xi in pref}|{'FUEL':iin}
    byran = range(1+max([pref[xi] for xi in pref]))
    byr = {nu:[] for nu in byran}
    byr[0] = ['FUEL']
    for el in pref:
        byr[pref[el]].append(el)
    for nu in byran:
        for el in byr[nu]:
            if el != 'ORE': # satisy nii[el] using rel[el]
                mu = cei(nii[el],int(rel[el][-1][0]))
                for nit in rel[el][:-1]:
                    nii[nit[1]]+= int(nit[0])*mu
#                print(el, nii[el], rel[el])
    return nii

print('pt1 ORE',sat(pre['FUEL'],1)['ORE'])

sat(pre['FUEL'],1)['ORE']

produ = 0
reage = sat(pre['FUEL'],produ)['ORE'] # reagents and products.
ival = 10**5
while ival > 0:
    while reage < 1000000000000:
        produ += ival
        reage = sat(pre['FUEL'],produ)['ORE']
    produ -= ival
    reage = sat(pre['FUEL'],produ)['ORE']
    ival = ival//10

if sat(pre['FUEL'],produ)['ORE'] <= 1000000000000 and sat(pre['FUEL'],produ+1)['ORE'] > 1000000000000:
    print('pt2', produ)
