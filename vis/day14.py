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
import random
from common import View, Controller


class Element:
    def __init__(self, font, ch):
        self.surface = pygame.Surface((32, 32))
        bg = (random.randint(20, 80), random.randint(20, 80), random.randint(20, 80))
        col = (random.randint(160, 240), random.randint(160, 240), random.randint(160, 240))
        self.surface.fill(bg)
        pygame.draw.rect(self.surface, (200, 160, 80), (0, 0, 32, 32), 2)
        font.render_to(self.surface, (12, 20), ch, col)


class ChainRenderer:
    def __init__(self, font):
        self.chars = {}
        self.font = font
        for c in range(65, 91):
            self.chars[chr(c)] = Element(font, chr(c))

    def render(self, win, word, a, b, pos=(10, 10)):
        idx = 0
        (px, py) = pos
        W = self.chars['A'].surface.get_width()
        S = 4
        B = 53
        L = 19
        for c in word:
            if (idx == L * B):
                break
            (x, y) = pos
            r = (idx // B)
            x += (B - abs((idx % (B * 2)) - B) - r % 2) * (S + W)
            y += r * (S + W)
            win.blit(self.chars[c].surface, (x, y))
            if y > py:
                pygame.draw.line(win, (200, 160, 80), (x + W // 2, y), (x + W // 2, y - S), 2)
            elif x > px:
                pygame.draw.line(win, (200, 160, 80), (x - S, y + W // 2), (x, y + W // 2), 2)
            elif x < px:
                pygame.draw.line(win, (200, 160, 80), (x + W, y + W // 2),
                                 (x + W + S, y + W // 2), 2)
            if idx == a or idx == b:
                pygame.draw.rect(win, (250, 250, 200), (x, y, W, W), 2)
            if idx > a and idx < b:
                pygame.draw.rect(win, (200, 250, 200), (x, y, W, W), 2)
            (px, py) = (x, y)
            idx += 1


class CountRenderer:
    def __init__(self, chain):
        self.chars = chain.chars
        self.font = chain.font

    def count(self, word):
        counts = {}
        z = None
        for c in word:
            if z:
                counts[z + c] = 1 if (z + c) not in counts else counts[z + c] + 1
            z = c
        return counts

    def render(self, win, counts, iter, word, pos=(10, 710)):
        idx = 0
        W = self.chars['A'].surface.get_width()
        S = 4
        ccounts = {word[0]: 1}
        for p in counts:
            (x, y) = pos
            x += (idx//10) * W * 4
            y += (idx % 10) * (S+W)
            win.blit(self.chars[p[0]].surface, (x, y))
            win.blit(self.chars[p[1]].surface, (x + W, y))
            self.font.render_to(win, (x + 2*W + S, y + W//2 + 4), str(counts[p]), (200, 250, 200))
            idx += 1
            ccounts[p[1]] = counts[p] if p[1] not in ccounts else ccounts[p[1]] + counts[p]
        lmax = lmin = word[0]
        for l in ccounts:
            if ccounts[l] < ccounts[lmin]:
                lmin = l
            if ccounts[l] > ccounts[lmin]:
                lmax = l
        (x, y) = pos
        x += (1 + idx // 10) * W * 4
        txt = "Iteration: {}".format(iter)
        self.font.render_to(win, (x, y + 16), txt, (200, 250, 200))
        txt = "Min element: {} -> {}".format(lmin, ccounts[lmin])
        self.font.render_to(win, (x, y + 32), txt, (200, 250, 200))
        txt = "Max element: {} -> {}".format(lmax, ccounts[lmax])
        self.font.render_to(win, (x, y + 48), txt, (200, 250, 200))


class Polymer:
    def __init__(self, chainr, countr, word, rules):
        self.chainr = chainr
        self.countr = countr
        self.cntmap = countr.count(word)
        self.word = word
        self.rules = rules
        self.idx = 0
        self.iter = 1

    def update(self, view, controller):
        if self.idx == len(self.word) - 1 or self.idx == 1024:
            if self.iter == 10:
                controller.animate = False
                return
            self.idx = 0
            self.iter += 1
            nmap = {}
            for p in self.cntmap:
                x = self.cntmap[p]
                if p in self.rules:
                    l = p[0] + self.rules[p]
                    r = self.rules[p] + p[1]
                    nmap[l] = x if l not in nmap else nmap[l] + x
                    nmap[r] = x if r not in nmap else nmap[r] + x
            self.cntmap = nmap

        pfx = self.word[self.idx:self.idx + 2]
        pidx = self.idx
        if pfx in rules:
            self.word = self.word[:self.idx + 1] + rules[pfx] + self.word[self.idx + 1:]
            self.idx += 2
        else:
            self.idx += 1

        cm = self.countr.count(self.word) if len(self.word) < 1024 else self.cntmap

        view.win.fill((0, 0, 0))
        self.chainr.render(view.win, self.word, pidx, self.idx)
        self.countr.render(view.win, cm, self.iter, self.word)


view = View(1920, 1080, 30)
view.setup("Day 14")
controller = Controller()
with open(controller.workdir() + "/input/day14.txt") as f:
    lines = f.read().splitlines()
    rules = {}
    for l in lines[2:]:
        (f, t) = l.split(' -> ')
        rules[f] = t
    chain = ChainRenderer(view.font)
    count = CountRenderer(chain)
    controller.add(Polymer(chain, count, lines[0], rules))
controller.run(view)
