with open('y2019day16v1.txt', 'r') as file:
    t = [[int(z)] for x in file.readlines()[0] for z in x.strip()] # a column vector.

def dot(u,v):
    return sum([u[i]*v[i] for i in range(len(u))])

def col(x, j):
    return [x[i][j] for i in range(len(x))]

def mm(w,x): #matrix multiplicaiton.
    (n,m) = (range(len(w)), range(len(x[0])))
    return [[dot(w[i],col(x,j)) for j in m] for i in n]

def fftmat(nu):
    pa = [0, 1, 0, -1]
    ma = []
    for i in range(1,nu+1):
        st = []
        for e in pa:
            st = st+[e]*i
        ma.append((st*nu)[1:nu+1])
    return ma

def trunc(nu):
    if nu >= 0:
        return nu%10
    if nu < 0:
        return ((-1*nu)%10)

def one_phase(sig,nu):
    return [[trunc(z)] for y in mm(mat,sig) for z in y]

mat = fftmat(len(t))

for i43 in range(100):
    if i43%5 == 0:
        print(i43)
    t = one_phase(t,len(t))
print("pt1", ''.join([str(z) for y in t for z in y][:8]))

with open('y2019day16v1.txt', 'r') as file:
    li = file.readlines()[0]
    te = [int(z) for x in li for z in x.strip()] 

def fftd(tek,mul,ind,rii): # fft^rii of tek*mul at ind.
    han = (tek*mul)[ind:]
    for i23 in range(rii):
        i = len(han)
        su = 0
        tah = []
        while i > 0:
            i+= -1
            su = (su+han[i])%10
            tah.append(su)
        tah.reverse()
        han = tah
    return han[0:8]

oul = fftd(te,10**4,int(li[:7]),100)
print("pt2 ","".join([str(dig) for dig in oul]))

part2_comment='''fractals: 
s = [1]*50
for i in range(100):
    print(''.join([str(xiu) for xiu in s]))
    s = [sum(s[i:])%10 for i in range(len(s))]
11111111111111111111111111111111111111111111111111
09876543210987654321098765432109876543210987654321
55681506310013605186556815063100136051865568150631
05046500410009600546050465004100096005460504650041
55006055510000155506005515000655556000515500605551
05000449498888872722666165000049494888832722266161
55000062390246803142048215000006734024685364204871
05000004290084800762006865000000474008480526200681
55000000645557355582000460555555514000280053755591
05000000040505850502000060050505054000080005250501
55000000006611683388666660005500550666668888316611
05000000000487602968048260000500050048260246854821
55000000000068155348006860000055550006860084805131
05000000000004650528000460000005050000460002800541
55000000000000605508000060000000550000060000800051
05000000000000044944666660000000050000004444466661
00555555555555551784048260000000005555555173959371
00050505050505050924006860000000000505050547450181
00005500550055005564000460000000000055005506950091
00000500050005000504000060000000000005000500450001
00000055550000555500666660000000000000555500061111
00000005050000050500048260000000000000050500004321
00000000550000005500006860000000000000005500000631
00000000050000000500000460000000000000000500000041
00000000005555555500000060000000000000000055555551
22222222222727272722222226666666666666666661616161
08642086420819203142086420482604826048260482154871
'''

fft_comment = '''Is any property of FFT useful? 
The fact that the matrix is upper-triangular implies that: 
the value of fft^m(M)[i][j] (j>i) depends only on fft^n(M)[k][l] for k >i and l > i... and n < m.
A brute search then suffices, i.e.: for n < m, for k > i, compute fft^n[k][:]
'''
