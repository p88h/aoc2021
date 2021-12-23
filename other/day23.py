def display(s):
    print("#############")
    print("#"+s[0]+".".join(s[1:6])+s[6]+"#")
    for line in range(4):
        t = "###"
        for row in range(4):
            t += s[7+row*4+line] + "#"
        t += "##"
        print(t)        
    print("#############")

def genstate(s, a, b):
    ns = s.copy()
    (ns[a], ns[b]) = (ns[b], ns[a])
    return ns

Homes = {"A": 0, "B": 1, "C": 2, "D": 3}
Costs = {"A": 1, "B": 10, "C": 100, "D": 1000}

def move_home(s, cost):
    global Homes
    global Costs
    for hp in range(7):
        if s[hp] == '.':
            continue
        i = hp
        a = s[i]
        r = Homes[a]
        ofs = 7+r*4
        line = 3
        while line > 0 and s[ofs+line] == a:
            line -= 1
        if s[ofs+line] != '.':
            continue
        cb = (2+line)*Costs[a]
        # go right        
        while i < r + 1 and s[i+1] == '.':
            cb += Costs[a]*2 if i>0 else Costs[a]
            i+=1
        # go left
        while i > r + 2 and s[i-1] == '.':
            cb += Costs[a]*2 if i<7 else Costs[a]
            i-=1
        if i != r + 1 and i != r + 2:
            continue
        return move_home(genstate(s, ofs+line, hp), cost + cb)
    return (s,cost)

def move_out(s):
    global Homes
    global Costs
    # First move everybody in, if possible
    (s, cost) = move_home(s, 0)
    valid = []
    # Then try to get out, if possible
    for row in range(4):
        ofs = 7+row*4
        line = 0
        while line < 4 and s[ofs+line] == '.':
            line += 1
        if line == 4:
            continue
        a = s[ofs+line]        
        if row == Homes[a] and (line == 3 or all(s[i] == a for i in range(ofs+line+1,ofs+4))):
            continue
        rr = row + 2
        cb = cost + Costs[a]*line
        while rr < 8 and state[rr] == '.':
            cb += 2*Costs[a] if rr<7 else Costs[a]
            valid.append((genstate(s, ofs+line, rr), cb))
            rr += 1
        ll = row + 1
        cb = cost + Costs[a]*line
        while ll >= 0 and state[ll] == '.':
            cb += 2*Costs[a] if ll>0 else Costs[a]
            valid.append((genstate(s, ofs+line, ll), cb))            
            ll -= 1
    return valid

def search(start):
    queue = []
    for _ in range(100000):
        queue.append([])
    key = "".join(start)
    queue[0].append(key)
    mind = {key: 0}
    total = 1
    done = 0
    for cost in range(100000):
        tmp = set(queue[cost])
        print(cost, len(tmp), len(queue[cost]), total, done, done*100//total)
        for key in tmp:            
            if mind[key] < cost:
                continue
            state = list(key)
            valid = move_out(state)
            if all(state[i] == "." for i in range(7)) and len(valid) == 0:
                print(cost)
                display(state)
                return
            for (nstate,ncost) in valid:
                nkey = "".join(nstate)
                if nkey in mind and mind[nkey] <= cost+ncost:
                    continue
                mind[nkey]=cost+ncost
                queue[cost+ncost].append(nkey)
                total += 1
        done += len(queue[cost])

maze = open("input/day23.txt").read().splitlines()

state = []
state.append(maze[1][1])
for hp in range(1,6):
    state.append(maze[1][2*hp])
state.append(maze[1][11])
for row in range(4):
    for line in range(4):
        state.append(maze[line+2][3+row*2])

search(state)
