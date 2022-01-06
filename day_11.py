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

def tru(pg,vi,vo,hul, gem): # vi = values input; vo = values outout
#    global hul
    gi = 0 # global index
    reb = 0
#    hul = {} # there is no hull color; part 1.
    lox = 0
    loy = 0
    vec = 0 # 0 == up, add 
    while pg[gi] != 99:
        if (lox,loy) in hul:
            vi = [hul[(lox,loy)]]
        else:
            vi = [0]
        (pg, gi, vi, vo, reb) = ron(pg, gi, vi, vo, reb, gem)
        if len(vo) > 1:
            hul[(lox,loy)] = vo[0]
            vec = (vec + vo[1]*2-1)%4
            if vec == 0:
                loy += 1
            if vec == 1:
                lox += 1
            if vec == 2:
                loy += -1
            if vec == 3:
                lox += -1
            vo = [] 
    return hul

# len(hul) == 1787 is too low. 
# hypothesis: my realization of vec, lox, loy and motion is wrong.
# I am too slow to read the "draw" command? Perhaps the robot draws and then quits.

with open('y2019day11v1.txt', 'r') as file:
    t = [x.strip() for x in file.readlines()]
for u in t:
    pj = [int(x) for x in u.split(",")]
    pg = {i:pj[i] for i in range(len(pj))}

#print("p1",len(tru(pg,[],[],{},0)))
reg = tru(pg,[],[],{(0,0):1},0)
xil = [x for (x,y) in reg]
yil = [y for (x,y) in reg]
reg1 = {(x-min(xil),y-min(yil)):reg[(x,y)] for (x,y) in reg if reg[(x,y)] == 1}
xil = [x for (x,y) in reg1]
yil = [y for (x,y) in reg1]
yra = range(max(yil)+1)
xra = range(max(xil)+1)
sid = [['.' for il in xra] for jil in yra]
for (x,y) in reg1:
    sid[max(yil)-y][x] = '#'
[''.join(row) for row in sid]

comment = '''
That line 149 inverts, suggests that I've got my 2d turing machine somewhat backwards vs the intention.
'''
