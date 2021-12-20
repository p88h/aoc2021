points = []
(sx, sy) = (0, 0)
for l in open("input/day13.txt").read().splitlines():
    if ',' in l:
        points.append(tuple(map(int, l.split(","))))
    if 'x=' in l:
        sx = int(l.split('=')[1])
    if 'y=' in l:
        sy = int(l.split('=')[1])
d = {}
print(sx, sy)
for p in points:
    (x, y) = p
    dx = x // (sx + 1)
    dy = y // (sy + 1)
    x = sx - ((x - dx) % sx) - 1 if dx % 2 == 1 else (x-dx) % (sx)
    y = sy - ((y - dy) % sy) - 1 if dy % 2 == 1 else (y-dy) % (sy)
    d[(x, y)] = True
for i in range(sy):
    print("".join(["#" if (j, i) in d else " " for j in range(sx)]))
