with open('y2019day10v1.txt', 'r') as file:
    tei = file.readlines()
stars = []
aye = 0
while aye < len(tei):
    row = tei[aye]
    jee = 0
    while jee < len(row) and '#' in row[jee:]:
        jee = row.index('#',jee)
        stars.append((aye,jee))
        jee += 1
    aye += 1
len(stars)
vie = {tri:{} for tri in stars}
for sir in stars:
    for bet in stars:
        if bet != sir:
            (a,b) = sir
            (c,d) = bet
            p = c-a
            q = d-b
            if p == 0:
                q = q//abs(q)
            if q == 0:
                p = p//abs(p)
            for r in range(min(abs(p),abs(q)),0,-1):
                if p%r == 0 and q%r == 0:
                    p = p//r
                    q = q//r     
            if p<=0: # try to save the closest star.
                vie[sir][(p,q)] = (c,d)
            if p>0 and (p,q) not in vie[sir]:
                vie[sir][(p,q)] = (c,d)

print("p1",max([len(vie[tri]) for tri in vie]))

sir = [tri for tri in vie if len(vie[tri])==max([len(vie[tri]) for tri in vie])][0]
sum([q >= 0 for (p,q) in vie[sir]])
com = [[p/q,(p,q),vie[sir][(p,q)]] for (p,q) in vie[sir] if q < 0]
com.sort()
out = com[200-1-sum([q >= 0 for (p,q) in vie[sir]])][2]
print("p2",out[1]*100 + out[0])
