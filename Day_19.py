
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

def run(pg,vi,vo,gem): # vi = values input; vo = values outout
    gi = 0 # global index
    reb = 0
    while pg[gi] != 99:
        (pg, gi, vi, vo, reb) = ron(pg, gi, vi, vo, reb, gem)
    return vo #, pg[0]

def inbeam(x, y):
    pj = [int(x) for x in t[0].split(",")]
    pg = {i:pj[i] for i in range(len(pj))}
    vo = run(pg,[x,y],[],0)
    return vo[0]

with open('y2019day19v0.txt', 'r') as file:
    t = [x.strip() for x in file.readlines()]

ct, tb = 0, {}
for py in range(45):
    op = ''
    tb[py] = []
    for px in range(50):
        if inbeam(px,py):
            op+= '#'
            ct += 1
            tb[py].append(px)
        elif px == py+py//8 - 1:
            op += chr(92)
        elif px == py+py//4 + 2:
            op += chr(92)
        else:
            op += '.'
    print(op)

#tbmat = [[{True:'#',False:'.'}[(y,x) in tb] for x in range(50)] for y in range(50)]
#print('\n'.join([''.join([tbmat[i][j] for j in range(50)]) for i in range(50)]))

#"in tractor beam iff"
#x >= y + y//8 

print("Part 1", ct)

x,y,maxsq = 0,0,1
while maxsq < 99:
    if inbeam(x+99,y) == False:
        y += 1
    elif inbeam(x,y+99) == False:
        x += 1
    else:
        maxsq = 99

print('Part2',y*10000+x)
