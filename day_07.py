def rp(x,n): #read n parameters as digits from n.
    if n==0:
        return []
    else:
        return [x%10] + rp(x//10,n-1)

def ron(pg, gi, vi, vo, gem): #run one: program, index, value_in, global error-printing mode.
    op = pg[gi]%100 #opcode
    np = {1:3,2:3,3:1,4:1,5:2,6:2,7:3,8:3,99:0} # number of parameters
    try:
        mp = rp(pg[gi]//100,np[op]) #mode parameters
    except KeyError:
        print("HCF-mp",pg,gi,vi,vo,op)
    ao = pg[gi+1:gi+np[op]+1] #parameters of the active opcode pg[gi]
    ar = []
    for i in range(len(ao)):
        if mp[i] == 1:
            ar.append(ao[i])
        elif mp[i] == 0:
            try:
                ar.append(pg[ao[i]])
            except IndexError:
                print("HCF-ar.append when mode = 0, gi=",gi,ao)
    if gem and ao:
        wtm = str({1:ao[-1], 0:'.'}[{1:1, 2:1, 3:1, 4:0, 5:0, 6:0, 7:1, 8:1, 99:0}[op]])
        print(f"Write:{wtm:4} gil:{gi:4}", 
            "op", op, ar, vi,
#            {True:vi, None:''}[vi[0] and True], 
            "found at:", ao  
        ) #references
    if op == 1:
        pg[ao[-1]] = ar[0] + ar[1]    
        return (pg, gi + np[op] + 1, vi, vo)
    if op == 2:
        pg[ao[-1]] = ar[0] * ar[1]        
        return (pg, gi + np[op] + 1, vi, vo)
    if op == 3:
        try:
            pg[ao[-1]] = vi[-1]
            vi = vi[:-1]
        except IndexError:
            print("HCF-3",gi,vi,op,mp,ao,ar)
        return (pg, gi + np[op] + 1, vi, vo)
    if op == 4:
        vo.append(ar[0])
        return (pg, gi + np[op] + 1, vi, vo)
    if op == 5:
        return (pg, {True:ar[1], False:gi + np[op]+1}[ar[0] and True], vi, vo)
    if op == 6:
        return (pg, {True:gi + np[op]+1, False: ar[1]}[ar[0] and True], vi, vo)
    if op == 7:
        pg[ao[-1]] = {True:1, False:0}[ar[0] < ar[1]]
        return (pg, gi + np[op] + 1, vi, vo)    
    if op == 8: 
        pg[ao[-1]] = {True:1, False:0}[ar[0] == ar[1]]
        return (pg, gi + np[op] + 1, vi, vo)
    if op == 99:
        return(pg,gi,vi,vo)

def run(pg,vi,vo,gem): # vi = values input; vo = values outout
    gi = 0 # global index
    while pg[gi] != 99:
        (pg, gi, vi, vo) = ron(pg, gi, vi, vo, gem)
    return vo #, pg[0]

def chainrun(pg, perm, vo, gem):
    for phase in perm:
        vo = run(pg,[vo[0],phase],[],gem)
    return vo

def orzero(outv):
    if outv:
        return outv[-1:]
    else:
        return [0]

def runparallel(pgm,vil,vom,gem):
    pgA=[x41 for x41 in pgm]
    pgB=[x41 for x41 in pgm]
    pgC=[x41 for x41 in pgm]
    pgD=[x41 for x41 in pgm]
    pgE=[x41 for x41 in pgm]
    giA=0
    giB=0
    giC=0
    giD=0
    giE=0
    [viA,viB,viC,viD,viE] = vil
    voA=[0]
    voB=[0]
    voC=[0]
    voD=[0]
    voE=[0]
#    for i15 in range(1):
    while [pgA[giA],pgB[giB],pgC[giC],pgD[giD],pgE[giE]] != [99]*5:
        ((pgA, giA, viA, voA),
        (pgB, giB, viB, voB),
        (pgC, giC, viC, voC),
        (pgD, giD, viD, voD),
        (pgE, giE, viE, voE)) = (
        ron(pgA, giA, viA, voA, gem),
        ron(pgB, giB, viB, voB, gem),
        ron(pgC, giC, viC, voC, gem),
        ron(pgD, giD, viD, voD, gem),
        ron(pgE, giE, viE, voE, gem))
        viA,viB,viC,viD,viE = orzero(voE),orzero(voA),orzero(voB),orzero(voC),orzero(voD)
        print(voE)
    return voE

def runsignal(pgm,vil,vom,gem):
    pgA=[x41 for x41 in pgm]
    pgB=[x41 for x41 in pgm]
    pgC=[x41 for x41 in pgm]
    pgD=[x41 for x41 in pgm]
    pgE=[x41 for x41 in pgm]
    giA=0
    giB=0
    giC=0
    giD=0
    giE=0
    [viA,viB,viC,viD,viE] = vil
    voA=[]
    voB=[]
    voC=[]
    voD=[]
    voE=[]    
    ((pgA, giA, viA, voA),
    (pgB, giB, viB, voB),
    (pgC, giC, viC, voC),
    (pgD, giD, viD, voD),
    (pgE, giE, viE, voE)) = (
    ron(pgA, giA, viA, voA, gem),
    ron(pgB, giB, viB, voB, gem),
    ron(pgC, giC, viC, voC, gem),
    ron(pgD, giD, viD, voD, gem),
    ron(pgE, giE, viE, voE, gem))    
    viA = [0]
    while pgE[giE] != 99:
        while voA == [] and pgA[giA] != 99:
            (pgA, giA, viA, voA) = ron(pgA, giA, viA, voA, gem)
        if voA:
            viB = [voA[-1]]
            voA = []
        while voB == [] and pgB[giB] != 99:
            (pgB, giB, viB, voB) = ron(pgB, giB, viB, voB, gem)
        if voB:
            viC = [voB[-1]]
            voB = [] 
        while voC == [] and pgC[giC] != 99:
            (pgC, giC, viC, voC) = ron(pgC, giC, viC, voC, gem)
        if voC:
            viD = [voC[-1]]
            voC = [] 
        while voD == [] and pgD[giD] != 99:
            (pgD, giD, viD, voD) = ron(pgD, giD, viD, voD, gem)
        if voD:
            viE = [voD[-1]]
            voD = []
        while voE == [] and pgE[giE] != 99:
            (pgE, giE, viE, voE) = ron(pgE, giE, viE, voE, gem)
        if voE:
            viA = [voE[-1]]
            output = voE[-1]
            voE = []
    return output

with open('y2019day07v1.txt', 'r') as file:
    t = [x.strip() for x in file.readlines()]

pers = [[[0]],[],[],[],[],[]] # all permutations of 1 element
for i11 in range(4):
    e = max([max(pe) for pe in pers[i11]])+1
    for pe in pers[i11]:
        for j in range(len(pe)+1):
            pers[i11+1].append(pe[:j]+[e]+pe[j:])
[len(perl) for perl in pers]

for u in t:
    pg = [int(x) for x in u.split(",")]
    print("part1", max([chainrun(pg,perm,[0],0)[0] for perm in pers[4]])) #the final bit prints to debug.

pers = [[[5]],[],[],[],[],[]] # all permutations of 1 element
for i11 in range(4):
    e = max([max(pe) for pe in pers[i11]])+1
    for pe in pers[i11]:
        for j in range(len(pe)+1):
            pers[i11+1].append(pe[:j]+[e]+pe[j:])
[len(perl) for perl in pers]

for u in t:
    pgm = [int(x) for x in u.split(",")]
    print("part2", max([runsignal(pgm,[[i12] for i12 in perm],[],0) for perm in pers[4]]))

excruciating_test_case= '''
perm = [9,8,7,6,5]
vil = [[i12] for i12 in perm]
gem = 1
u=t[0]
pgm = [int(x) for x in u.split(",")]
runsignal(pgm,vil,[],0)

"runparallel" is an idea of what "run in parallel" might mean.
But this requires that [0] be given as input to *each* amplifier on the third command.
On the other hand, the instructions say:
"All signals sent or received in this process will be between pairs of amplifiers except the very first signal and the very last signal. To start the process, a 0 signal is sent to amplifier A's input exactly once."

Runsignal hypothesis: The first input to B, after the phase, should be the first output from A, not zero.
Rather than run them in parallel, we should start and stop them, running A on 0 until it produces an output, then running B on that that value until it produces an output, &c.
'''
