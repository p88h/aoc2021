# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pygame
import math
from common import View, Controller


class DotFont:
    def __init__(self) -> None:
        self.segmap = {
            '0': [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]],
            '1': [[0, 0, 1, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [1, 1, 1, 1]],
            '2': [[0, 1, 1, 0], [1, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]],
            '3': [[0, 1, 1, 0], [1, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]],
            '4': [[0, 1, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1]],
            '5': [[1, 1, 1, 1], [1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 1], [1, 1, 1, 0]],
            '6': [[0, 1, 1, 0], [1, 0, 0, 0], [1, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]],
            '7': [[1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0]],
            '8': [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]],
            '9': [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 1], [0, 0, 0, 1], [0, 1, 1, 0]],
            ' ': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            'A': [[0, 1, 1, 0], [1, 0, 0, 1], [1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1]],
            'B': [[1, 1, 1, 0], [1, 0, 0, 1], [1, 1, 1, 1], [1, 0, 0, 1], [1, 1, 1, 0]],
            'C': [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 0], [1, 0, 0, 1], [0, 1, 1, 1]],
            'D': [[1, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 1, 0]],
            'E': [[1, 1, 1, 1], [1, 0, 0, 0], [1, 1, 1, 0], [1, 0, 0, 0], [1, 1, 1, 1]],
            'F': [[1, 1, 1, 1], [1, 0, 0, 0], [1, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
            '+': [[0, 0, 0, 0], [0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
            '-': [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            '*': [[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 0]],
            '<': [[0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]],
            '>': [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]],
            '=': [[0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0]],
            '[': [[0, 1, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0]],
            ']': [[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 1, 1, 0]],
            '(': [[0, 0, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]],
            ')': [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 1, 0, 0]],
            'L': [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 0]],
            '.': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
            ',': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 0, 0]],
            '~': [[0, 0, 0, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 0, 0, 0], [0, 1, 0, 0]],
            'v': [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0]],
            '^': [[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]
        }

    def get(self, ch):
        return self.segmap[ch]


class DotUnit:
    def __init__(self, font, pos):
        self.font = font
        self.tmp = pygame.Surface((4 * 4, 5 * 4))
        self.draw(' ', 0)
        self.pos = pos

    def draw(self, digit, csel=0):
        segs = self.font.get(digit)
        for i in range(len(segs)):
            for j in range(len(segs[i])):
                (x0, y0) = (4 * j, 4 * i)
                cols = [(255, 180, 180), (160, 160, 240), (160, 160, 40), (180, 255, 180)]
                col = cols[csel]
                if segs[i][j] == 0:
                    col = (60, 60, 60)
                pygame.draw.rect(self.tmp, col, (x0, y0, 3, 3))
        self.last = (digit, csel)

    def render(self, surface, digit, csel=0):
        if (digit, csel) != self.last:
            self.draw(digit, csel)
        surface.blit(self.tmp, self.pos)


class DotLine:
    def __init__(self, font, pos):
        (x, y) = pos
        self.units = [DotUnit(font, (x + i * 17, y)) for i in range(110)]

    def render(self, surface, word, csel, pfx):
        for i in range(len(self.units)):
            ch = word[i] if i < len(word) else ' '
            self.units[i].render(surface, ch, 3 if i < pfx else csel)


class DotDisplay:
    def __init__(self, pos):
        (x, y) = pos
        self.font = DotFont()
        self.lines = [DotLine(self.font, (x, y + i * 21)) for i in range(50)]

    def render(self, surface, items, bitpfx):
        k = 0
        l = len(items)
        for i in range(l):
            pfx = 0
            csel = 0
            if i == l - 2:
                csel = 1
                pfx = bitpfx
            if i == l - 1:
                csel = 2
            for j in range(1 + len(items[i]) // 110):
                if k == 50:
                    break
                w = items[i][j*110:(j+1)*110]
                self.lines[k].render(surface, w, csel, pfx - j*110)
                k += 1
        while k < len(self.lines):
            self.lines[k].render(surface, "", 0, 0)
            k += 1


class Solver:
    def __init__(self, text, display):
        self.stack = []
        self.bitstring = ""
        self.hexstring = text
        self.hexpos = 0
        self.bitpos = 0
        self.biteat = 0
        self.bitneed = 0
        self.display = display
        self.idx = 0
        self.ops = {0: "+", 1: "*", 2: "v", 3: "^", 4: "L", 5: ">", 6: "<", 7: "="}
        self.state = 0
        self.answer = None

    def bitlen(self):
        v = int(self.bitstring[self.bitpos:self.bitpos+3], 2)
        t = int(self.bitstring[self.bitpos+3:self.bitpos+6], 2)
        sz = 6
        if t in [0, 1, 2, 3, 5, 6, 7]:
            sz += 12 if self.bitstring[self.bitpos + 6] == 1 else 16
        elif t == 4:
            while self.bitstring[self.bitpos + sz] == 1:
                sz += 5
            sz += 5
        return sz

    def parse(self):
        v = int(self.bitstring[self.bitpos:self.bitpos+3], 2)
        t = int(self.bitstring[self.bitpos+3:self.bitpos+6], 2)
        self.bitpos += 6
        if t in [0, 1, 2, 3, 5, 6, 7]:
            k = int(self.bitstring[self.bitpos])
            self.bitpos += 1
            if k:
                n = int(self.bitstring[self.bitpos:self.bitpos+11], 2)
                self.bitpos += 11
                self.stack.append((self.ops[t], "[", "]", n, []))
            else:
                l = int(self.bitstring[self.bitpos:self.bitpos+15], 2)
                self.bitpos += 15
                self.stack.append((self.ops[t], "(", ")", self.bitpos + l, []))
        elif t == 4:
            acc = 0
            while True:
                m = int(self.bitstring[self.bitpos])
                acc = acc * 16 + int(self.bitstring[self.bitpos+1:self.bitpos+5], 2)
                self.bitpos += 5
                if m == 0:
                    break
            self.stack.append((self.ops[t], "=", "", 1, [acc]))

    def ready(self, elem):
        (_op, d1, _d2, lim, arr) = elem
        return (d1 == "(" and self.bitpos == lim) or len(arr) == lim

    def check(self):
        if not self.stack:
            return False
        if not self.ready(self.stack[-1]):
            return False
        (op, d1, _d2, lim, arr) = self.stack.pop()
        v = 0
        if op == "L":
            v = arr[0]
        elif op == "+":
            v = sum(arr)
        elif op == "*":
            v = math.prod(arr)
        elif op == "v":
            v = min(arr)
        elif op == "^":
            v = max(arr)
        elif op == "<":
            v = 1 if arr[0] < arr[1] else 0
        elif op == ">":
            v = 1 if arr[0] > arr[1] else 0
        elif op == "=":
            v = 1 if arr[0] == arr[1] else 0
        if len(self.stack):
            (op, d1, _d2, lim, arr) = self.stack[-1]
            arr.append(v)
        else:
            self.answer = v
        return True

    def describe(self):
        if self.answer:
            return [str(self.answer)]
        items = []
        for frame in self.stack:
            (op, d1, d2, lim, arr) = frame
            header = "{}{}{}".format(op, d1, ','.join([str(i) for i in arr]))
            if not self.ready(frame):
                header += " ... "
                if d1 == "[":
                    header += "+{}".format(lim - len(arr))
                else:
                    header += "~{}".format(lim - self.bitpos)
            header += d2
            while len(header) % 10:
                header += " "
            items.append(header)
        return items

    def update(self, view, controller):
        view.win.fill((0, 0, 0))

        if self.hexpos < len(self.hexstring):
            self.bitstring += "{:04b}".format(int(self.hexstring[self.hexpos], 16))
            self.hexpos += 1

        if self.answer or self.check():
            pass
        elif self.bitneed == 0 and len(self.bitstring) > 40:
            self.bitneed = self.bitlen()
        elif self.bitneed > 0 and self.bitpos + self.bitneed <= self.biteat:
            self.parse()
            self.bitneed = 0
        elif len(self.bitstring) > 40:
            self.biteat += 2

        items = self.describe()
        items.append(self.bitstring[self.bitpos:])
        items.append(self.hexstring[self.hexpos:])
        self.display.render(view.win, items, self.biteat-self.bitpos)


def init(controller):
    with open(controller.workdir() + "/input/day16.txt") as f:
        line = f.readline()
        disp = DotDisplay((25, 15))
        controller.add(Solver(line, disp))
    return controller


view = View(1920, 1080, 60)
view.setup("Day 16")
controller = Controller()
init(controller).run(view)
