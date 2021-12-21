import re
from collections import defaultdict
import itertools
import time

lines = open("input/day21.txt").readlines()
p1 = int(re.search(r'Player (\d+) starting position: (\d+)', lines[0]).group(2))
p2 = int(re.search(r'Player (\d+) starting position: (\d+)', lines[1]).group(2))

def run1(p1, p2):
    s1 = s2 = ofs = cnt = 0
    while True:
        p1 = (p1+(ofs%100)+((ofs+1)%100)+((ofs+2)%100)+2)%10+1
        ofs = (ofs+3)%100
        cnt = cnt + 3
        s1 = s1 + p1
        if s1 >= 1000:
            return s2*cnt
        (p1, p2, s1, s2) = (p2, p1, s2, s1)


def produce3(multiverse, p1, p2, s1, s2, c, w, p):
    for (d1,d2,d3) in itertools.product(range(3),range(3),range(3)):
        np = ((p1 + d1 + d2 + d3 + 2)%10) + 1
        ns = s1 + np
        if ns < 21:
            multiverse[(p2,np,s2,ns)] += c
        else:
            w[p] += c

def run2(p1, p2):
    multiverse = defaultdict(int)
    multiverse[(p1,p2,0,0)]=1
    wins = [0, 0]
    player = 0
    while multiverse:
        temp = defaultdict(int)
        for (p1,p2,s1,s2) in multiverse:
            produce3(temp, p1,p2,s1,s2, multiverse[(p1,p2,s1,s2)], wins, player)
        player = 1-player
        multiverse = temp
    return max(wins)

start = time.time()
ret1 = run1(p1,p2)
end = time.time()
print(ret1, end-start)
start = time.time()
ret2=run2(p1,p2)
end = time.time()
print(ret2, end-start)
