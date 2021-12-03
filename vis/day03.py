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


class Dataset:
    def __init__(self, base_path):
        self.idx = 0
        self.bit = 0
        self.filtered = []
        with open(base_path + "/input/day03.txt") as f:
            self.lines = f.read().splitlines()
        self.major = self.majority()

    def bbox(self, view, pos):
        S = 8
        w = (view.width - 128) // S
        (px, py) = (pos % w, pos // w)
        x = 64+px*S
        y = 32+py*S*13
        return (x, y)

    def paint(self, view, item, pos):
        (x, y) = self.bbox(view, pos)
        for j in range(len(item)):
            if item[j] == "0":
                pygame.draw.rect(view.win, (255, 255, 255), (x, y + j * 8, 6, 6), 1)
            else:
                pygame.draw.rect(view.win, (255, 255, 255), (x, y + j * 8, 6, 6), 0)

    def majority(self):
        d = {"0": 0, "1": 0}
        for item in self.lines:
            d[item[self.bit]] += 1
        return "0" if d["0"] > d["1"] else "1"

    def update(self, view, controller):
        if self.bit == 12:
            controller.animate = False
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
        if not controller.animate:
            return
        if self.idx < len(self.lines):
            if self.lines[self.idx][self.bit] == self.major:
                self.filtered.append(self.lines[self.idx])
            self.idx += 1
        else:
            self.lines = self.filtered
            self.filtered = []
            self.idx = 0
            self.bit += 1
            if self.bit < 11:
                self.major = self.majority()


view = View(1280, 720, 40)
view.setup("Day 03")
controller = Controller()
my_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
view.record(my_dir + "/day3.mp4")
controller.add(Dataset(my_dir))
controller.run(view)
