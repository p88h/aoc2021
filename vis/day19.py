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
import itertools
from common import View, Controller
from collections import Counter

class Solver:
    def __init__(self, lines) -> None:
        self.scanners = []
        cur = None
        for l in lines:
            if l == "":
                continue
            elif l[0:3] == "---":
                cur = []
                self.scanners.append(cur)
            else:
                cur.append(tuple(map(int, l.split(","))))
        self.done = set()
        self.next = [ self.scanners[0] ]
        self.rest = self.scanners[1:]
        self.shifts = []
        self.unrest = []
        self.aligned = None

          
    def try_align(self, aligned, candidate):
        ret = []
        dl = []
        dp = dpp = None
        for dim in range(3):
            x = [pos[dim] for pos in aligned]
            for (d,s) in [(0,1),(1,1),(2,1),(0,-1),(1,-1),(2,-1)]:
                if d == dp or d == dpp:
                    continue
                t = [pos[d]*s for pos in candidate]
                w = [b-a for (a,b) in itertools.product(x, t)]
                c = Counter(w).most_common(1)
                if c[0][1] >= 12:
                    break        
            if c[0][1] < 12:
                return None
            (dpp, dp) = (dp, d)
            ret.append([v - c[0][0] for v in t])
            dl.append(c[0][0])
        return (list(zip(ret[0],ret[1],ret[2])), dl)


    def solve_step(self):
        if not self.aligned:
            if self.next:
                self.aligned = self.next.pop()
            else:
                return
        if self.rest:
            self.candidate = self.rest.pop()
            self.result = self.try_align(self.aligned, self.candidate)
        else:
            self.rest = self.unrest
            self.done.update(self.aligned)
            self.aligned = None
            self.unrest = []
    
    def update(self):
        if self.result:
            (updated, shift) = self.result
            self.shifts.append(shift)
            self.next.append(updated)
        elif self.candidate:
            self.unrest.append(self.candidate)
        self.result = None
        self.candidate = None

class Plotter:
    def __init__(self, solver):
        self.solver = solver
    
    def render(self, view, scanner, dy, col):
        dx = 0
        for p in scanner:                                    
            view.font.render_to(view.win, (dx, dy), str(p[0]), col)
            view.font.render_to(view.win, (dx, dy+16), str(p[1]), col)
            view.font.render_to(view.win, (dx, dy+32), str(p[2]), col)
            dx += 48
            if dx == 1920:
                dx = 0
                dy += 56

    def update(self, view, controller):
        if not controller.animate:
            return
        view.win.fill((0,0,0))
        self.solver.solve_step()
        dy = 16        
        for s in self.solver.next[-5:-1]:
            self.render(view, s, dy, (200,255,200))
            dy += 56
        if self.solver.aligned:
            self.render(view, self.solver.aligned, dy, (255,255,180))
            dy += 56
        if self.solver.candidate:
            if self.solver.result:
                self.render(view, self.solver.candidate, dy, (200,255,200))
            else:
                self.render(view, self.solver.candidate, dy, (255,200, 200))
            dy += 56
        dc = 160
        for s in self.solver.rest[::-1]:
            self.render(view, s, dy, (dc,dc,dc))
            dy += 56
            dc -= 20
            if not dc:
                break
        if dy == 56:
            controller.animate = False
        self.render(view, self.solver.done, dy, (200,200,250))
        self.solver.update()

def init(controller):
    with open(controller.workdir() + "/input/day19.txt") as f:
        solver = Solver(f.read().splitlines())
        controller.add(Plotter(solver))
    return controller

view = View(1920, 1080, 10)
view.setup("Day 19")
controller = Controller()
init(controller).run(view)
