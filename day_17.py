
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

with open('y2019day17v1.txt', 'r') as file:
    t = [x.strip() for x in file.readlines()]
for u in t:
    pj = [int(x) for x in u.split(",")]
    pg = {i:pj[i] for i in range(len(pj))}
    vo = run(pg,[],[],0)

ou = ''.join([chr(il) for il in vo])
print(ou)
pt1 = 0
ow = [x for x in ou.split('\n') if len(x) > 10]
mat = [list(x) for x in ow]
for x in range(1,len(mat)-1):
    for y in range(1,len(mat[0])-1):
        if [mat[a][b] for (a,b) in [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]] == ['#']*4:
            mat[x][y] = 'o' 
            pt1 += x*y
[print(''.join(row)) for row in mat]
print('pt1',pt1)
len(mat[0])
[print(ou[i:i+45]) for i in range(0,len(ou),46)]
# The 46th is the carriage return.
mat = [list(x) for x in ow]
#mat[y][x] = '<'
[print(''.join(row)) for row in mat]


def mou(x,y,dir):
    return [(x+1,y),(x,y-1),(x-1,y),(x,y+1)][dir]#[{'>':'0','^':1,'<':2,'v':3}]

scaffold = '''
We seek three patterns, maximal w.t.r. a given score: 
leo('L') = leo('R') = 1;
leo('L,') = leo('R,') = 2;
leo('6') = 1
leo('12') = 2 ?? 
leo('6,') = 2
visually, we detect that the loops pointing N,W, and S are the same, only rotated.
We seek maximal patterns A,B,C, such that leo(A) <= 20.
In a sense, this is 2d pattern matching. 
compress_me prefers a right turn over "go straight". 

......## L8L ##..............................
......#.......#..............................
......#.......#.......................# L6 #^
......#.......#...................... L .....
......#.......#...................... 4 .....
......#.......#...................... R .....
......#####...#...........## 12 #######......
..........#...#.......... L .................
......###########........ 6 .................
......#...#...#.#........ R .................
......#...#...#.#.........#..................
......#...#...#.#.........#..................
......#...#...#### 12R12 ##..................
......#...#.....#............................
......#######...#............................
..........#.#...#............................
..........#.#...#............................
..........#.#...#............................
..........#######............................
............#................................
............#................................
............#................................
............#...........#######..............
............#...........#.....#..............
........###########.....#.....#..............
........#...#.....#.....#.....#..............
#############.....#.....#.....#...#..........
#.......#.........#.....#.....#...#..........
#.......#.....#############...#...#..........
#.......#.....#...#.....#.#...#...#..........
#.....#############.....#.#...#...#..........
#.....#.#.....#.........#.#...#...#..........
#.....#.#.....#.........###########..........
#.....#.#.....#...........#...#..............
#######.#######...........#...#####..........
..........................#.......#..........
..........................#.......#..........
..........................#.......#..........
..........................#.......#..........
..........................#.......#..........
..........................#########..........
'''

def keepon(x,y,dir):
    a,b = mou(x,y,dir)
    if b in range(len(mat)):
        if a in range(len(mat[b])):
            if mat[b][a] == '#':
                return 1
    return 0

def turnLR(x,y,d0):
    for i in [-1,1]:
        dir = (d0+i)%4
        a,b = mou(x,y,dir)
        if b in range(len(mat)):
            if a in range(len(mat[b])):
                if mat[b][a] == '#':
                    return dir,{1:'L',-1:'R'}[i]
    return 5,'err'

def drawscaff(x,y,dir):
    cuu = []
    while dir < 5:
        nu = 0
        while keepon(x,y,dir):
            nu += 1
            x,y = mou(x,y,dir)
        if nu > 0:
            cuu.append(str(nu))
        dir,tur = turnLR(x,y,dir)
        if tur != 'err':
            cuu.append(tur)
    return ','.join(cuu)

x,y = ou.index('^')%46, ou.index('^')//46
cuu = drawscaff(x,y,1)

def vacuumcode1(est):
    pg = {i:pj[i] for i in range(len(pj))}
    pg[0] = 2
    vo = run(pg, [ord(c) for c in est],[],0)
    print(''.join([chr(il) for il in vo]))

vacuumcode1('\n')
vacuumcode1('A\n'+cuu[0:18]+'\nb\nc\nd\ne\nf\ng\nh\n'[::-1])
vacuumcode1('A,B,C\n'+cuu[0:18]+'\n'+cuu[19:38]+'\n'+cuu[39:57]+'\ny\n'[::-1])
 # vi = values input; vo = values outout

vacuumcode1_out = '''
ugg. I forgot that I read inputs *backwards*!! 
vi == [65, 44, 66, 44, 67, 10] becomes vi == [65, 44, 66, 44, 67]
'A,B,C\n'+cuu[0:18]+'\n'+cuu[19:38]+'\n'+cuu[39:57]+'\nn' : Expected function name but got: n
'A,B,C\n'+cuu[0:18]+'\n'+cuu[19:38]+'\n'+cuu[39:57]+'\nA' : HCF-3 291 [] 3 [0] [574] [65]
'A' : HCF-3 128 [] 3 [0] [574] [-1]
'A\nw' : Expected function name but got: w
'A\nwoo' : Expected function name but got: o
'A,A,A\n'+cuu[0:18]+'\nx' : Expected function name but got: x
'A+\n'+(cuu[0:18]+'\n')*3+'y' : Expected function name but got: y
'A\n'+cuu[0:18]+'\nb\nc\nd\ne\nf\ng\nh\ni'

The robot reads everything, prints "Main", waits for more! 

This seems to feed code in.

The final bit of code has to be a 'function'. E.g.:
'L,6,L,10,L,10,L,6' occurs 3x.
'12,L,6,L,10,L,10,L,6' has length 20 and won't fit in the buffer.
cuu.index('L,6,L,10,L,10,L,6') == 44
So the initial 44 steps have to be 3 chunks, not 2.
'''

cuus = ''.join(str(x) for x in cuu)

A,B,C = ('L,6,L,4,R,12', 'L,6,R,12,R,12,L,8', 'L,6,L,10,L,10,L,6')
def vacuumcode():
    est = 'A+B+A+C+B+A+C+B+A+C'.replace('+',','
        )+'\n'+A+'\n'+B+'\n'+C+'\nn\n'
    pg = {i:pj[i] for i in range(len(pj))}
    pg[0] = 2
#    vo = run(pg, [ord(c) for c in est],[],0)  
    gi, reb, gem = 0,0,0 # global index
    vi,vo = [],[]
    while '\n' in est:
        niu = est.index('\n')
        while pg[gi]%10 != 3:
            (pg, gi, vi, vo, reb) = ron(pg, gi, vi, vo, reb, gem)
        print(''.join([chr(il) for il in vo]))
        vi,vo = [ord(c) for c in est[:niu+1][::-1]],[]
        est = est[niu+1:]
        print(vi)
        while pg[gi]%10 != 4:
            (pg, gi, vi, vo, reb) = ron(pg, gi, vi, vo, reb, gem)
#    while pg[gi]%100 not in (3,99):
    while pg[gi]%100 != 99: #len(vo) < 1887:
        (pg, gi, vi, vo, reb) = ron(pg, gi, vi, vo, reb, gem)
        if len(vo)%1887 == 0 and len(vo) > 1:
            print(''.join([chr(il) for il in vo]))
    print("part 2",vo[-1])
#    for i in range(40):
#        (pg, gi, vi, vo, reb) = ron(pg, gi, vi, vo, reb, 1)
# vacuumbot turns left, and he walks the entire programmed route. 

vacuumcode()

'''We can spin in place; LR== nothing, LLLL = nothing, LLL=R'''
'''We can certainly split a number into two numbers, e.g., 10 = 6+4.'''
'''We can run backwards and then retrace some of our steps.'''
'''In order for the vacuum robot to visit every part of the scaffold at least once, one path it could take is:'''
'''We must seek any path that is composed of appropriate pieces, stays on the scaffold, and visits each part of the scaffold.'''
