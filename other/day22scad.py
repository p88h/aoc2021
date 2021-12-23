import time
import re

def parse(lines):
    ret = []
    for line in lines:
        m = re.search(r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)', line)
        x0,x1,y0,y1,z0,z1 = [((int(m.group(i))+100000)//200)/10 for i in range(2,8)]
        bit = 1 if m.group(1) == "on" else 0
        ret.append(([(x0,x1+1),(y0,y1+1),(z0,z1+1)], bit))
    return ret

arrs = [[],[]]
for item in parse(open("input/day22.txt").read().splitlines()):
    ([(x0,x1),(y0,y1),(z0,z1)], bit) = item
    dx = int((x1-x0)*10)/10
    dy = int((y1-y0)*10)/10
    dz = int((z1-z0)*10)/10
    arrs[bit].append("        translate([{},{},{}]) cube([{},{},{}]);".format(x0,y0,z0,dx,dy,dz))

print("difference() {\n    union() {")
print("\n".join(arrs[1]))
print("    }\n    union() {")
print("\n".join(arrs[0]))
print("    }\n}")
