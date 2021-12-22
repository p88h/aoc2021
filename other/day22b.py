import time
import re

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

class Box:
    def __init__(self, seq):
        self.limits = seq
        self.boxes = []
        self.empty = False
        self.cvolume = None
    
    def subtract(self, seq):
        self.cvolume = None
        cropped = crop(seq, self.limits)
        if cropped == self.limits:
            self.empty = True
        if empty(cropped) or self.empty:
            return
        box = Box(cropped)
        nboxes = []
        tvol = 0
        for inner in self.boxes:
            inner.subtract(cropped)
            ivol = inner.volume()
            if ivol > 0:
                nboxes.append(inner)
            tvol += ivol
        nboxes.append(box)
        self.cvolume = tvol + box.volume()
        self.boxes = nboxes
    
    def volume(self):
        if self.empty:
            return 0
        tot = 1
        for (a,b) in self.limits:
            tot *= (b-a)
        if self.cvolume:
            return tot - self.cvolume
        return tot - sum(box.volume() for box in self.boxes)

def parse(lines):
    ret = []
    for line in lines:
        m = re.search(r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)', line)
        x0,x1,y0,y1,z0,z1 = [int(m.group(i)) for i in range(2,8)]
        bit = m.group(1) == "on"
        ret.append(([(x0,x1+1),(y0,y1+1),(z0,z1+1)], bit))
    return ret

def solve(inputs, bounds = None):
    total = 0
    boxes = []
    for (seq, on) in inputs:
        if bounds:
            seq = crop(seq,bounds)
        if empty(seq):
            continue
        box = Box(seq)
        for another in boxes:
            another.subtract(seq)
        if on:
            boxes.append(box)
    return sum(box.volume() for box in boxes)


dims = parse(open("input/day22.txt").read().splitlines())

start = time.time()
vol1 = solve(dims, [(-50,51),(-50,51),(-50,51)])
end = time.time()
print(vol1, end-start)
start = time.time()
vol2 = solve(dims)
end = time.time()
print(vol2, end-start)
