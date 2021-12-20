import time
start = time.time()
board = []
for l in open("input/day15.txt").read().splitlines():
    board.append([int(l[x]) for x in range(len(l))])
distance = [[0] * 500 for _t in range(500)]
queue = [[(0, 0)]] + [[] for _t in range(10000)]
v = 0
while distance[499][499] == 0:
    for (y, x) in queue[v]:
        if v > distance[y][x]:
            continue
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if y+dy >= 0 and y+dy < 500 and x+dx >= 0 and x+dx < 500:
                dt = ((board[(y+dy) % 100][(x+dx) % 100] +
                      (y+dy)//100 + (x+dx)//100 - 1) % 9)+1
                if distance[y+dy][x+dx] == 0:
                    distance[y+dy][x+dx] = v + dt
                    queue[v+dt].append((y+dy, x+dx))
    v += 1
print(distance[499][499])
end = time.time()
print(end - start)