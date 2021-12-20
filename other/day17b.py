
import re
import math
s = open("input/day13.txt").readline()
m = re.search(r'target area: x=(\d+)..(\d+), y=(-?\d+)..(-?\d+)', s)
x0,x1,y1,y0 = [int(m.group(i)) for i in range(1,5)]
vxmin = int(math.sqrt(x0*2))
vxmax = x1
mm = 0
hh = 0

def shoot(vx, vy):
    track = [(0,0)]
    x = y = m = 0
    while True:
        x += vx
        y += vy
        track.append((x,y))
        m = max(y,m)
        if x >= x0 and x <= x1 and y >= y1 and y <= y0:
            return track
        vy -= 1
        vx = max(0, vx-1)
        if (vx == 0 and x < x0) or x > x1 or y < y1: 
            return track

for vx in range(vxmin, vxmax + 1):
    td = vx * (vx + 1) // 2
    if td >= x0 and td <= x1:
        xsmin = vx - int(math.sqrt((td-x0)*2))
        vymin = y1//xsmin + (xsmin-1)//2
        vymax = -y1
    elif td > x1:
        tx = 0
        tvx = vx
        while tx < x0:
            tx += tvx
            tvx -= 1
        xsmin = vx - tvx
        while tx < x1 + 1:
            tx += tvx
            tvx -= 1
        xsmax = vx - tvx 
        vymin = y1//xsmin + (xsmin-1)//2
        vymax = y0//xsmax + (xsmax+1)//2
    else:
        vymin = 0
        vymax = -1
    for vy in range(vymin, vymax + 1):
        track = shoot(vx,vy)
        (x,y) = track[-1]
        if x >= x0 and x <= x1 and y >= y1 and y <= y0:
            hh += 1
            mm = max(mm,max([y for (x,y) in track]))

print(mm)
print(hh)

    