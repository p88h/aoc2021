import time
import copy

class Board:
    def __init__(self, rules, lines):
        self.bitmap = [ 1 if c == '#' else 0 for c in rules ]
        self.size = len(lines)
        self.ofs = 52
        self.dflt = 0
        self.board = []
        for y in range(self.ofs):
            self.board.append([0] * (self.size + self.ofs*2))
        for y in range(len(lines)):
            self.board.append([])
            self.board[self.ofs+y].extend([0] * self.ofs)
            for x in range(len(lines[y])):
                self.board[self.ofs+y].append(1 if lines[y][x] == '#' else 0)
            self.board[self.ofs+y].extend([0] * self.ofs)
        for y in range(self.ofs):
            self.board.append([0] * (self.size + self.ofs*2))
        self.old = copy.deepcopy(self.board)

    def iter(self, step):
        ndflt = self.bitmap[0] if self.dflt == 0 else self.bitmap[-1]
        total = 0
        (self.old, self.board) = (self.board, self.old)
        self.ofs -= 1
        self.size += 2
        for x in range(self.ofs-1,self.ofs+self.size+2):
            self.old[self.ofs-1][x]=self.old[self.ofs][x]=self.dflt
            self.old[self.ofs+self.size-1][x]=self.old[self.ofs+self.size][x]=self.dflt
        for y in range(self.ofs-1,self.ofs+self.size+2):
            self.old[y][self.ofs-1]=self.old[y][self.ofs]=self.dflt
            self.old[y][self.ofs+self.size-1]=self.old[y][self.ofs+self.size]=self.dflt
        for x in range(self.ofs,self.ofs+self.size):
            pval = 0 if self.dflt == 0 else 63
            for y in range(self.ofs,self.ofs+self.size):
                fval = (pval & 63)*8 + self.old[y+1][x-1]*4+self.old[y+1][x]*2+self.old[y+1][x+1]
                pval = fval
                nbit = self.bitmap[fval]
                total += nbit
                self.board[y][x]=nbit
        self.dflt = ndflt
        return total

start = time.time()
lines = open("input/day20.txt").read().splitlines()
board = Board(lines[0], lines[2:])
for i in range(1,51):
    t = board.iter(i)
    end = time.time()
    print(i, t, end - start)
