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
import os
from common import View, Controller
from functools import reduce


class DotFont:
    def __init__(self) -> None:
        self.segmap = {
            '{': [[0, 1, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0]],
            '[': [[0, 1, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0]],
            '(': [[0, 0, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]],
            '<': [[0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]],
            '}': [[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 1, 0]],
            ']': [[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 1, 1, 0]],
            ')': [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 1, 0, 0]],
            '>': [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]],
            '0': [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]],
            '1': [[0, 0, 1, 0], [0, 1, 1, 0], [1, 0, 1, 0], [0, 0, 1, 0], [0, 1, 1, 1]],
            '2': [[0, 1, 1, 0], [1, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]],
            '3': [[0, 1, 1, 0], [1, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]],
            '4': [[1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1]],
            '5': [[1, 1, 1, 1], [1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 1], [1, 1, 1, 0]],
            '6': [[0, 1, 1, 1], [1, 0, 0, 0], [1, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]],
            '7': [[1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0]],
            '8': [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]],
            '9': [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 1], [0, 0, 0, 1], [0, 1, 1, 0]],
            ' ': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        }

    def get(self, ch):
        return self.segmap[ch]


class DotUnit:
    def __init__(self, font, pos):
        self.font = font
        self.pos = pos

    def render(self, surface, digit, hl, hd):
        segs = self.font.get(digit)
        (x, y) = self.pos
        for i in range(len(segs)):
            for j in range(len(segs[i])):
                (x0, y0) = (x + 4*j, y + 4*i)
                if hl:
                    col = (180,255,180) if hd<0 else (160,160,240)
                    col = (255,180,180) if hd==0 else col
                else:
                    col = (160,160,40)
                if segs[i][j] == 0:
                    col = (60, 60, 60)
                pygame.draw.rect(surface, col, (x0, y0, 3, 3))
                pygame.draw.line(surface, (0, 0, 0, 0), (x0, y0+3), (x0+3, y0), 1)


class DotLine:
    def __init__(self, font, pos):
        (x, y) = pos
        self.ofs = y
        self.units = [DotUnit(font, (x + i*17, 0)) for i in range(110)]
        self.tmp = pygame.Surface((1920, 20))
        self.ready = False

    def render(self, surface, word, hl, hi):
        if hl or not self.ready:
            for i in range(len(self.units)):
                ch = word[i] if i < len(word) else ' '
                self.units[i].render(self.tmp, ch, hl, i - hi)
            self.ready = True
        surface.blit(self.tmp, (0, self.ofs))


class DotDisplay:
    def __init__(self, pos):
        (x, y) = pos
        self.font = DotFont()
        self.lines = [DotLine(self.font, (x, y + i * 21)) for i in range(50)]

    def render(self, surface, words, hw, hi):
        for i in range(len(self.lines)):
            w = words[i] if i < len(words) else ""
            self.lines[i].render(surface, w, hw == i, hi)


class Solver:
    def __init__(self, words, display):
        self.words = words
        self.display = display
        self.idx = 0
        self.cw = 0
        self.cnt = True
        self.mt = {"(": ")", "[": "]", "{": "}", "<": ">"}
        self.z1 = {")" : 3, "]" : 57, "}" : 1197, ">" : 25137}
        self.z2 = {"(" : 1, "[" : 2, "{" : 3, "<" : 4}


    def update(self, view, controller):
        if self.cw == len(self.words):
            controller.animate = False
            return
        view.win.fill((0,0,0))
        w = self.words[self.cw]
        i = self.idx
        if self.cnt and i < len(w):
            if i > 0 and w[i-1] in self.mt and w[i] == self.mt[w[i-1]]:
                self.words[self.cw] = w[:i-1] + w[i+1:]
                self.idx -= 1
            elif w[i] in self.mt:
                self.idx += 1
            else:
                if i < len(w) - 1:
                    self.words[self.cw] = w[:i+1]
                else:
                    self.words[self.cw] += " {}".format(self.z1[w[i]])
                    self.cnt = False
        elif self.cnt and i == len(w):
            score = 0
            for j in range(i,0,-1):
                score = score * 5 + self.z2[w[j-1]]
            self.words[self.cw] += " {}".format(score)
            self.cnt = False
        else:
            self.idx = 0
            self.cw += 1
            self.cnt = True
   
        self.display.render(view.win, self.words, self.cw, self.idx)



def init(my_dir, controller):    
    with open(my_dir + "/input/day10.txt") as f:
        lines = f.read().splitlines()
        disp = DotDisplay((25,15))
        controller.add(Solver(lines[:50], disp))


view = View(1920, 1080, 60)
view.setup("Day 10")
controller = Controller()
my_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
init(my_dir, controller)
view.record(my_dir + "/day10.mp4")
controller.run(view)
