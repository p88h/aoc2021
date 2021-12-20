import itertools

class Board:
    def __init__(self, rules, lines):
        self.bitmap = [ 1 if c == '#' else 0 for c in rules ]
        self.size = len(lines)
        self.board = {}
        self.dflt = 0
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                self.board[(x, y)] = 1 if lines[y][x] == '#' else 0

    def iter(self, step):
        ndflt = self.bitmap[0] if self.dflt == 0 else self.bitmap[-1]
        total = 0
        old = self.board.copy()
        for (x, y) in itertools.product(range(-step,self.size+step), range(-step, self.size+step)):
            fval = 0
            for (dx,dy) in [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]:
                bit = old.get((x+dx,y+dy), self.dflt)
                fval = fval * 2 + bit
            nbit = self.bitmap[fval]
            total += nbit
            self.board[(x,y)]=nbit
        self.dflt = ndflt
        return total


lines = open("input/day20.txt").read().splitlines()
board = Board(lines[0], lines[2:])
for i in range(1,51):
    print(i, board.iter(i))
