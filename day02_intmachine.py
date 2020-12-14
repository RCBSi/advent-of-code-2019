from collections import defaultdict
with open('day02.txt', 'r') as file:
    codes = [li for li in file.readlines()]

def execute(comm, val0, val1):
    if comm == 1:
        return val0+val1
    if comm == 2:
        return val0*val1

for (noun,verb) in [(x,y) for x in range(99) for y in range(99)]:
    ch = defaultdict(set)
    c1 = codes[0].split(',')
    for i in range(len(c1)):
        ch[i].add((-2,int(c1[i])))

    ch[1].add((-1,noun))
    ch[2].add((-1,verb))

    for j in range(len(ch)):
        comm = max(ch[4*j])[1]
        if comm in (1,2):
            val0 = max(ch[max(ch[4*j+1])[1]])[1]
            val1 = max(ch[max(ch[4*j+2])[1]])[1]
            ch[max(ch[4*j+3])[1]].add((j,execute(comm, val0, val1)))
        else:
            if noun == 12 and verb == 2:
                print(4*j, max(ch[4*j])[1], "part 1: ", max(ch[0])[1])
            break
    if max(ch[0])[1] == 19690720:
        print("part 2: ", noun, verb, noun * 100 + verb)
        break

