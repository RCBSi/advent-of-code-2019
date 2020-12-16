with open('day03.txt', 'r') as file:
    paths = [li.strip() for li in file.readlines()]

def point(base,direction,distance):
    (s,x,y) = base
    if direction == 'R':
        return (x+distance, y)
    if direction == 'D':
        return (x, y-distance)
    if direction == 'U':
        return (x, y+distance)
    if direction == 'L':
        return (x-distance, y)

def sortpoint(p):
    (x,y) = p
    return (abs(x)+abs(y), x,y)

def track(path):
    tr = [(0,0,0)]
    for x in path:
        tr = tr+[sortpoint(point(tr[-1],x[0],i+1)) for i in range(int(x[1:]))]
    return tr

def intersect(i,j):
    return [x for x in track(paths[i].split(',')) if x in track(paths[j].split(','))]

def manhattan(p):
    (x,y) = p
    return abs(x)+abs(y)

def first_intersection(a,b):
    a.sort()
    b.sort()
    (i, j) = (0,0)
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            i += 1
        if a[i] > b[j]:
            j += 1
        if a[i] == b[j]:
            return a[i]


t0 = track(paths[0].split(','))[1:]
t1 = track(paths[1].split(','))[1:]
print(first_intersection(t0,t1))

breakpoint()
print(track(paths[0].split(',')))

print(track(paths[0]))

print(paths[2])
print(min([manhattan(p) for p in intersect(3,4) if p != (0,0)]))
print(paths[5])
print(min([manhattan(p) for p in intersect(6,7) if p != (0,0)]))
print(paths[8])
