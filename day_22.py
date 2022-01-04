with open('y2019day22v1.txt', 'r') as file:
    tei = file.readlines()

def shu(ste,lie):
    if 'deal into new stack' in lie:
        ste.reverse()
        return ste
    if 'cut' in lie:
        N = int(lie.strip()[4:])
        return (ste*3)[pri+N:2*pri+N]
    if 'deal with increment' in lie:
        N = int(lie.strip()[20:])
        pla = {(iel*N)%pri:iel for iel in range(pri)}
        return [ste[pla[iel]] for iel in range(pri)]

pri = 10007

ste = [zi for zi in range(pri)]
for lie in tei:
    ste = shu(ste,lie)
print("p1",ste.index(2019))
print(ste[1000:1005],"p1")

nin = [int(lie.strip()[20:]) for lie in tei if 'increment' in lie]
nin.sort()
import numpy
nin = list(numpy.unique(nin))
nin

def imu(pri, nin): #invert the multiplication ring.
    inv = {}
    for pli in nin:
        qui = pri//pli
        while (pli*qui)%pri != 1:
            qui+= 1
        inv[pli] = qui
    return inv

def ver(pri, lok, lie): #reverse lie: for which location i < pri does lie send i to lok?
    if 'deal into new stack' in lie:
        return pri-lok-1
    if 'cut' in lie:
        N = int(lie.strip()[4:])
        return (lok+N)%pri
    if 'deal with increment' in lie:
        N = int(lie.strip()[20:])
        return (inv[N]*lok)%pri 

def tra(pri, lok, tei):
    for lie in tei:
#        print(lok, ver(pri, lok, lie))
        lok = ver(pri, lok, lie)
    return lok

inv = imu(pri, nin)
tei.reverse()
print([tra(pri,lok,tei) for lok in range(pri)][1000:1005], "pre pt2")
pri = 119315717514047


def i_to_b(x,b): # the base-be representation of x
    out = []
    while x >= b:
        out.append(x % b)
        x = x//b
    out.append(x)
#    out.reverse()
    return out

prib = i_to_b(pri-2,2)

comment1='''What, I should use efficient multiplication.
def mumo(xi,qi,pri):
    prod = 0
    for i in range(xi):
        prod = (prod+qi)%pri        
'''

#the binary representation of pri-2 would speed the inversion.
# inv {9: 53029207784021, 15: 55680668173222}
def imupr(pri, nin): #invert the multiplication ring given a prime.
    inv = {}
    for pli in nin:
        plinv = 1
        qui = pli
        for squs in range(len(prib)):
#            print(plinv,qui)
            if prib[squs]:
                plinv = (plinv*qui)%pri
            if squs < len(prib)-1:
                qui = (qui*qui)%pri
        if (pli*plinv)%pri == 1:
            inv[pli] = plinv
        else:
            print(pli,plinv, "Error finding inverse of pli")
    return inv

inv = imupr(pri,[9,15,17,19,20,21,22,23,27,28,30,32,36,
    39, 40, 43, 46, 48, 50, 51, 52, 53, 57, 61, 62, 63, 66, 68,
    71, 73, 74, 75])

inv = {9: 53029207784021,
 15: 55680668173222,
 17: 98260002658627,
 19: 12559549212005,
 20: 101418359886940,
 21: 22726803336009,
 22: 5423441705184,
 23: 57064038811066,
 27: 97220214270705,
 28: 106531890637542,
 30: 27840334086611,
 32: 3728616172314,
 36: 43086231324517,
 39: 58128170070946,
 40: 50709179943470,
 43: 63820034949374,
 46: 28532019405533,
 48: 2485744114876,
 50: 40567343954776,
 51: 72525240057558,
 52: 103253986310233,
 53: 49527278968095,
 57: 83730328080033,
 61: 82151805501475,
 62: 86600117550518,
 63: 7575601112003,
 66: 1807813901728,
 68: 114051788800192,
 71: 105871693005422,
 73: 47399394628868,
 74: 17736120171007,
 75: 106588707645882}

#mulb

def repa(mul):
    slo = (tra(pri, 1, tei)- tra(pri, 0, tei))
    con = tra(pri, 0, tei)
    p2zero = (slo, con)
    p2ilk = p2zero
    mulb = i_to_b(mul,2)    
    lok = 2020
    for ilk in mulb: #[1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1]:
        if ilk:
            if 1==1:#(p2ilk[0]*lok + p2ilk[1])%pri == tra(pri, lok, tei):
                lok = (p2ilk[0]*lok + p2ilk[1])%pri
                #lok = tra(pri, lok, tei) 
                print(lok)
                #ok = (p2ilk[0]*lok + p2ilk[1])%pri
            else:
                print(ilk,"function p2ilk", p2ilk,"did not equal tra", lok)
        p2ilk = ((p2ilk[0]*p2ilk[0])%pri, (p2ilk[0]*p2ilk[1]+p2ilk[1])%pri) 
    return lok

mul = 101741582076661
print("p2",repa(mul))

lok = 2020
for ilk in range(20):
    if repa(ilk) == lok:
        print(ilk)
    lok = tra(pri, lok, tei)

comments ='''
Check:
* for m << mul that repa(m) == tra^m.
* for p << pri that tra is the inverse of shu.
* that mul is fairly represented in binary form.

sum([mulb[i] * 2**i for i in range(len(mulb))]) == mul
repa(1) == tra(pri,2020,tei) -- true.
repa(2) == tra(pri,tra(pri,2020,tei),tei) -- true.
repa(3) == tra(pri,tra(pri,tra(pri,2020,tei),tei),tei)
repa(4) == tra(pri,tra(pri,tra(pri,tra(pri,2020,tei),tei),tei),tei)

(slo*(slo*2020+con)+con)%pri == tra(pri,tra(pri,2020,tei),tei)
(slo*(slo*2020+con)+con)%pri == ((slo*slo)%pri*2020 + (slo*con+con)%pri)%pri
        b(ba+c)+c = bba+bc+c.

Compute the powers p^(2^k) p and apply those functions to a
which appear in the base2 representation of mul.

Given p, p^2(a) = b(b*a + c)+c = b^2 * a + bc+c.

hypothesis: 
slo = (tra(pri, 1, tei)- tra(pri, 0, tei))
con = tra(pri, 0, tei)
for all x < pri:
tra(pri, x, tei) == (slo*x + con)%pri

tra(pri,2,tei) == (slo*2+con)%pri True.

We can't iterate mul times. 

lok = 2020
mul = 101741582076661
for ilk in range(mul):
    lok = tra(pri, lok, tei)

a => pri - a -1 
    => * qui 
    => +N ... 
so a goes to a linear function p(a) = b*a + c, and we 
wish to evaluate p^k (a) for a very high k.
can we compute p^2, p^4 &c? 

Track one element through all the shuffles.
ste = [zi for zi in range(pri)]
for idu in range(mul):
    if idu%119315 == 0:
        print('.')
    for lie in tei:
        ste = shu(ste,lie)
print("p2",ste[2019])
'''
