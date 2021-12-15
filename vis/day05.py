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
from pygame import gfxdraw as gd
from common import View, Controller


class Painter:
    def __init__(self, lines):
        self.lines = lines
        self.dupes = {}

    def update(self, view, controller):
        if view.frame >= len(self.lines):
            controller.animate = False
            return
        idx = view.frame
        (x0, y0, x1, y1) = self.lines[idx]
        pygame.draw.line(view.win, (40, 40, 80), (x0, y0), (x1, y1), 1)
        while True:
            if (x0, y0) in self.dupes:
                gd.pixel(view.win, x0, y0, (255, 220, 220))
            else:
                self.dupes[(x0, y0)] = 1
            if x0 == x1 and y0 == y1:
                break
            if x0 != x1:
                x0 = x0 + 1 if x0 < x1 else x0 - 1
            if y0 != y1:
                y0 = y0 + 1 if y0 < y1 else y0 - 1


def init(controller):
    with open(controller.workdir() + "/input/day05.txt") as f:
        lines1 = []
        lines2 = []
        for line in f.read().splitlines():
            line = line.replace(" -> ", ",")
            (x0, y0, x1, y1) = tuple(map(int, line.split(",")))
            if x0 == x1 or y0 == y1:
                lines1.append((x0, y0, x1, y1))
            else:
                lines2.append((x0, y0, x1, y1))
        lines1.extend(lines2)
        controller.add(Painter(lines1))
    return controller


view = View(1000, 1000, 15)
view.setup("Day 05")
controller = Controller()
init(controller).run(view)
