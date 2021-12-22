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
    
    def subtract(self, seq):
        cropped = crop(seq, self.limits)
        if empty(cropped):
            return
        box = Box(cropped)
        for inner in self.boxes:
            inner.subtract(cropped)
        self.boxes.append(box)
    
    def volume(self):
        tot = 1
        for (a,b) in self.limits:
            tot *= (b-a)
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
