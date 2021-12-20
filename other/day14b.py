import numpy

def regular_power(m, n, mod):
    e = m
    n -= 1
    while n > 0:
        if n % 2 == 1:
            m = m * e % mod
        e = e * e % mod
        n //= 2
    return m

def matrix_power(m, n, mod):
    e = m
    n -= 1
    while n > 0:
        if n % 2 == 1:
            m = numpy.dot(m, e) % mod
        e = numpy.dot(e, e) % mod
        n //= 2
    return m

def primes(lim):
    era = [ 1 ] * lim
    pri = []
    for p in range(2,lim):
        if era[p] == 1:
            for j in range(p,lim,p):
                era[j] = 0
            pri.append(p)
    return pri    

lines = open("input/day14.txt").read().splitlines()
rules = dict([l.split(' -> ') for l in lines[2:]])
ridx = dict(zip(rules, range(len(rules))))
mat = numpy.zeros((len(rules), len(rules)), dtype=object)
for p in rules:
    mat[ridx[p[0] + rules[p]]][ridx[p]] = 1
    mat[ridx[rules[p] + p[1]]][ridx[p]] = 1
I = numpy.identity(len(rules), dtype=object)
M = 100000007 
tmp = list(zip(lines[0], lines[0][1:]))
v = [ tmp.count((p[0],p[1])) for p in rules ]
u = numpy.dot(mat, v) % M
for i in range(2, 100):
    PM = M ** i - 1 # (M ** i) - 1
    t = matrix_power(mat, PM, M)
    w = numpy.dot(t, u) % M 
    if numpy.equal(w, u).all():
        print("initial cycle found: {}**{}-1".format(M, i))
        # factorize a bit
        for p in primes(1000000):
            while PM % p == 0 and numpy.equal(numpy.dot(matrix_power(mat, PM // p, M), u) % M, u).all():
                PM = PM // p                
        break
print("minimized cycle and factor:", PM, '*', ((M ** i) - 1) // PM)
start = 12357
goog = regular_power(10, 10**100, PM)

for pow in [ 10, 40, 173, 500, goog, goog+PM ]:
    if pow > 1000:
        w = numpy.dot(matrix_power(mat,pow, M), v) % M
    else:
        w = numpy.dot(numpy.linalg.matrix_power(mat, pow), v)
    cnt = {lines[0][0]: 1}
    for p in ridx:
        cnt[p[1]] = cnt.get(p[1],0) + w[ridx[p]]
    # print(w)
    # print(cnt)
    lmin = min(cnt, key=lambda k: cnt[k])
    lmax = max(cnt, key=lambda k: cnt[k])
    lsum = sum(cnt[k] for k in cnt)
    print(cnt[lmax]-cnt[lmin], lsum % M)