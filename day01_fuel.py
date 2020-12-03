with open('day01.txt', 'r') as file:
    numbers = [int(x) for x in file.readlines()]

def fuel(mass:int):
    f = [mass]
    while f[-1] > 8:
        f.append(f[-1]//3-2)
    return f[1:]

print("part 1: ", sum([x//3-2 for x in numbers]))
print("part 2: ", sum([sum(fuel(x)) for x in numbers]))
