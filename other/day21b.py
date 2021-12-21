from collections import defaultdict
import time

lines = open("input/day21.txt").readlines()
p1 = int(lines[0].split(": ")[1])
p2 = int(lines[1].split(": ")[1])


def run1(p1, p2):
    s1 = s2 = ofs = cnt = 0
    while True:
        p1 = (p1+(ofs % 100)+((ofs+1) % 100)+((ofs+2) % 100)+2) % 10+1
        ofs = (ofs+3) % 100
        cnt = cnt + 3
        s1 = s1 + p1
        if s1 >= 1000:
            return s2*cnt
        (p1, p2, s1, s2) = (p2, p1, s2, s1)


def produce3(multiverse, p, s, c, w):
    for (d, f) in [(6, 7), (5, 6), (7, 6), (4, 3), (8, 3), (3, 1), (9, 1)]:
        np = ((p + d - 1) % 10) + 1
        ns = s + np
        if ns < 21:
            multiverse[(np, ns)] += c*f
        else:
            w[-1] += c*f


def run2(p):
    multiverse = defaultdict(int)
    multiverse[(p, 0)] = 1
    wins = []
    while multiverse:
        wins.append(0)
        temp = defaultdict(int)
        for (p, s) in multiverse:
            produce3(temp, p, s, multiverse[(p, s)], wins)
        multiverse = temp        
    return wins

def run3(p1,p2):
    wins1 = run2(p1)
    wins2 = run2(p2)
    size1 = size2 = 1
    w1 = w2 = 0
    for step in range(len(wins1)):
        size1 = size1 * 27 - wins1[step]
        w1 += wins1[step]*size2
        size2 = size2 * 27 - wins2[step]
        w2 += wins2[step]*size1
    return max(w1,w2)


start = time.time()
ret1 = run1(p1, p2)
end = time.time()
print(ret1, end-start)
start = time.time()
ret2 = run3(p1, p2)
end = time.time()
print(ret2, end-start)
