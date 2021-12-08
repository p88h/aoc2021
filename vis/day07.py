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
import math
import os
from common import View, Controller
import numpy as np
from numpy.polynomial import polynomial as poly

class Painter:
    def __init__(self, points):
        self.points = points
        self.a = 0
        self.b = max(self.points)
        self.thist = []
        self.ehist = []

    def update(self, view, controller):
        if view.frame >= self.b:
            controller.animate = False
            return
        view.win.fill((0,0,0))
        c = view.frame
        ofs = (view.width - self.b) // 2
        pos = view.height // 2
        pygame.draw.line(view.win, (200, 200, 200), (ofs, pos), (view.width-ofs , pos), 1)
        pygame.draw.line(view.win, (240, 240, 240), (ofs + c, pos - 2), (ofs + c, pos + 2), 1)
        th = 0
        eh = 0
        for p in self.points:
            w = 2 if p < c else 1
            pygame.draw.circle(view.win, (240,240,240), (ofs+p, pos), 2, w)
            h = abs(p - c)
            th += h
            h //= 4
            e = (abs(p - c) * (abs(p -c) + 1) // 2)
            eh += e 
            e //= 16
            pygame.draw.line(view.win, (240,240,240), (ofs+p, pos-h), (ofs+p, pos), 1)
            pygame.draw.line(view.win, (160,240,160), (ofs+p-2, pos-h), (ofs+p+2, pos-h), 2)
            pygame.draw.line(view.win, (240,160,160), (ofs+p-2, pos-e), (ofs+p+2, pos-e), 2)
        self.thist.append(th)
        self.ehist.append(eh)
        m1 = 0

        if len(self.ehist) > 5:
            minv = 1600000*1000
            minp = 0
            for tx in range(self.a, self.b):
                v = min(max(0, int(self.epoly(tx))), 1600000*1000)
                if v < minv:
                    minv = v
                    minp = tx                    
                dh = v // 1600000
                gd.pixel(view.win, ofs+tx, pos+dh, (160, 80, 80))
            dh = minv // 1600000
            (x, y) = (ofs+minp, pos+dh)
            if c < minp:
                pygame.draw.circle(view.win, (160,160,160), (x, y), 4, 1)
            view.font.render_to(view.win, (x-24, y+6), "EST[2]: {}@{}".format(minv,minp), (240, 120, 120))

        for i in range(len(self.thist)):
            dh = self.thist[i] // 4000
            gd.pixel(view.win, ofs+i, pos+dh, (160, 255, 160))
            if self.thist[i] <= self.thist[m1]:
                m1 = i
        (x, y) = (ofs+m1, pos+ self.thist[m1] // 4000)
        pygame.draw.circle(view.win, (240,240,240), (x, y), 4, 1)
        view.font.render_to(view.win, (x-24,y-24), "MIN[1]: {}@{}".format(self.thist[m1],m1), (160, 255, 160))

        m2 = 0
        for i in range(len(self.ehist)):
            dh = self.ehist[i] // 1600000
            gd.pixel(view.win, ofs+i, pos+dh, (255, 160, 160))
            if self.ehist[i] <= self.ehist[m2]:
                m2 = i
        (x, y) = (ofs+m2, pos+self.ehist[m2] // 1600000)
        pygame.draw.circle(view.win, (240,240,240), (x, y), 4, 1)
        view.font.render_to(view.win, (x-24,y-24), "MIN[2]: {}@{}".format(self.ehist[m2],m2), (255, 160, 160))

        if len(self.ehist) == 5:
            ax = np.array(range(5))
            ay = np.array(self.ehist)
            self.epoly = np.poly1d(np.polyfit(ax, ay, deg=2))


def init(my_dir, controller):
    with open(my_dir + "/input/day07.txt") as f:
        points = map(int, f.readline().split(","))
        controller.add(Painter(list(sorted(points))))

view = View()
view.setup("Day 07")
controller = Controller()
my_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
init(my_dir, controller)
view.record(my_dir + "/day7.mp4")
controller.run(view)
