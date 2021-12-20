import time
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
        self.board={}
        for x in range(-step,self.size+step):
            pval = 0
            for y in range(-step, self.size+step):
                fval = pval & 63
                for dx in [-1,0,1]:
                    bit = old.get((x+dx,y+1), self.dflt)
                    fval = fval * 2 + bit
                pval = fval
                nbit = self.bitmap[fval]
                total += nbit
                if nbit != ndflt:
                    self.board[(x,y)]=nbit
        self.dflt = ndflt
        return total

start = time.time()
lines = open("input/day20.txt").read().splitlines()
board = Board(lines[0], lines[2:])
for i in range(1,51):
    t = board.iter(i)
    end = time.time()
    print(i, t, end - start)
