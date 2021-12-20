import itertools

# helper for day 19

def rot(v3, d):
    (d1, d2) = ((d+1)%3, (d+2)%3)
    tmp = list(v3)
    ret = []
    for _ in range(4):
        (tmp[d1], tmp[d2]) = (tmp[d2], -tmp[d1])
        ret.append(tuple(tmp))
    return ret

def rot2(lv3, d):
    return [ rv3 for v3 in lv3 for rv3 in rot(v3, d) ]

def rot3(lv3, ld):
    return [ rv3 for d in ld for rv3 in rot2(lv3, d) ]

once = [v3 for p in itertools.permutations([0,1,2]) for v3 in rot3([(1,2,3)],p)]
print(set([v3 for p in itertools.permutations([0,1,2]) for v3 in rot3(once,p)]))
