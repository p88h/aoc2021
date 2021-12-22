import time
import re
import itertools

def crop(seq, limits):
    crop = seq.copy()
    for l in range(len(crop)):
        (s0,s1) = limits[l]
        (c0,c1) = crop[l]
        c0 = max(c0,s0)
        c1 = min(c1,s1)
        crop[l]=(c0,c1) if c0<c1 else (0,0)
    return crop

def empty(seq):
    return seq[0] == (0,0) or seq[1] == (0,0) or seq[2] == (0,0)

class SuperCube:
    def __init__(self, bounds, value):
        self.bounds = bounds
        self.reset(value)
    
    def reset(self, value):
        self.value = value
        self.children = None

    def explode(self):
        if self.children:
            return
        self.children = []
        [(sx0, sx1), (sy0, sy1), (sz0, sz1)] = self.bounds
        (cw, ch, cd) = ((sx1-sx0)//2, (sy1-sy0)//2, (sz1-sz0)//2)
        for (xd,yd,zd) in itertools.product([0,cw],[0,ch],[0,cd]):
            cbounds = [(sx0+xd,sx0+xd+cw), (sy0+yd,sy0+yd+ch), (sz0+zd,sz0+zd+cd)]
            self.children.append(SuperCube(cbounds, self.value))
        self.value = None
    
    def update(self, box, value):
        if box == self.bounds:
            self.reset(value)
        else:
            self.explode()
            for child in self.children:
                subbox = crop(box, child.bounds)
                if not empty(subbox):
                    child.update(subbox, value)
    
    def volume(self):
        if self.children:
            return sum(child.volume() for child in self.children)
        tot = self.value
        for (a,b) in self.bounds:
            tot *= (b-a)
        return tot


def parse(lines):
    ret = []
    for line in lines:
        m = re.search(r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)', line)
        x0,x1,y0,y1,z0,z1 = [int(m.group(i)) for i in range(2,8)]
        bit = 1 if m.group(1) == "on" else 0
        ret.append(([(x0,x1+1),(y0,y1+1),(z0,z1+1)], bit))
    return ret

def solve(inputs, bounds = None):
    MAX=2**17
    cube = SuperCube([(-MAX,MAX),(-MAX,MAX),(-MAX,MAX)], 0)
    for (seq, on) in inputs:
        if bounds:
            seq = crop(seq,bounds)
        if empty(seq):
            continue
        cube.update(seq, on)
    return cube.volume()

dims = parse(open("input/day22.txt").read().splitlines())

start = time.time()
vol1 = solve(dims, [(-50,51),(-50,51),(-50,51)])
end = time.time()
print(vol1, end-start)
start = time.time()
vol2 = solve(dims)
end = time.time()
print(vol2, end-start)
