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
    t = [[int(z)] for x in file.readlines()[0] for z in x.strip()] # a column vector.

part2_comment='''mat = fftmat(len(t)*10000) is prohibitive.
We can't construct the upper-triangular matrix fftmat(650*10000).
Even fftmat(10000) is too slow to construct.'''
