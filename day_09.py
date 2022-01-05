comment = '''
...available memory should be much larger than the initial program. Memory beyond the initial program starts with the value 0 and can be read or written like any other memory.
To write to an arbitrary memory location, treat the program as a dictionary, not a list.
To read from memory locations not yet written, 1. read via a function that returns 0 as a default. Or try/except.
'''

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

with open('y2019day09v1.txt', 'r') as file:
    t = [x.strip() for x in file.readlines()]
for u in t:
    pj = [int(x) for x in u.split(",")]
    pg = {i:pj[i] for i in range(len(pj))}
    print("p1",run(pg,[1],[],0))
    print("p2",run(pg,[2],[],0))

'''
Lines 46-51 could be collapsed to a line similar to 
        return (pg, {True:ar[1], False:gi + np[op]+1}[ar[0] and True], vi, vo, reb)
Use of ar, which is either ao or reb+ao, could prevent the need to split on ao/ reb+ao.
'''
