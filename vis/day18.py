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
            for j in range(1 + len(items[i]) // 110):
                if k == 50:
                    break
                w = items[i][j*110:(j+1)*110]
                csel = i + 1 if i < 2 else 0
                self.lines[k].render(surface, w, csel, pfx - j*110)
                k += 1
        while k < len(self.lines):
            self.lines[k].render(surface, "", 0, 0)
            k += 1


class Node:
    def __init__(self) -> None:
        self.value = None
        self.left = self.right = None

    def addtofirst(self, val):
        if not self.left:
            self.value += val
        else:
            self.left.addtofirst(val)

    def addtolast(self, val):
        if not self.right:
            self.value += val
        else:
            self.right.addtolast(val)

    def tryexplode(self, depth=0):
        if depth < 4 and self.left:
            (e, l, r) = self.left.tryexplode(depth+1)
            if not e:
                (e, l, r) = self.right.tryexplode(depth+1)
                if e and l > 0:
                    self.left.addtolast(l)
                    l = -1
            elif r > 0:
                self.right.addtofirst(r)
                r = -1
            return (e, l, r)
        if depth == 4 and self.left:
            ret = (True, self.left.value, self.right.value)
            self.value = 0
            self.left = self.right = None
            return ret
        else:
            return (False, -1, -1)

    def trysplit(self):
        if self.left:
            return self.left.trysplit() or self.right.trysplit()
        elif self.value >= 10:
            self.left = Node()
            self.right = Node()
            self.left.value = self.value // 2
            self.right.value = self.value - self.left.value
            self.value = None
            return True
        else:
            return False

    def magnitude(self):
        if self.left:
            return 3*self.left.magnitude()+2*self.right.magnitude()
        else:
            return self.value

    def str(self, depth=0):
        if not self.left:
            return str(self.value)
        else:
            return ("[")+self.left.str(depth+1)+","+self.right.str(depth+1)+"]"


class Solver:
    def __init__(self, lines, display):
        self.lines = lines
        self.display = display
        self.idx = 0
        (_, self.top) = self.parse(lines[0], 1)
        self.other = None

    def number(self, line, pos):
        npos = pos
        while line[npos] != ',' and line[npos] != ']':
            npos += 1
        node = Node()
        node.value = int(line[pos:npos])
        return (npos+1, node)

    def parse(self, line, pos):
        node = Node()
        npos = pos
        if line[npos] == '[':
            (npos, node.left) = self.parse(line, npos+1)
        else:
            (npos, node.left) = self.number(line, npos)
        if line[npos] == '[':
            (npos, node.right) = self.parse(line, npos+1)
        else:
            (npos, node.right) = self.number(line, npos)
        return (npos+1, node)

    def add(self, left, right):
        node = Node()
        node.left = left
        node.right = right
        return node

    def update(self, view, controller):
        if not controller.animate:
            return
        cnt = 0
        while cnt < min(64, self.idx):
            (e, _, _) = self.top.tryexplode(0)
            if not e:
                e = self.top.trysplit()
            if e:
                cnt += 1
            else:
                break
        e = cnt > 0
        if self.other:
            self.top = self.add(self.top, self.other)
            self.other = None
            self.idx += 1
            e = True
        elif not e and self.idx + 1 < len(self.lines):
            (_, self.other) = self.parse(self.lines[self.idx + 1], 1)

        self.lines[self.idx] = self.top.str()
        if not e and self.idx == len(self.lines)-1:
            self.lines[self.idx] += " = {}".format(self.top.magnitude())
        view.win.fill((0, 0, 0))
        self.display.render(view.win, self.lines[self.idx:], 0)

        if not e and self.idx + 1 >= len(self.lines):
            controller.animate = False


def init(controller):
    with open(controller.workdir() + "/input/day18.txt") as f:
        lines = f.read().splitlines()
        disp = DotDisplay((25, 15))
        controller.add(Solver(lines, disp))
    return controller


view = View(1920, 1080, 15)
view.setup("Day 18")
controller = Controller()
init(controller).run(view)
