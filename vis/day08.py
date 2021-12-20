import pygame
from common import View, Controller
from functools import reduce


def initmap():
    return dict([(x, 0b1111111) for x in "abcdefg"])


def single(bit):
    while bit != 0 and (bit & 1) == 0:
        bit //= 2
    return bit == 1


def allsingle(vals):
    return any(map(single, vals))


def allbits(vals):
    return reduce((lambda x, y: x | y), vals) == 0b1111111


def noempty(vals):
    return not any([x == 0 for x in vals])


def valid(vals):
    return allbits(vals) and noempty(vals)


class Descrambler:
    def __init__(self) -> None:
        self.pattern = {0: 0b1110111, 1: 0b0010100, 2: 0b0111011, 3: 0b0111110, 4: 0b1011100,
                        5: 0b1101110, 6: 0b1101111, 7: 0b0110100, 8: 0b1111111, 9: 0b1111110}
        self.classes = {2: [1], 3: [7], 4: [4], 5: [2, 3, 5], 6: [0, 6, 9], 7: [8]}

    def savestate(self, c, matrix):
        self.history.append((self.used.copy(), c, matrix.copy()))

    def resolve(self, matrix):
        cont = True
        done = {}
        while cont:
            cont = False
            for k in matrix:
                if k not in done and single(matrix[k]):
                    z = matrix[k] ^ 0b1111111
                    for j in matrix:
                        if j != k:
                            upd = matrix[j] & z
                            if matrix[j] != upd:
                                matrix[j] = upd
                                self.savestate(j, matrix)

                    cont = True
                    done[k] = True
                    break

    def updatemap(self, matrix, word, bits):
        for c in word:
            matrix[c] = matrix[c] & bits
            self.savestate(c, matrix)

    def descramble(self, words, matrix=None):
        if not matrix:
            self.history = []
            self.used = []
            self.solved = False
            matrix = initmap()
        if len(self.used) == len(words):
            if allsingle(matrix.values()):
                self.solved = True
            return
        ofs = len(self.used)
        h = words[ofs]
        for n in self.classes[len(h)]:
            if n in self.used:
                continue
            self.used.append(n)
            new_matrix = matrix.copy()
            self.updatemap(new_matrix, h, self.pattern[n])
            self.resolve(new_matrix)
            if valid(new_matrix.values()):
                self.descramble(words, new_matrix)
                if self.solved:
                    return
            self.used.pop()


class Segment:
    def __init__(self, idx):
        self.segmap = {0: [1, 0, 1, 1, 1, 1, 1], 1: [0, 0, 0, 0, 1, 0, 1],
                       2: [1, 1, 1, 0, 1, 1, 0], 3: [1, 1, 1, 0, 1, 0, 1],
                       4: [0, 1, 0, 1, 1, 0, 1], 5: [1, 1, 1, 1, 0, 0, 1],
                       6: [1, 1, 1, 1, 0, 1, 1], 7: [1, 0, 0, 0, 1, 0, 1],
                       8: [1, 1, 1, 1, 1, 1, 1], 9: [1, 1, 1, 1, 1, 0, 1]}
        self.pos = idx * 64

    def update(self, view, digit, word):
        segs = self.segmap[digit]
        si = 0
        for h in range(3):
            (x0, y0) = (self.pos + 44, 56+48*h)
            col = (160, 255, 160) if segs[si] == 1 else (60, 120, 60)
            pygame.draw.polygon(view.win, col,
                                [(x0+4, y0), (x0+36, y0), (x0+40, y0+4),
                                 (x0+36, y0+8), (x0+4, y0+8), (x0, y0+4)], 1-segs[si])
            si += 1
        for h in range(2):
            for v in range(2):
                (x0, y0) = (self.pos+36+48*v, 64+48*h)
                col = (160, 255, 160) if segs[si] == 1 else (60, 120, 60)
                pygame.draw.polygon(view.win, col,
                                    [(x0, y0+4), (x0, y0+36), (x0+4, y0+40), 
                                     (x0+8, y0+36), (x0+8, y0+4), (x0+4, y0)], 1-segs[si])
                si += 1
        (x0, y0) = (self.pos+36, 64+96+48)
        view.font.render_to(view.win, (x0, y0), word, (120, 240, 120))


class Solver:
    def __init__(self, words, codes, frames):
        self.words = words
        self.codes = codes
        self.frames = frames
        self.segments = dict([(x, Segment(x)) for x in range(10)])

    def update(self, view, controller):
        if view.frame >= len(self.frames):
            controller.animate = False
            return
        view.win.fill((0, 0, 0))
        # print(self.frames[view.frame])
        (digits, letter, matrix) = self.frames[view.frame]
        idx = len(digits) - 1
        self.pos = idx * 64
        for d in range(len(digits)):
            self.segments[d].update(view, digits[d], self.words[d])
        for h in range(3):
            (x0, y0) = (self.pos + 44, 56+48*h)
            pygame.draw.line(view.win, (40, 120, 40), (x0+40, y0+4), (x0+140, y0+4))
        for v in range(2):
            for h in range(2):
                (x0, y0) = (self.pos+36+48*v, 64+48*h)
                if v == 0:
                    pygame.draw.line(view.win, (40, 120, 40), (x0+4, y0+h*46), (x0+4, y0-26+h*92))
                    pygame.draw.line(view.win, (40, 120, 40),
                                     (x0+4, y0-26+h*92), (x0+148, y0-26+h*92))
                else:
                    pygame.draw.line(view.win, (40, 120, 40), (x0+8, y0+20), (x0+100, y0+20))

        chars = "abcdefg "
        for l in range(len(chars)):
            (x0, y0) = (self.pos+184, 28)
            pygame.draw.line(view.win, (40, 120, 40), (x0, y0+24*l), (x0 + 168, y0+24*l))
            pygame.draw.line(view.win, (40, 120, 40), (x0+24*l, y0), (x0 + 24*l, y0+168))
            view.font.render_to(view.win, (x0+24*l+8, y0-4), chars[l], (120, 240, 120))
            if l == 7:
                break
            bits = matrix[chars[l]]
            for b in range(len(chars) - 1):
                d = 1 if chars[l] == letter else 2
                col = (200//d, 200//d, 200//d)
                w = 0 if (bits & (1 << (6-b))) != 0 else 1
                pygame.draw.rect(view.win, col, (x0+24*l+6, y0+24*b+6, 12, 12), w)

        (x0, y0) = (self.pos+36, 64+96+48)
        for i in range(idx+1, len(self.words)):
            view.font.render_to(view.win, (x0, y0+(i-idx)*24), self.words[i], (80, 160, 80))


def init(controller):
    descrambler = Descrambler()
    with open(controller.workdir() + "/input/day08.txt") as f:
        line = f.readline().split('|')
        data = []
        for w in line[0].split():
            data.append(''.join(sorted(w)))
        code = []
        for w in line[1].split():
            code.append(''.join(sorted(w)))
        descrambler.descramble(data)
        controller.add(Solver(data, code, descrambler.history))
    return controller


view = View(960, 540, 10)
view.setup("Day 08")
controller = Controller()
init(controller).run(view)
