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
import pygame.freetype
from common import View, Controller


class Dataset:
    def __init__(self, base_path):
        self.idx = 0
        self.bit = 0
        self.filtered = []
        self.mode = 1
        self.dcnt = {"0": 0, "1": 0}
        with open(base_path + "/input/day03.txt") as f:
            self.lines = f.read().splitlines()
        self.major = self.majority()

    def bbox(self, view, pos):
        S = 8
        w = (view.width - 128) // S
        (px, py) = (pos % w, pos // w)
        x = 64 + px * S
        y = 32 + py * S * 13
        return (x, y)

    def paint(self, view, item, pos, sel=(255, 255, 255)):
        (x, y) = self.bbox(view, pos)
        for j in range(len(item)):
            col = (255, 255, 255)
            if j == self.bit:
                col = sel
            if item[j] == "0":
                pygame.draw.rect(view.win, col, (x, y + j * 8, 6, 6), 1)
            else:
                pygame.draw.rect(view.win, col, (x, y + j * 8, 6, 6), 0)

    def majority(self):
        d = {"0": 0, "1": 0}
        for item in self.lines:
            d[item[self.bit]] += 1
        return "0" if d["0"] > d["1"] else "1"

    def legend(self, view):
        (x, y) = self.bbox(view, 0)
        text = "{:3d}     {:3d}".format(self.dcnt["0"], self.dcnt["1"])
        pygame.draw.rect(view.win, (255, 255, 255), (x + 32, y - 14, 6, 6), 1)
        pygame.draw.rect(view.win, (255, 255, 255), (x + 96, y - 14, 6, 6), 0)
        view.font.render_to(view.win, (x, y-8), text, (255, 255, 255))

    def update(self, view, controller):
        if self.bit == 12:
            controller.animate = False
        if not controller.animate:
            return
        if self.mode == 1:
            view.win.fill((0, 0, 0))
            for i in range(self.idx):
                self.paint(view, self.lines[i], i, (160, 160, 240))
            for i in range(self.idx, self.idx+4):
                if i < len(self.lines):
                    self.dcnt[self.lines[i][self.bit]] += 1
                    self.paint(view, self.lines[i], i, (160, 240, 160))
            for i in range(self.idx+4, len(self.lines)):
                self.paint(view, self.lines[i], i)
            self.legend(view)
            if not controller.animate:
                return
            self.idx += 4
            if self.idx >= len(self.lines):
                self.idx = 0
                self.mode = 2
                self.major = self.majority()
            return

        view.win.fill((0, 0, 0))
        fl = len(self.filtered)
        for i in range(fl):
            self.paint(view, self.filtered[i], i)
        (x, y) = self.bbox(view, fl)
        y += self.bit * 8
        pygame.draw.line(view.win, (255, 255, 255), (x+3, y), (x, y+3), 2)
        pygame.draw.line(view.win, (255, 255, 255), (x, y+3), (x+3, y+6), 2)
        for i in range(self.idx, len(self.lines)):
            self.paint(view, self.lines[i], i-self.idx+fl+1)
        self.legend(view)
        if self.idx < len(self.lines):
            item = self.lines[self.idx]
            if item[self.bit] == self.major:
                self.filtered.append(item)
            else:
                self.dcnt[item[self.bit]] -= 1
            self.idx += 1
        else:
            self.lines = self.filtered
            self.filtered = []
            self.idx = 0
            self.bit += 1
            self.mode = 1
            self.dcnt = {"0": 0, "1": 0}


view = View(1280, 800, 60)
view.setup("Day 03")
controller = Controller()
controller.add(Dataset(controller.workdir()))
controller.run(view)
