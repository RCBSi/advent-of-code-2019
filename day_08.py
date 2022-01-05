with open('y2019day08v1.txt', 'r') as file:
    tei = [int(zi) for zi in file.readlines()[0]]

imp = 25*6
teu = [tei[imp*cue:imp*(cue+1)] for cue in range(len(tei)//imp)]

mio = imp
for tes in teu:
    if tes.count(0) < mio:
        out = (tes.count(2) , tes.count(1), tes.count(0))
        mio = tes.count(0)
print("p1",out, out[0]*out[1])

# 1908 is too low.

fin = [2 for ian in range(len(teu[0]))]
for ide in range(len(tei)):
    if tei[ide] < 2 and fin[ide%imp] == 2:
        fin[ide%imp] = {1:'#',0:'.'}[tei[ide]]

print("pt2")
[print(''.join(fin[cut:cut+25])) for cut in range(0,imp,25)]

