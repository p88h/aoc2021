import numpy as np

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
            m = np.dot(m, e) % mod
        e = np.dot(e, e) % mod
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

t = np.array([[0,1,0,0,0,0,0,0,0],
              [0,0,1,0,0,0,0,0,0],
              [0,0,0,1,0,0,0,0,0],
              [0,0,0,0,1,0,0,0,0],
              [0,0,0,0,0,1,0,0,0],
              [0,0,0,0,0,0,1,0,0],
              [1,0,0,0,0,0,0,1,0],
              [0,0,0,0,0,0,0,0,1],
              [1,0,0,0,0,0,0,0,0]], dtype=object)

v = np.bincount(list(map(int, input().split(","))), minlength=9)

e = t
# find the cycle
M = 100000007

for i in range(1, 100):
    PM = (M ** i) - 1   
    if np.equal(matrix_power(t, PM, M), np.identity(9)).all():
        print("initial cycle found: {}**{}-1".format(M, i))
        # factorize a bit
        for p in primes(1000000):
            while PM % p == 0 and matrix_power(t, PM // p, M).all() == np.identity(9).all():
                PM = PM // p                
        break

print("minimized cycle and factor:", PM, '*', ((M ** i) - 1) // PM)
pp = regular_power(10, 10 ** 100, PM)
print("reduced googolplex power:", pp)
mt = matrix_power(t, pp, M)
r = np.dot(mt, v) % M
print("final population mod M:", r.sum() % M)

